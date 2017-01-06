# coding: utf8
from __future__ import unicode_literals

import message_parsing
import random
import transfert_class
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
        help_cmds(cmds, message.msg_type, message.pseudo, message.target,bot)
        print_message("[!] help called by " + message.pseudo)
        return 1
    for cmd in cmds:
        if isinstance(cmd.keyword, str) or isinstance(cmd.keyword, unicode):
            if message.content == cmd.keyword or message.content + "?" == cmd.keyword:
                if "?" in message:
                    help_cmd(cmd, message.msg_type, message.pseudo, message.target,bot)
                else:
                    print_message("[!] function " + cmd.name + " called by " + message.pseudo)
                    cmd.function(message, bot)
                return 1
        else:
            for key in cmd.keyword:
                if message.content.startswith(key + " ") or message.content == key or message.content + "?" == key:
                    if "?" in message.content:
                        help_cmd(cmd, message.msg_type, message.pseudo, message.target,bot)
                    else:
                        print_message("[!] function " + cmd.name + " called by " + message.pseudo)
                        cmd.function(message, bot)
                    return 1
                elif cmd.match and key in message.content:
                    if "?" in message.content:
                        help_cmd(cmd, message.msg_type, message.pseudo, message.target,bot)
                    else:
                        print_message("[!] function " + cmd.name + " called by " + message.pseudo)
                        cmd.function(message, bot)
                    return 1


def create_transferer(message, bot):
    """
    create a transfer

    :param message: commands line (message_parsing.Message)
    :param bot: the bot
    :return:
    """
    # geting_param
    ret = message_parsing.Message()
    num_genrator = random.Random()
    num_genrator.seed()
    param = message.content.split()
    if len(param) >= 3:
        addr = param[1]
        server_addr = addr.split(":")
        if len(server_addr) == 1:
            server_addr = addr
            port = 6667
        elif len(server_addr) == 2:
            port = int(server_addr[1])
            server_addr = server_addr[0]
        else:
            print_message("too much :", message.msg_type, message.pseudo, message.target)
            return
        channel = param[2]
        # check existence:
        # create bot
        # transfert_class.Transferrer(bot.dispatcher,)
        bot.add_bot(message_parsing.Message(server=server_addr, target=channel), transfert_class.Transferrer,
                    server=server_addr, channel=channel,
                    bot_name="user_" + str(num_genrator.randint(1000, 1000 * 1000)), sock=sock)


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
        bot.reply(content=ret, msg_type=msg_type, target=channel, pseudo=pseudo)


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
    bot.reply(content=ret, msg_type=msg_type, target=channel, pseudo=pseudo)
