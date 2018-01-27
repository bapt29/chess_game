from chess_server.core.models.piece import Piece
from chess_server.core.models.position import Position


class Pawn(Piece):

    def __init__(self, color):
        Piece.__init__(self, color)
        self.en_passant_turn = 0  # Special movement "en passant": available only one turn
        self.en_passant_piece_id = 0  # " " ": the enemy piece related to this move

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

    def promote_to(self, piece_type_chosen):
        if self.__class__ == piece_type_chosen:  # Chose a pawn: don't need modification
            return

        new_piece = piece_type_chosen(self.color)

        self.__dict__ = new_piece.__dict__
        self.__class__ = piece_type_chosen
