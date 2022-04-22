import librosa
import os
import numpy as np

import tkinter


# чтение файла
def read_file(folder_name):

    # чтение директории с файлами
    files = os.listdir(folder_name)

    # список для сегментов
    segments_to_share = []

    # предел времени для сегментации записи, измеряется в секундах
    time_lim = 30

    # флаг для анализа корректных файлов
    flag_for_audio_files = 0

    # чтение файлов
    for name in files:

        # проверка формата файла
        if name.endswith(('.wav', '.mp3')):

            # флаг меняется, если был найден хоть один корректный файл
            flag_for_audio_files = 1

            # определение полного пути и имени файла
            file_name = os.path.join(folder_name, name)

            # чтение файла
            x, sr = librosa.load(file_name, mono=False, sr=None)

            # проверка: нужно ли файл сегментировать
            duration = librosa.get_duration(y=x, sr=sr)

            # временные граници цифрового сигнала
            time_start = 0
            time_end = duration

            if duration > time_lim:

                # сегментация и добавление сегментов записи
                segments = segmention(x=x,
                                      sr=sr,
                                      time_lim=time_lim,
                                      file_name=file_name,
                                      time_start=time_start,
                                      time_end=time_end)

                for i in segments:
                    segments_to_share += [i]

            else:

                # добавление не сегментируемой записи
                segments = [x, sr, file_name, time_start, time_end]
                segments_to_share += [segments]

    if flag_for_audio_files:

        return segments_to_share

    else:

        # Файлы для обработки не обнаружены
        print('Файлы .wav и .mp3 не были обнаружены!')
        return


# разбиение на сегменты с пробросом имени файла и времени сегмента
def segmention(x, sr, time_lim=30, file_name='No_name', time_start=0, time_end=30):

    # контайнер для результата сегментации
    res = []

    # разбиваем на сегменты по time_lim секунд
    step_seg = int(sr * time_lim)

    # проверка на моно
    # моно
    if len(x.shape) == 1:

        for n, i in enumerate(range(0, len(x), int(step_seg))):
            segment = x[i:i + step_seg]
            # проверка размера сегмента
            # если он меньше 1 секунды - не учитывать
            if len(segment) < sr * 1:
                break
            t0 = time_start + n * time_lim
            t1 = time_start + n * time_lim + time_lim
            if t1 > time_end:
                t1 = time_end
            res += [[segment, sr, file_name, t0, t1]]

        return res

    # многоканальная запись
    else:

        for n, i in enumerate(range(0, len(x[0]), int(step_seg))):
            segment = [[] for ch in range(len(x))]
            for ch in range(len(x)):
                segment[ch] = x[ch][i:i + step_seg]
            segment = np.array(segment)
            # проверка размера сегмента
            # если он меньше 1 секунды - не учитывать
            if len(segment[0]) < sr * 1:
                break
            t0 = time_start + n * time_lim
            t1 = time_start + n * time_lim + time_lim
            if t1 > time_end:
                t1 = time_end
            res += [[segment, sr, file_name, t0, t1]]

        return res


def generate_h_spectre(x):

    # Нормализованная матрица спектра.
    h = librosa.amplitude_to_db(abs(librosa.stft(x, n_fft=2048))) + 0.0
    (min_val, max_val) = (-50.0, 50.0)
    min_val = max(min_val, h.min())
    max_val = min(max_val, h.max())
    np.clip(h, min_val, max_val, out=h)
    h = (h - min_val) / (max_val - min_val)

    return h


def get_defects_dense(s):
    """
    Получение дефектов dense.
    """

    # загрузка настроек
    min_hz = 500
    max_hz = 900
    flag_channel = 2

    if flag_channel == 2:

        # обрабатываем каждый канал сегмента
        for n, x in enumerate(s[0]):

            # нормализованная спектрограмма
            xh = generate_h_spectre(x)

            # задаем процент погрешности
            percent = 3

            # выбираем рабочий диапозон частот
            xh = xh[min_hz:max_hz]

            # смещаем частоты вправо сортировкой
            xh.sort(axis=1)

            # условие нахождения звукового события
            # исследуем только последние проценты
            xht = xh.T[0:int(xh.shape[1] / 100 * percent)]
            xh = xht.T

            # проверсяем каждую строку окна на наличие частот
            fil = []
            flag = 0
            width = 4
            for nh, i in enumerate(xh):

                # если в строке есть частоты
                if i.max() != 0:

                    fil.append(1)

                # если в строке нет частот
                else:

                    fil.append(0)

                # если подряд есть частоты
                if nh > width - 1 and sum(fil[nh - width:nh]) == width:
                    # пердположительно это не то что мы ищим
                    flag = 1
                    break

            # если это то что мы искали и там встрачались частоты
            if flag == 0 and sum(fil) > 0:
                # условие выполненно, записать фреймы начала и конца
                # print(f'root path file: {s[2]}, channel number {n}, name of defect: dense,'
                #       f' time mark: {s[3]}, {s[4]}')

                return (f'root path file: {s[2]}, channel number {n}, name of defect: dense,'
                        f' time mark: {s[3]}, {s[4]}')

            # else:
            #     print(f'root path file: {s[2]}, channel number {n}, name of defect: dense,'
            #           f' time mark: {s[3]}, {s[4]} - не обнаружен!')


def run(dir_name):
    # чтение всех файлов из папки
    # получаем набор сегментов аудиоданных для анализа
    seg = read_file(dir_name)

    res = []
    # анализруем каждый сегмент
    # сначала проверяем есть ли сегменты
    if seg:

        # анализ сегмента
        # распаковываем все сегменты
        for i in seg:

            try:

                res.append(get_defects_dense(i))

            except Exception as e:
                print(i[2:])
                print(f"Error! {e}")

    return res

