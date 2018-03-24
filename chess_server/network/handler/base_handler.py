from chess_server.database.managers.user_manager import UserManager
from chess_server.database.managers.game_manager import GameManager


class BaseHandler(object):

    def __init__(self, server):
        self.server = server

        self.user_manager = UserManager(self.server.db.db_root)
        self.game_manager = GameManager(self.server.db.db_root)

    def on_read(self, conn, mask):
        try:
            data = conn.recv(1024)

            if data:
                self.handle(data, conn)
            else:
                self.server.close_connection(conn)
        except ConnectionResetError:
            self.server.close_connection(conn)

    def handle(self, data, conn):
        raise NotImplementedError
