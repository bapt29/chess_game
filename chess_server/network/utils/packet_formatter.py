import struct
from chess_server.error.network_error import *


class PacketFormatter:

    @staticmethod
    def process_packet(data):
        packet_type, packet_code, packet_data = data[0], data[1], data[2:]

        return packet_type, packet_code, packet_data

    @staticmethod
    def format_response_packet(packet_type, packet_code, data=None):
        packet = bytearray()

        packet.append(packet_type)
        packet.append(packet_code)

        if data is not None:
            packet.extend(data)

        return packet

    @staticmethod
    def from_string(string):
        string_bytes = bytearray(string.decode())
        string_bytes_length = len(string_bytes)

        converted_string = bytearray().append(string_bytes_length)
        converted_string.extend(string_bytes)

        return converted_string

    @staticmethod
    def to_string(data, string_number=1):
        strings = list()
        current_index = 0

        for i in range(string_number):
            string_bytes_length = data[current_index]

            if string_bytes_length == 0:
                strings.append(None)
                continue

            try:
                strings.append(data[current_index + 1:current_index + string_bytes_length + 1].decode())
            except UnicodeDecodeError:
                raise InvalidPacket

            current_index += string_bytes_length + 1

        return strings

    @staticmethod
    def from_list(list):
        return PacketFormatter.from_string(list)

    @staticmethod
    def from_position(position):
        return bytearray(position.x << 4 | position.y)  # 1 byte: 4 bits X | 4 bits Y

    @staticmethod
    def from_piece_list(piece_list):
        pieces = bytearray()

        pieces.append(len(piece_list))

        for position, piece in piece_list:
            pieces.append(piece.id)
            pieces.append(piece.color)
            pieces.append(ord(str(piece)))
            pieces.extend(PacketFormatter.from_position(position))

        return pieces

    @staticmethod
    def from_seconds(time):
        return bytearray(struct.pack("H", time))


if __name__ == "__main__":
    test = b"\x06coucou\x07bonjour\x0Acoucoubonj"
    print(PacketFormatter.to_string(test, 3))
