import time
import persistent


class Game(persistent.Persistent):

    def __init__(self, player1_username, player2_username):
        self.player1_username = player1_username
        self.player2_username = player2_username

        self.start_time = int(time.time())
        self.end_time = None
        self.in_progress = True
