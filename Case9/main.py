from pytube import YouTube
import os
import ffmpeg
import PySimpleGUI as sg


# URL = 'https://www.youtube.com/watch?v=2A7JJX9tR9M'
# DOWNLOAD_DIRECTORY = 'E:/IT/git/load video from YouTube/'


# интерфейс
class GUI:

    def __init__(self):

        # параметры окна
        layout = [

            # первая строчка: текстовое описание + отступ, поле ввода текста + первичное значение, кнопка поиска папки
            [sg.Text('Укажите путь для скачивания:', size=(24, 1)), sg.InputText(''),
             sg.FolderBrowse('Выбрать папку')],

            # вторая строчка: текстовое описание + отступ, поле ввода текста + первичное значение
            [sg.Text('Введите URL адрес видео с YouTube: ', size=(29, 1)), sg.InputText(size=55)],

            # третья строчка: поле вывода информации
            [sg.Output(size=(88, 20))],

            # четвертая строчка: кнопки Submit и Cancel
            [sg.Submit('Скачать'), sg.Cancel('Выход')]
        ]

        # создание окна
        window = sg.Window('Скачать видео с YouTube', layout)

        # обработка действий в окне
        while True:  # The Event Loop
            event, values = window.read()
            # print(event, values) #debug
            if event in (None, 'Exit', 'Выход'):
                break
            if event == 'Скачать':
                if not values[0]:
                    print('Укажите путь для скачивания!')
                elif not values[1]:
                    print('Укажите URL адрес видео!')
                else:
                    try:
                        YT(values[0], values[1])
                    except Exception as e:
                        print('Ошибка! ', e, '\n')

        # закрыть окно
        window.close()


class YT:

    def __init__(self, dir,  url):

        if url.startswith('https://www.youtube.com/'):

            try:
                self.yt = YouTube(url)
            except Exception as e:
                print('Введен не корректный адрес! ')
                return

            # Имя канала
            self.channel_name = self.yt.vid_info['videoDetails']['author']

            # Название ролика
            self.video_name = self.yt.vid_info['videoDetails']['title']

            # имя конечного файла
            self.tru_name = os.path.join(dir, f'{self.channel_name} {self.video_name}.mp4')

            # загрузка видео
            self.download_video(dir)

        else:

            print('Введен не корректный адрес!')

    def download_video(self, dir):

        # проверка не существует ли уже файла с таким именем
        if os.path.isfile(self.tru_name):
            os.remove(self.tru_name)
            print('Обнаружен файл с таким же именем! Он был удален...')

        # просто скачать видео со звуком относительно высокого качества
        # yt.streams.get_highest_resolution().download(DOWNLOAD_DIRECTORY)

        # скачать видео высшего качества без звука
        print('Скачивание видео файла...')
        stream_video = self.yt.streams.filter(file_extension='mp4').order_by('resolution').desc().first()
        stream_video.download(dir, 'video.mp4')
        print('Временный файл video.mp4 загружен...')
        stream_video_name = os.path.join(dir, 'video.mp4')

        # если нет звука
        if not stream_video.is_progressive:
            print('Скачивание аудио файла...')
            stream_audio = self.yt.streams.get_audio_only()
            stream_audio.download(dir, 'audio.mp3')
            print('Временный файл audio.mp3 загружен...')
            stream_audio_name = os.path.join(dir, 'audio.mp3')
            print('Идет процесс рендеринга видео...')
            self.combine(stream_video_name, stream_audio_name)
            os.remove(stream_video_name)
            os.remove(stream_audio_name)
            print('Временные файлы video.mp4 и audio.mp3 удалены...')
            print('Готово!')
            print('Приятного просмотра!')

        # если есть звук
        else:
            os.rename(stream_video_name, self.tru_name)
            print('Временный вайл video.mp4 переименован...')
            print('Готово!')
            print('Приятного просмотра!')

    def combine(self, video, audio):
        video_stream = ffmpeg.input(video)
        audio_stream = ffmpeg.input(audio)
        ffmpeg.output(audio_stream, video_stream, self.tru_name).run()


if __name__ == '__main__':
    GUI()
