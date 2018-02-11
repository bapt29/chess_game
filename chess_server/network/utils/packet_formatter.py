from struct import pack


class PacketFormatter:

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
        return bytearray(position.x << 4 | position.y)

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
