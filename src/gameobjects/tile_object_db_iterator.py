class TileObjectDBIterator():
    def __init__(self, data):
        self.__data = data
        self.__index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.__index < len(self.__data):
            self.__index += 1
            return self.__data[self.__index - 1]
        else:
            raise StopIteration
