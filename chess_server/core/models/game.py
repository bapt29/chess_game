import random, time

from chess_server.core.models.board import Board
from chess_server.core.models.player import Player


class Game:

    def __init__(self, client1, client2):
        self.__board = Board(self)
        self.__player1 = Player(client1.id, client1.nickname, 0)
        self.__player2 = Player(client2.id, client2.nickname, 0)
        self.__start_time = 0
        self.__turn = 0

    @property
    def turn(self):
        return self.__turn

    @property
    def board(self):
        return self.__board

    def coin_toss(self):
        self.__player1.color = random.randint(0, 1)
        self.__player2.color = 0 if self.__player1.color == 1 else 1

    def start(self):
        self.coin_toss()
        self.__start_time = int(time.time())
        self.__turn += 1
