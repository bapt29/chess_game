from chess_server.core.models.piece import Piece
from chess_server.core.models.position import Position


class Pawn(Piece):

    def __init__(self, color):
        Piece.__init__(self, color)
        self.en_passant = dict()  # Key: Piece id; Value: Turn number

    def __str__(self):
        return "P"

    def move(self, current_position, new_position):
        movement = Position.position_delta(current_position, new_position)
        
        if self.color == Piece.WHITE:  # White pawn
            if new_position.y > current_position.y:  # Move forward
                if current_position.y == 1:  # Initial position (never moved)
                    if movement.y in range(1, 3):  # Move from 1 to 2 cells
                        return True
                else:  # Pawn already moved
                    if movement.y == 1:  # Move 1 cell
                        return True
        else:  # Black pawn
            if new_position.y < current_position.y:  # Move forward
                if current_position.y == 6:  # Initial position (never moved)
                    if movement.y in range(1, 3):  # Move from 1 to 2 cells
                        return True
                else:  # Pawn already moved
                    if movement.y == 1:  # Move 1 cell
                        return True

        return False  # if did not pass any verification -> movement not allowed

    def move_eat(self, current_position, new_position):
        movement = Position.position_delta(current_position, new_position)

        if movement.x == 1 and movement.y == 1:  # Move one cell in diagonal
            if self.color == Piece.WHITE:  # White pawn
                if new_position.y > current_position.y:  # Move forward
                    return True
            else:  # Black pawn
                if new_position.y < current_position.y:  # Move forward
                    return True

        return False

    def is_promotion_available(self, new_position):
        if new_position.y == 7 and self.color == Piece.WHITE:
            return True

        if new_position.y == 0 and self.color == Piece.BLACK:
            return True

        return False

    def promote_to(self, piece_type_chosen):
        if self.__class__ == piece_type_chosen:  # Chose a pawn: don't need modification
            return

        saved_id = self.id
        new_piece = piece_type_chosen(self.color)

        self.__dict__ = new_piece.__dict__
        self.__class__ = piece_type_chosen
        self.id = saved_id  # Keep same id: Avoid problems between server and client
