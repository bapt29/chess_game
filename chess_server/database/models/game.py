import persistent


class Game(persistent.Persistent):

    def __init__(self, player1_username, player2_username):
        self.player1_username = player1_username
        self.player2_username = player2_username

        self.start_time = None
        self.end_time = None
        self.password = None
        self.in_progress = True
