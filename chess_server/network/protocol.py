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
    def game_information(game_id, color, opponent_nickname):
        opponent_nickname = bytes(opponent_nickname, "utf-8")
        opponent_nickname_len = len(opponent_nickname)
        code = 0x02

        return struct.pack("4B%ds" % opponent_nickname_len, code, game_id, color, opponent_nickname_len, opponent_nickname)

    @staticmethod
    def move_piece(piece_id, position):
        data = bytearray()
        code = 0x03

        position_field = position.x << 4 | position.y  # 1 octet: 4 bits X | 4 bits Y

        data.append(code)
        data.append(piece_id)
        data.append(position_field)

        return data

    @staticmethod
    def move_piece_error(piece_id, error_code, piece_id_collision=None):
        code = 0x04

        if error_code == 1:  # Unauthorized movement
            return struct.pack("3B", code, piece_id, error_code)
        elif error_code == 2 and piece_id_collision is not None:  # Collision
            return struct.pack("4B", code, piece_id, error_code, piece_id_collision)

    @staticmethod
    def pawn_promotion(pawn_id):
        code = 0x05

        return struct.pack("2B", code, pawn_id)

    @staticmethod
    def game_surrender(game_id):
        code = 0x06

        return struct.pack("2B", code, game_id)

    @staticmethod
    def message(nickname, message):
        code = 0x07

        full_message = ("%s: %s" % (nickname, message)).encode()
        full_message_length = len(full_message)

        return struct.pack("2B%ds" % full_message_length, code, full_message_length, full_message)

    @staticmethod
    def game_information_spectator(game_id, nickname_white, nickname_black, game_time, piece_list):
        packet = bytearray()

        packet.append(game_id)

        nicknames = "%s;%s" % (nickname_white, nickname_black)
        nicknames_length = len(nicknames)

        for c in nicknames:
            packet.append(ord(c))

        pieces = bytearray()
        piece_number = 0

        for position, piece in piece_list:
            piece_number += 1
            pieces.append(piece.id)
            pieces.append(piece.color)
            pieces.append(ord(str(piece)))

            position_field = position.x << 4 | position.y
            pieces.append(position_field)

        packet.append(piece_number)
        packet.extend(pieces)

        return packet
