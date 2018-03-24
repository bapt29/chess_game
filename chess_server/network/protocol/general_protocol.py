import struct
from chess_server.network.utils.packet_formatter import PacketFormatter

GENERAL_TYPE = 0x02


class GeneralProtocol:

    @staticmethod
    def friend_list(friend_list):
        response_code = 0x01
        data = bytearray()

        for friend in friend_list:
            friend_id, friend_nickname, friend_connected = friend

            friend_nickname_data = PacketFormatter.from_string(friend[1])
            data = bytearray(struct.pack("Q{}s?".format(len(friend_nickname)),
                                         friend_id,
                                         friend_nickname_data,
                                         friend_connected))

        return PacketFormatter.format_response_packet(GENERAL_TYPE, response_code, data)
