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

    # user_manager.add_user("test", "coucou", "bonjour", "test@test.com")
    # user_manager.set_connected(1, False)
    # user_manager.set_banned(1, False)

    for user in user_manager.users.values():
        print(user.username)

    user_manager.password_match("test", "bonjour")

    db.close()
