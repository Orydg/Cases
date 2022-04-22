import os
from PIL import Image


DIRECTORY = input("Введите путь к папке с изображениями: ")
FROM_EXT = '.' + input("Введите исходный формат изменяемых изображений: ")
TO_EXT = '.' + input("Введите конечный формат изменяемых изображений: ")
MAX_SIZE = (1024, 1024)


# чтение содержимого директории
def walk(directory):
    for root, dirs, files in os.walk(directory):
        for name in files:
            conversion(os.path.join(root, name))


# изменение максимального размера изображения
def resize(file):
    im = Image.open(file)
    im.thumbnail(MAX_SIZE, Image.ANTIALIAS)
    im.save(file)


# изменение формата файлов изображений
def conversion(file):
    resize(file)
    name, ext = os.path.splitext(file)
    if ext == FROM_EXT:
        im = Image.open(file)
        im.save(name + TO_EXT)
        os.remove(file)


if __name__ == '__main__':
    walk(DIRECTORY)
