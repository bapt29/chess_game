import time
import transaction
from BTrees.LOBTree import LOBTree  # 64-bit integer as key / value: Object

from chess_server.database.models.game import Game
from chess_server.database.models.user import User
from chess_server.database.managers.user_manager import UserManager
from chess_server.error.database_error import *


class GameManager:

    def __init__(self, database):
        self.db = database

        if "games" not in self.db.db_root:
            self.db.db_root["games"] = LOBTree()

        self.games = self.db.db_root["games"]
        self.user_manager = UserManager(database)

    def get_game(self, game_id):
        if game_id not in self.games.keys():
            raise GameNotFound

        return self.games[game_id]

    def game_list(self, in_progress=None, username=None):
        games_list = list()

        if in_progress is not None:
            if not isinstance(in_progress, bool):
                raise TypeError

            for game_id, game in self.games.items():
                if game.in_progress == in_progress:
                    try:
                        user1 = self.user_manager.get_user(game.player1_username)
                    except UserNotFound:
                        user1 = None

                    try:
                        user2 = self.user_manager.get_user(game.player2_username)
                    except UserNotFound:
                        user2 = None

                    games_list.append((game_id,
                                       user1.nickname,
                                       user2.nickname,
                                       game.start_time,
                                       game.end_time,
                                       game.in_progress))
        elif username is not None:
            if not isinstance(username, str):
                raise TypeError

            for game_id, game in self.games.items():
                if username in (game.player1_username, game.player2_username):
                    try:
                        user1 = self.user_manager.get_user(game.player1_username)
                    except UserNotFound:
                        user1 = None

                    try:
                        user2 = self.user_manager.get_user(game.player2_username)
                    except UserNotFound:
                        user2 = None

                    games_list.append((game_id,
                                       user1.nickname,
                                       user2.nickname,
                                       game.start_time,
                                       game.end_time,
                                       game.in_progress))

        else:
            for game_id, game in self.games.items():
                try:
                    user1 = self.user_manager.get_user(game.player1_username)
                except UserNotFound:
                    user1 = None

                try:
                    user2 = self.user_manager.get_user(game.player2_username)
                except UserNotFound:
                    user2 = None

                games_list.append((game_id,
                                   user1.nickname,
                                   user2.nickname,
                                   game.start_time,
                                   game.end_time,
                                   game.in_progress))

        return games_list

    def add_game(self, player1_username, player2_username):
        self.check_player_already_in_game(player1_username)
        self.check_player_already_in_game(player2_username)

        min_key = 1
        games_id = list(self.games.keys())

        if len(games_id) > 0:
            min_key = min(games_id)

        self.games[min_key] = Game(player1_username, player2_username)

        transaction.commit()

    def delete_game(self, game_id):
        self.get_game(game_id)
        del self.games[game_id]

        transaction.commit()

    def check_player_already_in_game(self, username):
        for game in self.games.values():
            if game.in_progress:
                if username in (game.player1_username, game.player2_username):
                    raise PlayerAlreadyInGame

    def set_end_time(self, game_id):
        game = self.get_game(game_id)
        game.end_time = int(time.time())

        transaction.commit()

    def set_in_progress(self, game_id, state):
        game = self.get_game(game_id)

        if state and game.in_progress:
            raise GameAlreadyInProgress

        if not state and not game.in_progress:
            raise GameAlreadyOver

        if not state:
            self.set_end_time(game_id)

        game.in_progress = state
        transaction.commit()

    def set_password(self, game_id, password):
        game = self.get_game(game_id)
        game.password = password

        transaction.commit()
