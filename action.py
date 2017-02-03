# coding: utf8
from __future__ import unicode_literals

from utils import print_message


class Command:
    """
    command class
    represent a function pointeur and when to call it
    """

    def __init__(self, keyword, function, name, helpable=True, match=False, args=None):
        self.keyword = keyword
        self.function = function
        self.name = name
        self.help = helpable
        self.match = match
        self.args = args

    def __str__(self):
        return "Command {} activate by {} helpable {} with args {} matchable {}".format(self.name, self.keyword,
                                                                                        self.help, self.args,
                                                                                        self.match)


def command_loop(message, cmds, bot):
    """
    search commands who match Message and execute it

    :param message: the commands to execute (str/uni)
    :param cmds: the commands available
    :param bot: the bot who invoke the command (must expose a reply method, other parameter can be require depending on the function)
    :return: 1(success)/None
    """
    if "!help" == message.content:
        help_cmds(cmds, message.msg_type, message.pseudo, message.target, bot)
        print_message("[!] help called by " + message.pseudo)
        return 1
    for cmd in cmds:
        if isinstance(cmd.keyword, str) or isinstance(cmd.keyword, unicode):
            if message.content == cmd.keyword or message.content == cmd.keyword + "?":
                if "?" in message:
                    help_cmd(cmd, message.msg_type, message.pseudo, message.target, bot)
                else:
                    print_message("[!] function " + cmd.name + " called by " + message.pseudo)
                    cmd.function(message, bot)
                return 1
        else:
            for key in cmd.keyword:
                if message.content == key + "?" or message.content == key:
                    help_cmd(cmd, message.msg_type, message.pseudo, message.target, bot)
                elif message.content.startswith(key + " "):
                    print_message("[!] function " + cmd.name + " called by " + message.pseudo)
                    cmd.function(message, bot)
                    return 1
                elif cmd.match and key in message.content:
                    if "?" in message.content:
                        help_cmd(cmd, message.msg_type, message.pseudo, message.target, bot)
                    else:
                        print_message("[!] function " + cmd.name + " called by " + message.pseudo)
                        cmd.function(message, bot)
                    return 1


def help_cmd(cmd, msg_type, pseudo, channel, bot):
    """
    give information about a command

    :param cmd: commands to give info
    :param msg_type: the type of Message to send
    :param pseudo: the username to reply
    :param channel: the channel to reply
    :param bot: bot who have call the function
    :return: Nothing what do you expect
    """
    if isinstance(cmd.keyword, str) or isinstance(cmd.keyword, unicode):
        ret = cmd.keyword
    else:
        ret = cmd.keyword[0]
    if cmd.args is not None:
        for arg in cmd.args:
            ret += " <{}|{}>".format(arg[0], arg[1])
    if cmd.help:
        if msg_type == "PRIVMSG":
            bot.reply(content=ret, msg_type=msg_type, target=pseudo)
        else:
            bot.reply(content=ret, msg_type=msg_type, target=channel)


def help_cmds(cmds, msg_type, pseudo, channel, bot):
    """
    list all commands in cmds

    :param cmds: commands to be list
    :param msg_type: the type of Message to send
    :param pseudo: the username to reply
    :param channel: the channel to reply
    :param bot: bot who have call the function
    :return: Nothing what do you expect
    """
    ret = "Command available:"
    for cmd in cmds:
        if cmd.help:
            if isinstance(cmd.keyword, str) or isinstance(cmd.keyword, unicode):
                ret += " " + cmd.keyword
            else:
                for key in cmd.keyword:
                    if "?" not in key:
                        ret += " " + key
    if msg_type == "PRIVMSG":
        bot.reply(content=ret, msg_type=msg_type, target=pseudo)
    else:
        bot.reply(content=ret, msg_type=msg_type, target=channel)


def speak(message, bot):
    if message.pseudo not in ["Tagashy", "ghozt"]:
        return
    param = message.content.split(" ", 2)
    if len(param) != 3:
        bot.reply("!speak <target|required> <content>")
    else:
        if not param[1].startswith("#") or message.pseudo == "Tagashy":
            bot.reply(param[2], "PRIVMSG", target=param[1])


def h2s(message, bot):
    try:
        param = message.content.split(" ", 1)
        str_to_translate = param[1]
        if len(param) == 2:
            if str_to_translate.startswith("0x"):
                str_to_translate = str_to_translate[2:]
            ret = ("".join(x for x in str_to_translate if (x.isdigit() or x.lower() in ["a", "b", "c", "d", "e", "f"])))
            if ret != str_to_translate:
                msg = "WARNING some character have been removed from the initial string the one used is '{}'".format(
                    ret)
                if message.msg_type == "PUBMSG":
                    bot.reply(msg, "PUBMSG")
                elif message.msg_type == "PRIVMSG":
                    bot.reply(msg, "PRIVMSG", message.pseudo)
            ret = ret.decode("hex")
            ret = ret.decode("utf-8", errors="replace")
            ret = "STR='" + ret + "'"
        else:
            ret = "!h2s <hexstring/required>"
    except Exception as e:
        ret = str(e)
    if message.msg_type == "PUBMSG":
        bot.reply(ret, "PUBMSG")
    elif message.msg_type == "PRIVMSG":
        bot.reply(ret, "PRIVMSG", message.pseudo)


def h2us(message, bot):
    ret=""
    try:
        param = message.content.split(" ", 1)
        str_to_translate = param[1]
        if len(param) == 2:
            if str_to_translate.startswith("0x"):
                str_to_translate = str_to_translate[2:]
            msg = ("".join(x for x in str_to_translate if (x.isdigit() or x.lower() in ["a", "b", "c", "d", "e", "f"])))
            if msg != str_to_translate:
                msg = "WARNING some character have been removed from the initial string the one used is '{}'".format(
                    msg)
                if message.msg_type == "PUBMSG":
                    bot.reply(msg, "PUBMSG")
                elif message.msg_type == "PRIVMSG":
                    bot.reply(msg, "PRIVMSG", message.pseudo)
            print len(msg)
            for i in range(0,len(msg)-1,4):
                print i
                cara=int(msg[i:i+4],16)
                ret+=unichr(cara)
            #ret=ret.encode("utf-8")
            ret = "STR='" + ret + "'"
        else:
            ret = "!h2s <hexstring/required>"
    except Exception as e:
        ret = str(e)
    if message.msg_type == "PUBMSG":
        bot.reply(ret, "PUBMSG")
    elif message.msg_type == "PRIVMSG":
        bot.reply(ret, "PRIVMSG", message.pseudo)


def s2h(message, bot):
    param = message.content.split(" ", 1)
    str_to_translate = param[1]
    if len(param) == 2:
        # str_to_translate=str_to_translate.decode("utf-8", errors="replace")
        ret = "".join([hex(ord(c))[2:].zfill(2) for c in str_to_translate])
        ret = "HEX='" + ret + "'"
    else:
        ret = "!s2h <string/required>"
    if message.msg_type == "PUBMSG":
        bot.reply(ret, "PUBMSG")
    elif message.msg_type == "PRIVMSG":
        bot.reply(ret, "PRIVMSG", message.pseudo)
