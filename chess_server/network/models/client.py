from chess_server.database.models.user import User


class Client:

    def __init__(self, peer_name, socket):
        self.__user_id = None
        self.__peer_name = peer_name
        self.__socket = socket

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        if not isinstance(value, int):
            raise TypeError

        self.__user_id = value

    @property
    def peer_name(self):
        return self.__peer_name

    @peer_name.setter
    def peer_name(self, value):
        pass  # can't edit client peer name

    @property
    def socket(self):
        return self.__socket

    @socket.setter
    def socket(self, value):
        pass  # can't edit client socket
