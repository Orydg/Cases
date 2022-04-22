class Primes:
    """
    Итератор простых чисел

    """

    def __init__(self, n):
        self.__count = 0
        self.__num = n

    def __iter__(self):
        self.__count = 0
        return self

    def __next__(self):
        self.__count += 1
        if self.__count > self.__num:
            raise StopIteration()
        if self.__count > 3:
            if self.__count % 2 == 0 or self.__count % 3 == 0 or self.__count % 5 == 0:
                self.__next__()

            for i in range(self.__count, self.__num + 1, 2):
                for j in range(2, self.__count):
                    if i % j == 0:
                        self.__next__()
                return i

        return self.__count


prime_nums = Primes(50)

for i_elem in prime_nums:
    print(i_elem, end=' ')
