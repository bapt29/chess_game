import hashlib
import os
import persistent
from BTrees.LLBTree import TreeSet


class User(persistent.Persistent):

    def __init__(self, username, nickname, email):
        self.username = username
        self.nickname = nickname

        self.password_salt = None
        self.password_hash = None

        self.email = email
        self.friend_list = TreeSet()

        self.banned = False
        self.connected = False
