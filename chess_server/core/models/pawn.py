from chess_server.core.models.piece import Piece
from chess_server.core.models.position import Position


class Pawn(Piece):

    def __str__(self):
        return "P"

    def move(self, initial_position, new_position):
        movement = Position.position_delta(initial_position, new_position)

        # Color 0: White / Color 1: Black | Initial position
        if self.color == 0 and initial_position.y == 1 or self.color == 1 and initial_position.y == 6:
            if new_position.y > initial_position.y and movement.y in range(1, 3):
                return True

        # Already Moved
        if new_position.y > initial_position.y and movement.y == 1:
            return True

        return False

    def move_eat(self, initial_position, new_position):
        movement = Position.position_delta(initial_position, new_position)

        if new_position.y > initial_position.y and movement.x == 1 and movement.y == 1:
            return True

        return False
