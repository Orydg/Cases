import os
import re
import pymorphy2

find_directory = 'test'
morph = pymorphy2.MorphAnalyzer()


# как часто встрчается это слово в текстовом файле
def analysis(content):
    frequency = {}
    matches = re.findall(r'\b[а-я]+\b', content, re.IGNORECASE)
    for word in matches:
        word = word.lower()
        word = morph.parse(word)[0].normal_form
        count = frequency.get(word, 0)
        frequency[word] = count + 1
    return frequency


def sort(frequency):
    sorted_dict = {}
    sorted_keys = sorted(frequency, key=frequency.get, reverse=True)
    for key in sorted_keys:
        sorted_dict[key] = frequency[key]
    return sorted_dict


def print_res(frequency):
    frequency = sort(frequency)
    for word in frequency:
        print(word, frequency[word])


def walk(directory):
    frequency = {}
    for root, dirs, files in os.walk(directory):
        for name in files:
            file = os.path.join(root, name)
            f = open(file, 'r', encoding='utf-8')
            new_frequency = analysis(f.read())
            f.close()
            for word in new_frequency:
                count = frequency.get(word, 0)
                frequency[word] = count + new_frequency.get(word)
    print_res(frequency)


if __name__ == '__main__':
    walk(find_directory)
