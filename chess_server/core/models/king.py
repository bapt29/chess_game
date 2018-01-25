from core.models.piece import Piece
from core.models.position import Position


class King(Piece):

    def __str__(self):
        return "K"

    def move(self, initial_position, new_position):
        movement = Position.position_delta(initial_position, new_position)

        if movement.x in range(2) and movement.y in range(2):
            return True

        return False
