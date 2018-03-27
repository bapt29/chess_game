import selectors
import logging
import _thread
from chess_server.network.handler.base_handler import BaseHandler

from chess_server.network.protocol.authentication_protocol import AuthenticationProtocol, AUTHENTICATION_TYPE
from chess_server.network.protocol.general_protocol import GeneralProtocol
from chess_server.network.utils.packet_formatter import PacketFormatter

from chess_server.error.database_error import *


logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')


class AuthenticationHandler(BaseHandler):

    def handle(self, data, conn):
        packet_data = bytearray(data)
        packet_type, packet_code = PacketFormatter.process_packet(packet_data)

        if packet_type == AUTHENTICATION_TYPE:
            if packet_code == AuthenticationProtocol.request_codes["authentication"]:
                username, password = AuthenticationProtocol.on_authentication(packet_data)

                logging.info(packet_data)

                if self.connect(username, password, conn):
                    self.server.selector.unregister(conn)
                    self.server.selector.register(fileobj=conn,
                                                  events=selectors.EVENT_READ,
                                                  data=self.server.general_handler.on_read)

                    _thread.start_new_thread(self.send_connection_signal,
                                             self.server.client_list[conn.fileno()].user_id)

    def connect(self, username, password, conn):
        try:
            self.user_manager.authentication(username, password)
        except (UserNotFound, UserBadPassword):
            conn.send(AuthenticationProtocol.bad_credentials())
            return False
        except UserAlreadyConnected:
            conn.send(AuthenticationProtocol.already_connected())
            return False
        except UserBanned:
            conn.send(AuthenticationProtocol.banned())
            return False
        else:
            conn.send(AuthenticationProtocol.success(self.user_manager.get_user(username).nickname))

            self.user_manager.set_connected(username, True)
            user_id = self.user_manager.get_user_id(username)
            self.server.client_list[conn.fileno()].user_id = user_id

            return True

    def send_connection_signal(self, user_id):
        for client in self.server.client_list.values():
            if client.user_id is not None:
                client_user = self.user_manager.get_user_by_id(client.user_id)

                if user_id in client_user.friend_list:
                    client.socket.send(GeneralProtocol.connection_signal(user_id))

    def send_disconnection_signal(self, user_id):
        for client in self.server.client_list.values():
            if client.user_id is not None:
                client_user = self.user_manager.get_user_by_id(client.user_id)

                if user_id in client_user.friend_list:
                    client.socket.send(GeneralProtocol.disconnection_signal(user_id))
