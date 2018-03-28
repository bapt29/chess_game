import os
import hashlib

import transaction
from BTrees.LOBTree import LOBTree

from chess_server.database.models.user import User
from chess_server.error.database_error import *


class UserManager:

    def __init__(self, database):
        self.db = database

        if "users" not in self.db.db_root:
            self.db.db_root["users"] = LOBTree()

        self.users = self.db.db_root["users"]

    def get_user_by_id(self, user_id):
        if user_id not in self.users.keys():
            raise UserNotFound

        return self.users[user_id]

    def get_user_id(self, username=None, nickname=None, email=None):
        if username is not None:
            for user_id, user in self.users.items():
                if user.username == username:
                    return user_id
        elif nickname is not None:
            for user_id, user in self.users.items():
                if user.nickname == nickname:
                    return user_id
        elif email is not None:
            for user_id, user in self.users.items():
                if user.email == email:
                    return user_id

        raise UserNotFound

    def get_user(self, username):
        return self.users[self.get_user_id(username=username)]

    def get_user_list(self):
        return self.users.values()

    def get_friend_list(self, username, connected=None):
        user_id = self.get_user_id(username=username)
        friend_list = list()

        if connected is not None:
            if not isinstance(connected, bool):
                raise TypeError

            for friend_username in list(self.users[user_id].friend_list):
                try:
                    friend_id = self.get_user_id(friend_username)
                    friend = self.users[friend_id]
                except UserNotFound:
                    pass
                else:
                    if friend.connected == connected:
                        friend_list.append((friend_id, friend.nickname, friend.connected))
        else:
            for friend_username in list(self.users[user_id].friend_list):
                try:
                    friend_id = self.get_user_id(friend_username)
                    friend = self.users[friend_id]
                except UserNotFound:
                    pass
                else:
                    friend_list.append((friend_id, friend.nickname, friend.connected))

        return friend_list

    def is_connected(self, username):
        user_id = self.get_user_id(username)

        return self.users[user_id].connected

    def is_banned(self, username):
        user_id = self.get_user_id(username)

        return self.users[user_id].banned

    def authentication(self, username, password):
        self.password_match(username, password)
        user_id = self.get_user_id(username=username)

        if self.is_connected(username):
            raise UserAlreadyConnected

        if self.is_banned(username):
            raise UserBanned

    def add_user(self, username, nickname, password, email):
        try:
            self.get_user_id(username=username)
        except UserNotFound:
            pass
        else:
            raise UsernameAlreadyTaken

        try:
            self.get_user_id(nickname=nickname)
        except UserNotFound:
            pass
        else:
            raise NicknameAlreadyTaken

        try:
            self.get_user_id(email=email)
        except UserNotFound:
            pass
        else:
            raise EmailAlreadyTaken

        min_id = 1

        try:
            min_id = self.users.minKey()
        except ValueError:
            pass

        self.users[min_id] = User(username, nickname, email)
        self.set_password(username, password)

        transaction.commit()

    def remove_user(self, user_id):
        if user_id not in self.users.keys():
            raise UserNotFound

        del self.users[user_id]
        transaction.commit()

    def user_list(self):
        return dict(self.users)

    def add_friend(self, username, friend_nickname):
        user = self.get_user(username=username)

        try:
            friend_id = self.get_user_id(nickname=friend_nickname)
        except UserNotFound:
            raise FriendNotFound

        if friend_id in user.friend_list:
            raise AlreadyFriend

        if friend_id == self.get_user_id(username):
            raise CantBeFriendWithYourself

        user.friend_list.add(friend_id)
        transaction.commit()

    def remove_friend(self, username, friend_nickname):
        user = self.get_user(username)
        friend_id = self.get_user_id(nickname=friend_nickname)

        try:
            user.friend_list.remove(friend_id)
        except KeyError:
            raise FriendNotInFriendList

        transaction.commit()

    def set_password(self, username, password):
        user = self.get_user(username)

        user.password_salt = os.urandom(64)
        user.password_hash = hashlib.pbkdf2_hmac('sha512',
                                                 password.encode(),
                                                 user.password_salt,
                                                 100000)

    def password_match(self, username, password):
        user = self.get_user(username)

        password_hash = hashlib.pbkdf2_hmac('sha512',
                                            password.encode(),
                                            user.password_salt,
                                            100000)

        if user.password_hash != password_hash:
            raise UserBadPassword

    def set_connected(self, user_id, connected):
        user = self.get_user_by_id(user_id)

        if not isinstance(connected, bool):
            raise TypeError

        user.connected = connected
        transaction.commit()

    def set_banned(self, user_id, banned):
        if not isinstance(banned, bool):
            raise TypeError

        if user_id not in self.users.keys():
            raise UserNotFound

        self.users[user_id].banned = banned
        transaction.commit()
