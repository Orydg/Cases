"""
Задание: написать метод, который анализируе вхождение одной строки в другую и выдает True,
если одна строка целиком входит в другую, иначе - False.

"""


def occurrence_of_single_string(str1, str2):
    """
    The function finds the full occurrence of one string in another.

    :param str1: A text string, where words are separated by spaces.
    :param str2: A text string, where words are separated by spaces.
    :return:
        True - One line is completely included in the other.
        False - Not.

    """

    assert isinstance(str1, str) and isinstance(str2, str), f"Error: Incorrect data type entered. " \
                                                            f"Your type is: str1 - {type(str1)}, str2 - {type(str2)}." \
                                                            f"The desired type is a string."

    str1, str2 = str1.lower(), str2.lower()
    return all([s in str2 for s in str1.split(' ')]) or all([s in str1 for s in str2.split(' ')])


if __name__ == '__main__':
    assert occurrence_of_single_string('Я люблю есть', 'Люблю')
    assert not occurrence_of_single_string('Я люблю есть', 'Лю ec')
    assert not occurrence_of_single_string('Я люблю есть', 'Люблю спать')
