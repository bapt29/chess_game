class Position:

    def __init__(self, x, y):
        self.__x = None
        self.__y = None
        self.x = x
        self.y = y

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        if not isinstance(value, int):
            raise TypeError('Type int is expected')

        if not value in range(8):
            raise ValueError('Value must be lower than 8 and greater or equal to 0')

        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        if not isinstance(value, int):
            raise TypeError('Type int is expected')

        if not value in range(8):
            raise ValueError('Value must be lower than 8 and greater or equal to 0')

        self.__y = value

    def __add__(self, other):
        Position.error_handling(other)

        if isinstance(other, Position):
            return Position(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple):
            return Position(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        Position.error_handling(other)

        if isinstance(other, Position):
            return Position(self.x - other.x, self.y - other.y)
        elif isinstance(other, tuple):
            return Position(self.x - other[0], self.y - other[1])

    def __iadd__(self, other):
        Position.error_handling(other)

        if isinstance(other, Position):
            self.x += other.x
            self.y += other.y
        elif isinstance(other, tuple):
            self.x += other[0]
            self.y += other[1]

        return self

    def __isub__(self, other):
        Position.error_handling(other)

        if isinstance(other, Position):
            self.x -= other.x
            self.y -= other.y
        elif isinstance(other, tuple):
            self.x -= other[0]
            self.y -= other[1]

        return self

    def __eq__(self, other):
        Position.error_handling(other)

        if isinstance(other, Position):
            return self.__dict__ == other.__dict__
        elif isinstance(other, tuple):
            return self.__x == other[0] and self.__y == other[1]

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.__x, self.__y))

    def __abs__(self):
        self.__x = abs(self.__x)
        self.__y = abs(self.__y)

        return self

    @staticmethod
    def error_handling(object):

        if not isinstance(object, (Position, tuple)):
            raise TypeError

        if isinstance(object, tuple):
            if not len(object) == 2:
                raise IndexError

            if not isinstance(object[0], int) or not isinstance(object[1], int):
                raise TypeError

            if not object[0] in range(8) or not object[1] in range(8):
                raise ValueError

    @staticmethod
    def position_delta(first_position, second_position):
        delta_x = abs(first_position.x - second_position.x)
        delta_y = abs(first_position.y - second_position.y)

        return Position(delta_x, delta_y)


if __name__ == "__main__":
    pos1 = Position(1, 1)
    pos2 = Position(1, 2)
    pos3 = (1, 1)

    print(pos1 == pos2)
    print(pos1 == pos3)
