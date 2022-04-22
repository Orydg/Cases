import os
import PySimpleGUI as sg


# интерфейс
class GUI:

    def __init__(self):

        # параметры окна
        layout = [

            # первая строчка: текстовое описание + отступ, поле ввода текста + первичное значение, кнопка поиска папки
            [sg.Text('Укажите папку:', size=(15, 1)), sg.InputText('Полный путь к папке'),
             sg.FolderBrowse('Выбрать папку')],

            # вторая строчка: текстовое описание + отступ, поле ввода текста + первичное значение
            [sg.Text('Введите текст: ', size=(15, 1)), sg.InputText('Введите искомую строку')],

            # третья строчка: поле вывода информации
            [sg.Output(size=(88, 20))],

            # четвертая строчка: кнопки Submit и Cancel
            [sg.Submit('Найти'), sg.Cancel('Выход')]
        ]

        # создание окна
        window = sg.Window('Поиск содержимого текстовых файлов', layout)

        # обработка действий в окне
        while True:  # The Event Loop
            event, values = window.read()
            # print(event, values) #debug
            if event in (None, 'Exit', 'Выход'):
                break
            if event == 'Найти':
                if not values.get('Browse'):
                    print('Укажите путь к папке!')
                else:
                    # print(values.get('Browse'))
                    # print(event)
                    try:
                        FindString(values[0], values[1])
                    except Exception as e:
                        print('Ошибка! ', e, '\n')

        # закрыть окно
        window.close()


class FindString:
    """
    Поиск строки в одном из файлов директории

    Параметры: Исследуемая директория, строка
    Параметры: Искомая строка, строка

    Возвращает местонахождение файла, содержащего искомую строку
    """

    def __init__(self, dir, find_text):

        self.Index = -1
        self.Flag = 0
        self.Dir = dir
        self.FindText = find_text
        self.find()
        if self.Flag == 0:
            print(f"Строка '{self.FindText}' не найдена!", '\n')

    # Вывод результирующей информации
    def print_info(self, file, content):

        self.Flag = 1
        print(f"строка '{self.FindText}' обнаружена в файле с расположением {file}")
        print('содержимое файла:')
        print(content, '\n')

    # чтение содержимого файла
    def find_string_in_file(self, file):

        # проверка формата файла
        if file.endswith(('.txt', '.docx')):

            # чтение содержимого
            try:
                f = open(file, 'r',
                         encoding='utf-8',
                         errors="ignore"
                         )
                content = f.read()
                f.close()

                # поиск строки
                self.Index = content.find(self.FindText)
                if self.Index != -1:
                    self.print_info(file, content)

            except Exception as e:
                print(f"Ошибка! {e}")
                print(f"В файле '{file}' обнаружены неизвестные символы!", '\n')

    # чтение содержимого директории
    def find(self):

        # чтение файлов директории
        for root, dirs, files in os.walk(self.Dir):
            for name in files:

                self.find_string_in_file(os.path.join(root, name))


if __name__ == '__main__':

    GUI()
