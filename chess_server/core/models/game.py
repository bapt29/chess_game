import random

from chess_server.core.models.board import Board
from chess_server.core.models.player import Player


class Game:

    def __init__(self, client1, client2):
        self.__board = Board()
        self.__player1 = Player(client1.id, client1.nickname, 0)
        self.__player2 = Player(client2.id, client2.nickname, 0)

    def coin_toss(self):
        self.__player1.color = random.randint(0, 1)
        self.__player2.color = 0 if self.__player1.color == 1 else 1

    def start(self):
        self.coin_toss()
