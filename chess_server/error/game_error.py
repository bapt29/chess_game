class NoMovement(Exception):
    pass


class PieceNotFound(Exception):
    pass


class PieceCollision(Exception):
    def __init__(self, piece_id):
        self.piece_id = piece_id


class OwnPiece(Exception):
    pass


class PieceCaptured(Exception):
    def __init__(self, piece_id):
        self.piece_id = piece_id


class PawnPromoted(Exception):
    pass


class MovementNotAllowed(Exception):
    pass


class PawnPromotedAndPieceCaptured(Exception):
    def __init__(self, piece_id):
        self.piece_id = piece_id
