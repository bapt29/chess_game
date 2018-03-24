from struct import pack, unpack


class PacketFormatter:

    @staticmethod
    def process_packet(data):
        packet_type, packet_code = unpack('2B', data[:1])
        packet_data = data[2:]

        return packet_type, packet_code, packet_data

    @staticmethod
    def format_response_packet(type, response, data=None):
        packet = bytearray()

        packet.append(type)
        packet.append(response)

        if data is not None:
            packet.extend(data)

        return packet

    @staticmethod
    def from_string(string):
        converted_string = bytearray()
        converted_string.append(len(string))

        for c in string:
            converted_string.append(ord(c))

        return converted_string

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
        return bytearray(pack("H", time))
