from chess_server.network.handler.base_handler import BaseHandler

from chess_server.network.protocol.general_protocol import GeneralProtocol, GENERAL_TYPE
from chess_server.network.utils.packet_formatter import PacketFormatter
from chess_server.error.network_error import *


class GeneralHandler(BaseHandler):

    def handle(self, data, conn):
        client = self.server.client_list[conn.fileno()]
        user = self.user_manager.get_user_by_id(client.user_id)

        packet_type, packet_code, packet_data = PacketFormatter.process_packet(data)

        if packet_type == GENERAL_TYPE:
            if packet_code == GeneralProtocol.request_codes["friend_list"]:
                online_option = GeneralProtocol.friend_list_request(packet_data)
                friend_list = list()

                if online_option == 0x00:  # Offline users
                    friend_list = self.user_manager.get_friend_list(user.username, connected=False)
                elif online_option == 0x01:  # Online users
                    friend_list = self.user_manager.get_friend_list(user.username, connected=True)
                elif online_option == 0x02:  # Both
                    self.user_manager.get_friend_list(user.username)

                conn.send(GeneralProtocol.friend_list(friend_list))
            elif packet_code == GeneralProtocol.request_codes["game_list_progress"]:
                try:
                    in_progress, nickname = GeneralProtocol.game_list_request(packet_data)
                except InvalidPacket:
                    conn.send(GeneralProtocol.invalid_packet())
                else:
                    self.game_manager.game_list(in_progress, nickname)
            elif packet_code == GeneralProtocol.request_codes["create_game"]:
                try:
                    password = GeneralProtocol.create_game_request(packet_data)
                except InvalidPacket:
                    conn.send(GeneralProtocol.invalid_packet())
                else:


            else:
                conn.send(GeneralProtocol.invalid_packet())
