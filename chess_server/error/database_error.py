class UserNotFound(Exception):
    pass


class UserAlreadyConnected(Exception):
    pass


class UserBadPassword(Exception):
    pass


class UserBanned(Exception):
    pass


class FriendNotFound(Exception):
    pass


class FriendNotInFriendList(Exception):
    pass


class AlreadyFriend(Exception):
    pass


class UsernameAlreadyTaken(Exception):
    pass


class NicknameAlreadyTaken(Exception):
    pass


class EmailAlreadyTaken(Exception):
    pass


class UserCreationFailed(Exception):
    pass


class GameNotFound(Exception):
    pass


class GameAlreadyInProgress(Exception):
    pass


class GameAlreadyOver(Exception):
    pass


class PlayerAlreadyInGame(Exception):
    pass
