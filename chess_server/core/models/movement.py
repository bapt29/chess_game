class Movement:

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

        if not value in range(-8, 9):
            raise ValueError('Value must be lower than 8 and greater or equal to 0')

        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        if not isinstance(value, int):
            raise TypeError('Type int is expected')

        if not value in range(-8, 9):
            raise ValueError('Value must be lower than 8 and greater or equal to 0')

        self.__y = value

    def __add__(self, other):
        if isinstance(other, Movement):
            return Movement(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if isinstance(other, Movement):
            return Movement(self.x - other.x, self.y - other.y)
        elif isinstance(other, tuple):
            return Movement(self.x - other[0], self.y - other[1])

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
