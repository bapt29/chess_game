import struct
from chess_server.network.utils.packet_formatter import PacketFormatter

GENERAL_TYPE = 0x02


class GeneralProtocol:

    request_codes = {"friend_list": 0x01, "game_list": 0x02}

    @staticmethod
    def friend_list(friend_list):
        code = 0x01
        data = bytearray()

        for friend in friend_list:
            friend_id, friend_nickname, friend_connected = friend

            friend_nickname_data = PacketFormatter.from_string(friend[1])
            data.extend(bytearray(struct.pack("Q{}s?".format(len(friend_nickname)),
                                              friend_id,
                                              friend_nickname_data,
                                              friend_connected)))

        return PacketFormatter.format_response_packet(GENERAL_TYPE, code, data)

    @staticmethod
    def friend_list_request(data):
        online = ord(data[0])

        return online

    @staticmethod
    def game_list(game_list):
        code = 0x02
        data = bytearray()

        for game in game_list:
            game_id, player1_nickname, player2_nickname, start_time, end_time, in_progress = game

            players = PacketFormatter.from_string(player1_nickname).extend(PacketFormatter.from_string(player2_nickname))
            data.extend(bytearray(struct.pack("Q{}s2I?".format(len(players)),
                                              game_id,
                                              players,
                                              start_time,
                                              end_time,
                                              in_progress)))

        return PacketFormatter.format_response_packet(GENERAL_TYPE, code, data)

    @staticmethod
    def game_list_request(data):
        pass

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
