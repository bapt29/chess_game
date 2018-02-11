import struct

from chess_server.network.utils.packet_formatter import PacketFormatter


class Protocol:

    @staticmethod
    def authentication_response(success, nickname=None):
        code = 0x01

        if success:
            packet = bytearray(struct.pack("B?", code, success))
            packet.extend(PacketFormatter.from_string(nickname))
        else:
            packet = bytearray(struct.pack("?", success))

        return packet

    @staticmethod
    def in_queue(place):
        code = 0x02
        return bytearray(struct.pack("2B", code, place))

    @staticmethod
    def game_information(game_id, color, opponent_nickname):
        code = 0x03

        packet = bytearray(struct.pack("3B", code, game_id, color))
        packet.extend(PacketFormatter.from_string(opponent_nickname))

        return packet

    @staticmethod
    def your_turn(remaining_time):
        code = 0x04
        return bytearray(struct.pack("BH", code, remaining_time))

    @staticmethod
    def time_left_warn(time_left):
        code = 0x05
        return bytearray(struct.pack("2B", code, time_left))

    @staticmethod
    def move_piece(piece_id, position):
        code = 0x06

        packet = bytearray()
        packet.append(code)
        packet.append(piece_id)
        packet.append(PacketFormatter.from_position(position))

        return packet

    @staticmethod
    def move_piece_error(piece_id, error_code, piece_id_collision=None):
        code = 0x07

        if error_code == 0x01:  # Unauthorized movement
            return bytearray(struct.pack("3B", code, piece_id, error_code))
        elif error_code == 0x02 and piece_id_collision is not None:  # Collision
            return bytearray(struct.pack("4B", code, piece_id, error_code, piece_id_collision))

    @staticmethod
    def king_in_check(king_id, piece_id_list):
        code = 0x08

        packet = bytearray()
        packet.append(code)
        packet.append(king_id)
        packet.extend(PacketFormatter.from_list(piece_id_list))

        return packet

    @staticmethod
    def pawn_promotion(pawn_id):
        code = 0x09
        return struct.pack("2B", code, pawn_id)

    @staticmethod
    def game_over(result):
        code = 0x0A
        return bytearray(struct.pack("B?", code, result))

    @staticmethod
    def game_over_spectator(winner_nickname):
        code = 0x0B

        packet = bytearray()
        packet.append(code)
        packet.extend(PacketFormatter.from_string(winner_nickname))

        return packet

    @staticmethod
    def message(message):
        code = 0x0C

        packet = bytearray().append(code)
        packet.extend(PacketFormatter.from_string(message))

        return packet

    @staticmethod
    def game_information_spectator(game_id, nickname_white, nickname_black, game_time, piece_list):
        code = 0x0D

        packet = bytearray()
        packet.append(code)
        packet.append(game_id)
        packet.append(PacketFormatter.from_seconds(game_time))
        packet.extend(PacketFormatter.from_string(nickname_white))
        packet.extend(PacketFormatter.from_string(nickname_black))
        packet.extend(PacketFormatter.from_piece_list(piece_list))

        return packet
