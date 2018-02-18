class BaseHandler:

    def __init__(self, server):
        self.__server = server

    def on_read(self, conn, mask):
        raise NotImplementedError

    def handle(self, data):
        raise NotImplementedError
