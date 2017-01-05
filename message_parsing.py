from __future__ import unicode_literals

import re
import time

message_regex = re.compile(
    r"^:([\w\[\]\\`_\^\{\|\}][\w\d\[\]\\`_\^\{\|\}\-]{1,})!([^\r\n@ ]+)@([\w\d\-\./]+)\s([\w]*)\s:?([&\#\w][^\s,\x07]{2,200})\s?:?(.*)$",
    re.VERBOSE)


class Message:
    """
    a Message represnetation of IRC Message
    """
    def __init__(self, pseudo=None, user_account=None, ip=None, msg_type=None, content=None, target=None, server=None):
        self.pseudo = pseudo
        self.user_account = user_account
        self.ip = ip
        self.msg_type = msg_type
        self.content = content
        self.target = target
        self.server = server
        self.time = time.time()

    def construct_message(self):
        """
        construct a real IRC Message
        :return: IRC byte sequence Message
        """
        msg_type = self.msg_type
        if msg_type == "PUBMSG":
            msg_type = "PRIVMSG"
        ret = "{} {}".format(msg_type, self.target)
        if self.content:
            ret += " :{}".format(self.content)
        return ret + "\r\n"

    def get_time(self):
        """
        time of the Message
        :return: the time were Message was created
        """
        return time.strftime("%d/%m/%y %M:%H:%S", self.time)

    def __str__(self):
        if self.pseudo is None:
            pseudo = "*"
        else:
            pseudo = self.pseudo
        if self.user_account is None:
            user_account = "*"
        else:
            user_account = self.user_account
        if self.ip is None:
            ip = "*"
        else:
            ip = self.ip
        if self.msg_type is None:
            msg_type = "*"
        else:
            msg_type = self.msg_type
        if self.content is None:
            content = "*"
        else:
            content = self.content
        if self.target is None:
            target = "*"
        else:
            target = self.target
        if self.server is None:
            server = "*"
        else:
            server = self.server
        return "pseudo={},user_account={},ip={},msg_type={},content={},target={},server={}".format(pseudo,
                                                                                                   user_account,
                                                                                                   ip,
                                                                                                   msg_type,
                                                                                                   content,
                                                                                                   target,
                                                                                                   server)


def parse(msg):
    """
    parse socket Message to IRC Message
    :param msg: the socket Message
    :return: IRC Message
    """
    msg = msg.replace("\r", "").replace("\n", "").replace("\b", "")
    pseudo = user_account = ip = msg_type = content = target = ""
    msg_parsed = message_regex.search(msg)
    if msg_parsed:
        data = msg_parsed.groups()
        if len(data) >= 6:
            pseudo = data[0]
            user_account = data[1]
            ip = data[2]
            msg_type = data[3]
            target = data[4]
            content = data[5]
        if target.startswith("#") and msg_type == "PRIVMSG":
            msg_type = "PUBMSG"
    return Message(pseudo, user_account, ip, msg_type, content, target)
