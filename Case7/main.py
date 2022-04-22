import xlrd3 as xlrd

FILE = 'test.xls'


def parsing(file):
    book = xlrd.open_workbook(file)
    sh = book.sheet_by_index(0)
    for row_nums in range(sh.nrows):
        for col_nums in range(sh.ncols):
            print(sh.cell_value(rowx=row_nums, colx=col_nums))


def do(file):
    articles = []
    exp = []
    book = xlrd.open_workbook(file)
    sh = book.sheet_by_index(0)
    # цикл перебирает все строки таблицы
    for row_nums in range(sh.nrows):
        # показать значение каждой ячейки таблицы
        # for col_nums in range(sh.ncols):
            # print(sh.cell_value(rowx=row_nums, colx=col_nums))
        row = sh.row_values(row_nums)
        if row[1]:
            # проверка на то что элемент в ячейке row[1] является числом с точкой
            if isinstance(row[1], float):
                articles.append(row[0])
                exp.append(row[1])

    print_res(articles, exp)


def get_extreme_key(array, compare):
    extreme_index = 0
    extreme = array[extreme_index]
    i = 1
    while i < len(array):
        if compare(array[i], extreme) == array[i]:
            extreme = array[i]
            extreme_index = i
        i += 1
    return extreme_index


def print_res(articles, exp):
    index_min = get_extreme_key(exp, min)
    index_max = get_extreme_key(exp, max)
    print(f'Самый дорогой продукт: {articles[index_max]}, с ценой {exp[index_max]} руб.')
    print(f'Самый дешевый продукт: {articles[index_min]}, с ценой {exp[index_min]} руб.')


if __name__ == '__main__':

    do(FILE)
