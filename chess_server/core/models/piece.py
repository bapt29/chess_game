class Piece(object):

    WHITE = 0
    BLACK = 1

    piece_id = 1

    def __init__(self, color):
        self.__id = Piece.piece_id
        Piece.piece_id += 1
        self.__color = color

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise TypeError

        self.__id = value

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        if not isinstance(value, int):
            raise TypeError

        if not value in range(2):
            raise ValueError

        self.__color = value

    def move(self, initial_position, new_position):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError
