import ZODB
from ZODB import FileStorage, DB
import zc.zlibstorage

from chess_server.database.managers.user_manager import UserManager


class Database:

    def __init__(self, file_storage):
        self.storage = FileStorage.FileStorage(file_storage)
        self.compressed_storage = zc.zlibstorage.ZlibStorage(self.storage)
        self.db = DB(self.compressed_storage)
        self.connection = self.db.open()
        self.db_root = self.connection.root()

    def close(self):
        self.db.close()


if __name__ == "__main__":
    db = Database("/home/user/PycharmProjects/chess_game/chess_server/database/core/database.fs")
    user_manager = UserManager(db)

    for user in user_manager.users.values():
        print(user.username)

    print(user_manager.password_match("test", "bonjour"))

    db.close()
