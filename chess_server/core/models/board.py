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

        if piece is None:
            return False

        if isinstance(piece, Pawn):  # Use specific pawn method
            return self.move_pawn(piece, piece_position, new_position)

        if self.is_movement_allowed(piece, piece_position, new_position):
            piece_at_new_position = self.piece_at(new_position)

            if piece_at_new_position is not None:
                if piece.color == piece_at_new_position.color:  # Own piece
                    return False

                self.delete_piece(piece_at_new_position)  # Captured a piece: remove it from the list

            self.set_piece_position(piece, new_position)
            return True

        return False # TODO: Return a specific value when a piece has been captured

    def move_pawn(self, pawn, current_position, new_position): # Specific method for pawns (handle exceptions)
        # TODO: Prevent pawn from eating a piece just in front (it can only eat piece in its diagonal)
        # TODO: Handle "En passant" move (If there is a piece next to the pawn, it can eat it)
        # TODO: Handle "Promotion" move (If the pawn reach border of board, it can transform to any kind of piece)
        movement = Position.position_delta(current_position, new_position)
        piece_at_new_position = self.piece_at(new_position)

        if movement.x == 0:  # Linear movement
            if pawn.move(current_position, new_position) and not self.detect_collision(current_position, new_position):
                if piece_at_new_position is None:  # Pawn can't capture with linear movement
                    self.en_passant_handler(pawn, new_position)
                    self.set_piece_position(pawn, new_position)

                    if pawn.is_promotion_available(new_position):  # TODO: Handle promotion
                        pass

                    return True
        else:  # Diagonal movement (should capture a piece)
            if pawn.move_eat(current_position, new_position):
                if piece_at_new_position is not None:  # There is a piece at new position
                    if pawn.color != piece_at_new_position.color:
                        self.delete_piece(piece_at_new_position)
                        self.en_passant_handler(pawn, new_position)
                        self.set_piece_position(pawn, new_position)

                        if pawn.is_promotion_available(new_position):  # TODO: Handle promotion
                            pass

                        return True
                else:
                    # Piece next to this pawn's current position and behind wanted position
                    piece_next_to_y = new_position.y - 1 if pawn.color == Piece.WHITE else new_position.y + 1
                    piece_next_to = self.piece_at(Position(new_position.x, piece_next_to_y))

                    if pawn.en_passant[piece_next_to.id] == self.__game.turn + 1:  # If the move is done the next turn
                        self.delete_piece(piece_next_to)
                        del pawn.en_passant[piece_next_to.id]
                        self.set_piece_position(pawn, new_position)

                        if pawn.is_promotion_available(new_position):  # TODO: Handle promotion
                            pass

                        return True

        return False # TODO: Return a specific value when a piece has been captured

    def en_passant_handler(self, pawn, new_position):
        pieces_next_to_new_position = self.get_pieces_next_to(new_position)

        if pieces_next_to_new_position[0] is not None:
            pawn.en_passant[pieces_next_to_new_position[0].id] = self.__game.turn

        if pieces_next_to_new_position[1] is not None:
            pawn.en_passant[pieces_next_to_new_position[1].id] = self.__game.turn

    def is_movement_allowed(self, piece, current_position, new_position):
        if piece.move(current_position, new_position) and not self.detect_collision(current_position, new_position):
            return True

        return False

    def detect_collision(self, current_position, new_position):
        movement = Movement(current_position, new_position)
        absolute_movement = abs(movement)

        if absolute_movement.x == 1 or absolute_movement.y == 1:  # Move one cell only -> no collision possible
            return False

        if absolute_movement.x > 1 and absolute_movement.y > 1:  # Diagonal movement
            for x in range(current_position.x + 1, new_position.x, 1 if movement.x > 1 else -1):
                for y in range(current_position.y + 1, new_position.y, 1 if movement.y > 1 else -1):
                    if self.piece_at(Position(x, y)) is not None:
                        return True
        else:  # Linear movement
            if absolute_movement.x > 1:  # Movement on X
                for x in range(current_position.x + 1, new_position.x, 1 if movement.x > 1 else -1):
                    if self.piece_at(Position(x, current_position.y)) is not None:
                        return True
            else:  # Movement on Y
                for y in range(current_position.y + 1, new_position.y, 1 if movement.y > 1 else -1):
                    if self.piece_at(Position(current_position.x, y)) is not None:
                        return True

        return False


if __name__ == "__main__":
    b = Board()
    pawn1 = b.piece_at(Position(0, 1))
    pawn2 = b.piece_at(Position(0, 6))
    b.move_piece(pawn1.id, Position(0, 3))
    b.move_piece(pawn2.id, Position(0, 4))
    b.move_piece(pawn1.id, Position(0, 4))
    print(b)
