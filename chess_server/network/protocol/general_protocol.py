import struct
import pickle
import zlib
from chess_server.network.utils.packet_formatter import PacketFormatter

GENERAL_TYPE = 0x02


class GeneralProtocol:

    request_codes = {"friend_list": 0x01, "game_list": 0x02, "create_game": 0x03}

    @staticmethod
    def invalid_packet():
        code = 0x01

        return PacketFormatter.format_response_packet(GENERAL_TYPE, code)

    @staticmethod
    def friend_list(friend_list):
        code = 0x02
        data = bytearray(zlib.compress(pickle.dumps(friend_list)))

        return PacketFormatter.format_response_packet(GENERAL_TYPE, code, data)

    @staticmethod
    def friend_list_request(data):
        online = data[0]

        return online

    @staticmethod
    def game_list(game_list):
        code = 0x03
        data = bytearray(zlib.compress(pickle.dumps(game_list)))

        return PacketFormatter.format_response_packet(GENERAL_TYPE, code, data)

    @staticmethod
    def game_list_request(data):
        in_progress = data[0]
        nickname = None

        if data[1] > 0:
            nickname = PacketFormatter.to_string(data[1:])

        return in_progress, nickname

    @staticmethod
    def connection_signal(user_id):
        code = 0x04
        data = bytearray(struct.pack("Q", user_id))

        return PacketFormatter.format_response_packet(GENERAL_TYPE, code, data)

    @staticmethod
    def disconnection_signal(user_id):
        code = 0x05
        data = bytearray(struct.pack("Q", user_id))

        return PacketFormatter.format_response_packet(GENERAL_TYPE, code, data)

    @staticmethod
    def user_not_found():
        code = 0x06

        return PacketFormatter.format_response_packet(GENERAL_TYPE, code)

    @staticmethod
    def create_game_request(data):
        # TODO: game_name?
        password = PacketFormatter.to_string(data)

        return password

    @staticmethod
    def private_message_request(data):
        nickname, message = PacketFormatter.to_string(data, 2)

        return nickname, message
