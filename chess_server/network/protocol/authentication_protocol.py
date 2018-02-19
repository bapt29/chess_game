from chess_server.network.utils.packet_formatter import PacketFormatter

AUTHENTICATION_TYPE = 0x01


class AuthenticationProtocol:

    @staticmethod
    def success(nickname):
        response_code = 0x01
        data = PacketFormatter.from_string(nickname)

        return PacketFormatter.format_response_packet(AUTHENTICATION_TYPE, response_code, data)

    @staticmethod
    def bad_credentials():
        response_code = 0x02

        return PacketFormatter.format_response_packet(AUTHENTICATION_TYPE, response_code)

    @staticmethod
    def already_connected():
        response_code = 0x03

        return PacketFormatter.format_response_packet(AUTHENTICATION_TYPE, response_code)

    @staticmethod
    def banned():
        response_code = 0x04

        return PacketFormatter.format_response_packet(AUTHENTICATION_TYPE, response_code)

    @staticmethod
    def server_not_available():
        response_code = 0x05

        return PacketFormatter.format_response_packet(AUTHENTICATION_TYPE, response_code)
