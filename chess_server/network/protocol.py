import struct


class Protocol:

    @staticmethod
    def authentication_response(success, nickname=None):
        nickname = bytes(nickname, "utf-8")
        nickname_length = len(nickname)
        code = 0x01

        if success:
            return struct.pack("B?B%ds" % nickname_length, code, success, nickname_length, nickname)

        return struct.pack("?", success)

    @staticmethod
    def send_game_information(game_id, color, opponent_nickname):
        opponent_nickname = bytes(opponent_nickname, "utf-8")
        opponent_nickname_len = len(opponent_nickname)
        code = 0x02

        return struct.pack("4B%ds" % opponent_nickname_len, code, game_id, color, opponent_nickname_len, opponent_nickname)