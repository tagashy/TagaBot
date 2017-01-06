# coding: utf8
from __future__ import unicode_literals

import time


class User:
    """
    IRC User class
    """

    def __init__(self, username, channel="UNKNOWN", server="UNKNOWN", admin=False):
        self.username = username
        self.server = server
        self.channel = channel
        self.admin = admin
        self.connection = [(self.channel, self.server)]
        self.actif = False
        self.lastSeen = time.strftime("%d/%m/%y %H:%M:%S")
        self.digiTime = time.time()
        self.realname = "UNKNOWN"
        self.age = "UNKNOWN"
        self.sexe = "THIRD"

    def update_last_seen(self, server="UNKNOWN", channel="UNKNOWN", admin=False):
        """
        update the last time a user has been seeb
        :param server: the server where the user has been seen
        :param channel: the channel where the user has been seen
        :param admin: is the user admin of the channel
        :return: Nothing what did you expect
        """
        self.lastSeen = time.strftime("%d/%m/%y %H:%M:%S")
        self.digiTime = time.time()
        self.server = server
        self.channel = channel
        self.admin = admin

    def __str__(self):
        ret = "user {} has been previously seen on {} and is on channels : ".format(self.username, self.lastSeen)
        for co in self.connection:
            ret += "{}=>{}, ".format(co[1], co[0])
        return ret

    def info(self):
        """
        retrieve personal information about user
        :return: personal information about user (str/unicode)
        """
        return "{} is {} years old, {}'s name is {} and is sexe is {}".format(self.username, self.age, self.username,
                                                                              self.realname, self.age)


class Users:
    """
    IRC list of users
    """

    def __init__(self):
        self.__users = []

    def user_exist(self, pseudo):
        """
        check if a user exist in the list
        :param pseudo: name of the user
        :return: True/False
        """
        for u in self.__users:
            if pseudo == u.username:
                return True
        return False

    def add_user(self, user, server="UNKNOWN", channel="UNKNOWN"):
        """
        add user to the list
        :param user: either the pseudo or a user object
        :param server: the server where user has been seen
        :param channel: the channel where user has been seen
        :return: 1(success)/0(exist)/-1(error)
        """
        admin = False
        if isinstance(user, User):
            if user.username[0:1] == "@":
                user.username = user.username[1:]
                user.admin = True
            u = self.get_user(user.username)
        elif isinstance(user, str) or isinstance(user, unicode):
            if user[0:1] == "@":
                user = user[1:]
                admin = True
            u = self.get_user(user)
        else:
            return -1
        if u == -1:
            if isinstance(user, User):
                self.__users.append(user)
            elif isinstance(user, str) or isinstance(user, unicode):
                self.__users.append(User(user, channel, server, admin))
            return 1
        else:
            for co in u.connection:
                if co[0] == channel and co[1] == server:
                    return 0
            u.connection.append((channel, server))
            return 1

    def deactivate_user(self, user):
        """
        deactivate user in user list
        :param user: either the pseudo or a user object
        :return: 1(success)/0(exist)/-1(error)
        """
        if isinstance(user, User):
            u = self.get_user(user.username)
        elif isinstance(user, str) or isinstance(user, unicode):
            u = self.get_user(user)
        else:
            return -1
        if u != -1:
            u.actif = False
            return 1
        else:
            return 0

    def remove_user(self, user):
        """
        remove user from user list
        :param user: either the pseudo or a user object
        :return: 1(success)/0(exist)/-1(error)
        """
        if isinstance(user, User):
            u = self.get_user(user.username)
        elif isinstance(user, str) or isinstance(user, unicode):
            u = self.get_user(user)
        else:
            return -1
        if u != -1:
            self.__users.remove(u)
            return 1
        else:
            return 0

    def update_user(self, user, server="UNKNOWN", channel="UNKNOWN", alcolemie=False):
        """
        deactivate user in user list
        :param user: either the pseudo or a user object
        :param server: the server where user has been seen
        :param channel: the channel where user has been seen
        :param alcolemie: not used but for trolling
        :return: 1(success)/0(exist)/-1(error)
        """
        if isinstance(user, User):
            if user.username[:1] == "@":
                user = user[1:]
                admin = True
            else:
                admin = False
            u = self.get_user(user.username)
        elif isinstance(user, str) or isinstance(user, unicode):
            if user[:1] == "@":
                user = user[1:]
                admin = True
            else:
                admin = False
            u = self.get_user(user)
        else:
            return -1
        if u != -1:
            u.update_last_seen(server, channel, admin)
            if alcolemie:
                u.alcolemie += 1
            return 1
        else:
            return 0

    def get_user(self, user):
        """
        get user object direct reference (deprecated)
        :param user: username (str/unicode)
        :return: user object/-1(error)
        """
        if self.user_exist(user):
            for u in self.__users:
                if user == u.username:
                    return u
        else:
            return -1

    def __str__(self):
        ret = "USERLIST:"
        for user in self.__users:
            ret = "{}\r\n{}".format(ret, user)
        return ret
