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
        packet_type, packet_code, packet_data = PacketFormatter.process_packet(data)

        if packet_type == AUTHENTICATION_TYPE:
            if packet_code == AuthenticationProtocol.request_codes["authentication"]:
                username, password = AuthenticationProtocol.on_authentication(packet_data)

                logging.info(packet_data)
                logging.info("Username: {} ; Password: {}".format(username, password))

                if self.connect(username, password, conn):
                    self.server.selector.unregister(conn)
                    self.server.selector.register(fileobj=conn,
                                                  events=selectors.EVENT_READ,
                                                  data=self.server.general_handler.on_read)

                    arguments = (self.server.client_list[conn.fileno()].user_id, )  # Tuple needed
                    _thread.start_new_thread(self.send_connection_signal, arguments)

    def connect(self, username, password, conn):
        try:
            self.user_manager.authentication(username, password)
        except (UserNotFound, UserBadPassword):
            conn.send(AuthenticationProtocol.bad_credentials())
            self.server.close_connection(conn)

            return False
        except UserAlreadyConnected:
            conn.send(AuthenticationProtocol.already_connected())
            self.server.close_connection(conn)

            return False
        except UserBanned:
            conn.send(AuthenticationProtocol.banned())
            self.server.close_connection(conn)

            return False
        else:
            conn.send(AuthenticationProtocol.success(self.user_manager.get_user(username).nickname))

            user_id = self.user_manager.get_user_id(username)
            self.user_manager.set_connected(user_id, True)
            self.server.client_list[conn.fileno()].user_id = user_id

            return True

    def send_connection_signal(self, user_id):
        client_dict = self.server.get_client_dict()

        for client in client_dict.values():
            if client.user_id is not None:
                client_user = self.user_manager.get_user_by_id(client.user_id)

                if user_id in client_user.friend_list:
                    client.socket.send(GeneralProtocol.connection_signal(user_id))

    def send_disconnection_signal(self, user_id):
        client_dict = self.server.get_client_dict()

        for client in client_dict.values():
            if client.user_id is not None:
                client_user = self.user_manager.get_user_by_id(client.user_id)

                if user_id in client_user.friend_list:
                    client.socket.send(GeneralProtocol.disconnection_signal(user_id))

    def client_disconnected(self, user_id):
        self.user_manager.set_connected(user_id, False)
