class Player:

    def __init__(self, client_id, color):
        self.__client_id = client_id
        self.__color = color

    @property
    def client_id(self):
        return self.__client_id

    @client_id.setter
    def client_id(self, value):
        if not isinstance(value, int):
            raise TypeError('Client id must be int type')

        if not value > 0:
            raise ValueError('Client id must be greater than 0')

        self.__client_id = value

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        if not isinstance(value, int):
            raise TypeError('Color must be int type')

        if not value in range(2):
            raise ValueError('Color must be equal to 0 or 1')

        self.__color = value


if __name__ == "__main__":
    p = Player(12, )
