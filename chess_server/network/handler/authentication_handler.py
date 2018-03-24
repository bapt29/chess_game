import selectors
from chess_server.network.handler.base_handler import BaseHandler

from chess_server.network.protocol.authentication_protocol import AuthenticationProtocol
from chess_server.network.protocol.general_protocol import GeneralProtocol
from chess_server.network.utils.packet_formatter import PacketFormatter

from chess_server.error.database_error import *


class AuthenticationHandler(BaseHandler):

    def handle(self, data, conn):
        packet_type, packet_code, packet_data = PacketFormatter.process_packet(data)

        if packet_type == 0x01:  # Authentication packet type
            if packet_code == 0x01:
                username, password = AuthenticationProtocol.on_authentication(data)

                if self.connect(username, password, conn):
                    self.server.selector.unregister(conn)
                    self.server.selector.register(fileobj=conn,
                                                  events=selectors.EVENT_READ,
                                                  data=self.server.general_handler.on_read)

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
            return True
