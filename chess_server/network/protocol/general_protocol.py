import struct
import pickle
import zlib
from chess_server.network.utils.packet_formatter import PacketFormatter

GENERAL_TYPE = 0x02


class GeneralProtocol:

    request_codes = {"friend_list": 0x01, "game_list": 0x02}

    @staticmethod
    def friend_list(friend_list):
        code = 0x01
        data = bytearray(zlib.compress(pickle.dumps(friend_list)))

        return PacketFormatter.format_response_packet(GENERAL_TYPE, code, data)

    @staticmethod
    def friend_list_request(data):
        online = data[0]

        return online

    @staticmethod
    def game_list(game_list):
        code = 0x02
        data = bytearray(zlib.compress(pickle.dumps(game_list)))

        return PacketFormatter.format_response_packet(GENERAL_TYPE, code, data)

    @staticmethod
    def game_list_request(data):
        option = data[0]
        parameter = data[1]

        return option, parameter

    @staticmethod
    def connection_signal(user_id):
        code = 0x03
        data = bytearray(struct.pack("Q", user_id))

        return PacketFormatter.format_response_packet(GENERAL_TYPE, code, data)

    @staticmethod
    def disconnection_signal(user_id):
        code = 0x04
        data = bytearray(struct.pack("Q", user_id))

        return PacketFormatter.format_response_packet(GENERAL_TYPE, code, data)
