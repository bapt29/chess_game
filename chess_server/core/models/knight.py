from core.models.piece import Piece
from core.models.position import Position


class Knight(Piece):

    def __str__(self):
        return "N"

    def move(self, initial_position, new_position):
        movement = Position.position_delta(initial_position, new_position)

        if movement.x == 1 and movement.y == 2 or movement.x == 2 and movement.y == 1:
            return True

        return False
