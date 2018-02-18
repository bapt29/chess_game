class BaseHandler(object):

    def __init__(self, server):
        self.__server = server

    def on_read(self, conn, mask):
        try:
            data = conn.recv(1000)

            if data:
                self.handle(data)
            else:
                self.__server.close_connection(conn)
        except ConnectionResetError:
            self.__server.close_connection(conn)

    def handle(self, data):
        raise NotImplementedError
