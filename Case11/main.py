from gtts import gTTS
import pdfplumber
from pathlib import Path


def pdf_to_mp3(file_path='test.pdf', lang='en', pp=None):
    """

    Parameters:
    file_path - путь к файлу.
    lang - указатель языка, на котором написан файл. Например: 'ru' - русский, 'en' - английский.
    pp - номера страниц, с какой по какую страницу читать.

    Result:
    аудиозапись в формате mp3 на основе текста в исходном pdf файле.

    """

    # проверяем наличие файла
    if Path(file_path).is_file() and Path(file_path).suffix in ['.pdf', '.PDF']:
        print(f'Файл {file_path} открыт!')

        with pdfplumber.PDF(open(file=file_path, mode='rb')) as pdf:
            pp = pp or (1, len(pdf.pages)+1)
            print(f'Производится чтение с {pp[0]} по {pp[1]} станицу.')
            pages = [page.extract_text() for n, page in enumerate(pdf.pages, 1) if pp[0] <= n <= pp[1]]
            text = ''.join(pages)
            text = text.replace('\n', ' ')
            audio = gTTS(text=text, lang=lang)
            file_name = Path(file_path).stem
            audio.save(f'{file_name}.mp3')

        return f'Файл {file_name}.mp3 записан!'
    else:
        return "Файл не найден!"


def main():
    print(pdf_to_mp3(file_path='test.pdf', pp=(19, 20)))


if __name__ == '__main__':

    main()
