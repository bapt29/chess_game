from chess_server.network.protocol.authentication_protocol import AuthenticationProtocol
from chess_server.network.protocol.registration_protocol import RegistrationProtocol
from chess_server.network.protocol.game_protocol import GameProtocol


class DataProcessor:

    def __init__(self):
        self.__authentication_protocol = AuthenticationProtocol
        self.__registration_protocol = RegistrationProtocol
        self.__game_protocol = GameProtocol

        self.__action_authentication_dict = {1: "login", 2: "logout"}
        self.__action_registration_dict = {1: "register"}
        self.__action_game_dict = {1: "move_piece",
                                   2: "pawn_promotion_choice",
                                   3: "surrender"
                                   4: "send_message"
                                   }


    @staticmethod
    def process(packet):
        type = packet[0]
        action = packet[1]
        data = packet[2:]

    def post_process(self, type, action, data):
        if type == 1:
            getattr(self.__authentication_protocol, self.__action_authentication_dict.get(action))(data)
        elif type == 2:
            getattr(self.__authentication_protocol, self.__action_authentication_dict.get(action))(data)
        elif type == 3:
            getattr(self.__authentication_protocol, self.__action_authentication_dict.get(action))(data)
