from core.models.position import Position
from core.models.piece import Piece
from core.models.pawn import Pawn
from core.models.knight import Knight
from core.models.queen import Queen
from core.models.bishop import Bishop
from core.models.rook import Rook
from core.models.king import King


class Board:

    def __init__(self):
        self.__piece_list = dict()
        self.__init_board()

    def __str__(self):
        string = ""

        for j in range(8):
            for i in range(8):
                position = Position(i, j)

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
            self.__piece_list[Position(i, 6)] = Pawn(Piece.WHITE)

        # Black pawns

        for i in range(8):
            self.__piece_list[Position(i, 1)] = Pawn(Piece.BLACK)

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
            if not piece.eaten:
                return piece

        return None

    def get_piece_position(self, wanted_piece):
        for position, piece in self.__piece_list.items():
            if piece == wanted_piece:
                return position

        return None

    def get_piece_by_id(self, piece_id):
        for piece in self.__piece_list.values():
            if piece.id == piece_id:
                return piece

        return None

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

                piece_at_new_position.eaten = True

            # TODO: Huge mistake to fix out: Potentially 2 pieces on same position if a piece has been eaten

            return True

        return False # TODO: Return a specific value when a piece has been eaten

    def move_pawn(self, piece, initial_position, new_position): # Specific method for pawns (handle exceptions)
        # TODO: Prevent pawn from eating a piece just in front (it can only eat piece in its diagonal)
        # TODO: Handle "En passant" move (If there is a piece next to the pawn, it can eat it)
        # TODO: Handle "Promotion" move (If the pawn reach border of board, it can transform to any kind of piece)

        possible_piece1 = self.piece_at(new_position)  # There is a piece in its direct diagonal

        # "En passant" move
        delta_y = -1 if piece.color == Piece.WHITE else 1
        possible_piece2 = self.piece_at(Position(new_position.x, new_position.y - delta_y))

        return False # TODO: Return a specific value when a piece has been eaten

    def is_movement_allowed(self, piece, initial_position, new_position):
        if piece.move(initial_position, new_position) and not self.detect_collision(initial_position, new_position):
            return True

        return False

    def detect_collision(self, initial_position, new_position):
        movement = new_position - initial_position
        absolute_movement = abs(movement)

        if absolute_movement.x == 1 or absolute_movement.y == 1:  # No collision possible
            return False

        if absolute_movement.x > 1 and absolute_movement.y > 1:  # Diagonal movement
            for x in range(initial_position.x, new_position.x, 1 if movement.x > 1 else -1):
                for y in range(initial_position.y, new_position.y, 1 if movement.y > 1 else -1):
                    if self.piece_at(Position(x, y)):
                        return True
        else:  # Linear movement
            if absolute_movement.x > 1:  # Movement on X
                for x in range(initial_position.x, new_position.x, 1 if movement.x > 1 else -1):
                    if self.piece_at(Position(x, initial_position.y)):
                        return True
            else:  # Movement on Y
                for y in range(initial_position.y, new_position.y, 1 if movement.y > 1 else -1):
                    if self.piece_at(Position(initial_position.x, y)):
                        return True

        return False


if __name__ == "__main__":
    b = Board()
    print(b)
