from chess_server.core.models.position import Position


class Movement:

    def __init__(self, start_position, end_position):
        self.__x = None
        self.__y = None
        self.get_movement(start_position, end_position)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        if not isinstance(value, int):
            raise TypeError('Type int is expected')

        if not value in range(-8, 9):
            raise ValueError('Value must be lower or equal to 8 and greater or equal to -8')

        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        if not isinstance(value, int):
            raise TypeError('Type int is expected')

        if not value in range(-8, 9):
            raise ValueError('Value must be lower or equal to 8 and greater or equal to -8')

        self.__y = value

    def __add__(self, other):
        if isinstance(other, Movement):
            return Movement(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if isinstance(other, Movement):
            return Movement(self.x - other.x, self.y - other.y)

    def __iadd__(self, other):
        if isinstance(other, Movement):
            self.x += other.x
            self.y += other.y

        return self

    def __isub__(self, other):
        if isinstance(other, Movement):
            self.x -= other.x
            self.y -= other.y

        return self

    def __abs__(self):
        self.__x = abs(self.__x)
        self.__y = abs(self.__y)

        return self

    def get_movement(self, start_position, end_position):
        if not isinstance(start_position, Position) or not isinstance(end_position, Position):
            raise TypeError

        self.x = end_position.x - start_position.x
        self.y = end_position.y - start_position.y