from chess_server.core.models.position import Position
from chess_server.core.models.movement import Movement
from chess_server.core.models.piece import Piece
from chess_server.core.models.pawn import Pawn
from chess_server.core.models.knight import Knight
from chess_server.core.models.queen import Queen
from chess_server.core.models.bishop import Bishop
from chess_server.core.models.rook import Rook
from chess_server.core.models.king import King


class Board:

    CODES = {"normal": 0,
             "collision": 1,
             "captured": 2,
             "own_piece": 3,
             "no_movement": 4,
             "pawn_promoted": 5,
             "pawn_no_piece_to_capture": 6
             }

    def __init__(self, game=None):
        self.__game = game
        self.__piece_list = dict()
        self.__init_board()

    def __str__(self):
        string = ""

        for y in range(7, -1, -1):  # Start at top of board
            for x in range(8):
                position = Position(x, y)

                if self.piece_at(position):
                    string += str(self.__piece_list[position])
                else:
                    string += "X"

                string += "  "

            string += "\n"

        return string

    @property
    def piece_list(self):
        return self.__piece_list

    @piece_list.setter
    def piece_list(self, value):
        self.__piece_list = value

    def __init_board(self):
        # White pawns

        for i in range(8):
            self.__piece_list[Position(i, 1)] = Pawn(Piece.WHITE)

        # Black pawns

        for i in range(8):
            self.__piece_list[Position(i, 6)] = Pawn(Piece.BLACK)

        # White knights

        self.__piece_list[Position(1, 0)] = Knight(Piece.WHITE)
        self.__piece_list[Position(6, 0)] = Knight(Piece.WHITE)

        # Black knights

        self.__piece_list[Position(1, 7)] = Knight(Piece.BLACK)
        self.__piece_list[Position(6, 7)] = Knight(Piece.BLACK)

        # White bishops

        self.__piece_list[Position(2, 0)] = Bishop(Piece.WHITE)
        self.__piece_list[Position(5, 0)] = Bishop(Piece.WHITE)

        # Black bishops

        self.__piece_list[Position(2, 7)] = Bishop(Piece.BLACK)
        self.__piece_list[Position(5, 7)] = Bishop(Piece.BLACK)

        # White rooks

        self.__piece_list[Position(0, 0)] = Rook(Piece.WHITE)
        self.__piece_list[Position(7, 0)] = Rook(Piece.WHITE)

        # Black rooks

        self.__piece_list[Position(0, 7)] = Rook(Piece.BLACK)
        self.__piece_list[Position(7, 7)] = Rook(Piece.BLACK)

        # Kings

        self.__piece_list[Position(4, 0)] = King(Piece.WHITE)
        self.__piece_list[Position(4, 7)] = King(Piece.BLACK)

        # Queens

        self.__piece_list[Position(3, 0)] = Queen(Piece.WHITE)
        self.__piece_list[Position(3, 7)] = Queen(Piece.BLACK)

    def piece_at(self, position):
        try:
            piece = self.__piece_list[position]
        except KeyError:
            pass
        else:
            return piece

        return None

    def get_piece_position(self, wanted_piece):
        for position, piece in self.__piece_list.items():
            if piece == wanted_piece:
                return position

        return None

    def set_piece_position(self, piece, new_position):
        if piece is not None:
            self.__piece_list[new_position] = self.delete_piece(piece)

    def get_piece_by_id(self, piece_id):
        for piece in self.__piece_list.values():
            if piece.id == piece_id:
                return piece

        return None

    def get_pieces(self, piece_type, color):
        pieces_list = list()

        for position, piece in self.__piece_list.items():
            if piece.color == color and isinstance(piece, piece_type):
                if piece_type == King:  # Always only one king on board
                    return piece

                pieces_list.append(position)

        return pieces_list

    def get_pieces_next_to(self, position):
        pieces = None

        if position.x == 0:  # Left border
            return None, self.piece_at(Position(position.x + 1, position.y))

        if position.x == 7:  # Right border
            return self.piece_at(Position(position.x - 1, position.y)), None

        # Return tuple with the piece on two possible position
        return self.piece_at(Position(position.x - 1, position.y)), self.piece_at(Position(position.x + 1, position.y))

    def delete_piece(self, piece):
        return self.__piece_list.pop(self.get_piece_position(piece))

    def move_piece(self, piece_id, new_position):
        piece = self.get_piece_by_id(piece_id)
        piece_position = self.get_piece_position(piece)

        response = {"codes": [], "movement_allowed": False, "collision": int, "captured_piece": int}

        if piece is None:
            return response

        if piece_position == new_position:
            response["codes"].append(Board.CODES["no_movement"])
            return response

        if isinstance(piece, Pawn):  # Use specific pawn method
            return self.move_pawn(piece, piece_position, new_position)

        if piece.move(piece_position, new_position):
            if not isinstance(piece, Knight):
                collision = self.detect_collision(piece_position, new_position)

                if collision is not None:
                    response["codes"].append(Board.CODES["collision"])
                    response["collision"] = self.piece_at(collision).id

                    return response

            piece_at_new_position = self.piece_at(new_position)

            if piece_at_new_position is not None:
                if piece_at_new_position.color != piece.color:
                    response["codes"].append(Board.CODES["own_piece"])
                    return response

                response["codes"].append(Board.CODES["captured"])
                response["captured_piece"] = piece_at_new_position.id

            response["movement_allowed"] = True
            return response

    def move_pawn(self, pawn, current_position, new_position): # Specific method for pawns (handle exceptions)
        movement = Movement(current_position, new_position)
        piece_at_new_position = self.piece_at(new_position)

        response = {"codes": [], "movement_allowed": False, "collision": int, "captured_piece": int}

        if movement.x == 0:  # Linear movement
            if pawn.move(current_position, new_position):
                collision = self.detect_collision(current_position, new_position)

                if collision is not None:
                    response["codes"].append(Board.CODES["collision"])
                    response["collision"] = self.piece_at(collision).id

                    return response

                if piece_at_new_position is not None:  # Pawn can't capture with linear movement
                    response["codes"].append(Board.CODES["collision"])
                    response["collision"] = piece_at_new_position.id

                    return response

                #self.en_passant_handler(pawn, new_position)
                self.set_piece_position(pawn, new_position)

                if pawn.is_promotion_available(new_position):  # TODO: Handle promotion
                    response["codes"].append(Board.CODES["pawn_promoted"])

                response["movement_allowed"] = True

        else:  # Diagonal movement (should capture a piece)
            if pawn.move_eat(current_position, new_position):

                if piece_at_new_position is None:
                    # Piece next to this pawn's current position and behind wanted position
                    piece_next_to_y = new_position.y - 1 if pawn.color == Piece.WHITE else new_position.y + 1
                    piece_next_to = self.piece_at(Position(new_position.x, piece_next_to_y))

                    response["codes"].append(Board.CODES["pawn_no_piece_to_capture"])
                    return response

                if pawn.color != piece_at_new_position.color:
                    self.delete_piece(piece_at_new_position)
                    #self.en_passant_handler(pawn, new_position)
                    self.set_piece_position(pawn, new_position)

                    if pawn.is_promotion_available(new_position):  # TODO: Handle promotion
                        pass

                    return True
                else:
                    # Piece next to this pawn's current position and behind wanted position
                    piece_next_to_y = new_position.y - 1 if pawn.color == Piece.WHITE else new_position.y + 1
                    piece_next_to = self.piece_at(Position(new_position.x, piece_next_to_y))

                    # if pawn.en_passant[piece_next_to.id] == self.__game.turn + 1:  # If the move is done the next turn
                    #    self.delete_piece(piece_next_to)
                    #    del pawn.en_passant[piece_next_to.id]
                    #    self.set_piece_position(pawn, new_position)

                    #    if pawn.is_promotion_available(new_position):  # TODO: Handle promotion
                    #        pass

                    #    return True

        return response

    def en_passant_handler(self, pawn, new_position):
        pieces_next_to_new_position = self.get_pieces_next_to(new_position)

        if pieces_next_to_new_position[0] is not None:
            pawn.en_passant[pieces_next_to_new_position[0].id] = self.__game.turn

        if pieces_next_to_new_position[1] is not None:
            pawn.en_passant[pieces_next_to_new_position[1].id] = self.__game.turn

    def detect_collision(self, current_position, new_position):
        movement = Movement(current_position, new_position)
        absolute_movement = abs(Movement(current_position, new_position))

        if absolute_movement.x in range(2) or absolute_movement.y in range(2):  # Move one cell only -> no collision possible
            return None

        x_range = None
        y_range = None

        if movement.x > 1:
            x_range = range(current_position.x + 1, new_position.x)
        elif movement.x < -1:
            x_range = range(new_position.x + 1, current_position.x)

        if movement.y > 1:
            y_range = range(current_position.y + 1, new_position.y)
        elif movement.y < -1:
            y_range = range(new_position.y + 1, current_position.y)

        if absolute_movement.x > 1 and absolute_movement.y > 1:  # Diagonal movement
            for x in x_range:
                for y in y_range:
                    if self.piece_at(Position(x, y)) is not None:
                        return Position(x, y)
        else:  # Linear movement
            if absolute_movement.x > 1:  # Movement on X
                for x in x_range:
                    if self.piece_at(Position(x, current_position.y)) is not None:
                        return Position(x, current_position.y)
            else:  # Movement on Y
                for y in y_range:
                    if self.piece_at(Position(current_position.x, y)) is not None:
                        return Position(current_position.x, y)

        return None

    def is_king_in_check(self, color):
        king = self.get_pieces(King, color)
        king_position = self.get_piece_position(king)
        knight_list = self.get_pieces(Knight, Piece.WHITE if color == Piece.BLACK else Piece.BLACK)

        # List of all pieces that can capture the king at next turn
        piece_list = list()

        # In check detection
        # At first, check if enemy knights can capture the king
        for knight in knight_list:
            knight_position = self.get_piece_position(knight)

            if knight.move(knight_position, king_position):
                piece_list.append(knight)

        # Secondly, check collisions on every diagonals and lines then check if the piece can move to king's position
        collision_position_list = self.get_all_collisions_from_position(king_position)

        for position in collision_position_list:
            piece = self.piece_at(position)

            if piece.color != king.color and piece.move(position, king_position):
                piece_list.append(piece)

        if len(piece_list) > 0:
            return piece_list

        return None

    def get_all_collisions_from_position(self, position):
        position_list = list()

        # Lines

        # +X
        position = self.get_collision_to_max_position(position, Position(7, position.y))

        if position is not None:
            position_list.append(position)

        # -X
        position = self.get_collision_to_max_position(position, Position(0, position.y))

        if position is not None:
            position_list.append(position)

        # +Y
        position = self.get_collision_to_max_position(position, Position(position.x, 7))

        if position is not None:
            position_list.append(position)

        # -Y
        position = self.get_collision_to_max_position(position, Position(position.x, 0))

        if position is not None:
            position_list.append(position)

        # Diagonals

        # +X +Y
        position = self.get_collision_to_max_position(position, Position(7, 7))

        if position is not None:
            position_list.append(position)

        # +X -Y
        position = self.get_collision_to_max_position(position, Position(7, 0))

        if position is not None:
            position_list.append(position)

        # -X +Y
        position = self.get_collision_to_max_position(position, Position(0, 7))

        if position is not None:
            position_list.append(position)

        return position_list

    def get_collision_to_max_position(self, initial_position, max_position):
        if initial_position != max_position:
            collision_position = self.detect_collision(initial_position, max_position)

            if collision_position is None:
                collision_position = self.piece_at(max_position)

            if collision_position is not None:
                return collision_position

        return None


if __name__ == "__main__":
    b = Board()

    pawn1 = b.piece_at(Position(0, 1))
    pawn2 = b.piece_at(Position(1, 6))

    print("\n" + str(b))

    b.move_piece(pawn1.id, Position(0, 3))
    print(b)
    b.move_piece(pawn2.id, Position(1, 4))
    print(b)
    b.move_piece(pawn1.id, Position(1, 4))
    print(b)