class Client:

    MAX_ID = 1
    AVAILABLE_ID_LIST = []

    def __init__(self, socket):
        if len(Client.AVAILABLE_ID_LIST) > 0:
            id = min(Client.AVAILABLE_ID_LIST)
            Client.AVAILABLE_ID_LIST.remove(id)
        else:
            id = Client.MAX_ID
            Client.MAX_ID += 1

        self.__id = id
        self.__user_id = None
        self.__nickname = None
        self.__socket = socket
        self.__is_authenticated = False

    def __del__(self):
        Client.AVAILABLE_ID_LIST.append(self.__id)

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        pass  # can't edit client id

    @property
    def user_id(self):
        return self.__id

    @user_id.setter
    def user_id(self, value):
        if isinstance(value, int) and value > 0:
            self.__user_id = value

    @property
    def nickname(self):
        return self.__nickname

    @nickname.setter
    def nickname(self, value):
        if isinstance(value, str) and len(value) < 32:
            self.__nickname = value

    @property
    def socket(self):
        return self.__socket

    @socket.setter
    def socket(self, value):
        pass  # can't edit client socket

    @property
    def is_authenticated(self):
        return self.__is_authenticated

    @is_authenticated.setter
    def is_authenticated(self, value):
        if isinstance(value, bool):
            self.__is_authenticated = value
