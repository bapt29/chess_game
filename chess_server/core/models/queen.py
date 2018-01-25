from chess_server.core.models.piece import Piece
from chess_server.core.models.position import Position


class Queen(Piece):

    def __str__(self):
        return "Q"

    def move(self, initial_position, new_position):
        movement = Position.position_delta(initial_position, new_position)

        if movement.x > 0 and movement.y == 0 or movement.y > 0 and movement.x == 0 or movement.x > 0 and movement.x == movement.y:
            return True

        return False
