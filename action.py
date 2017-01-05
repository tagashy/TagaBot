from __future__ import unicode_literals

from utils import print_message


class Command:
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


def command_loop(message, sock, cmds, controler):
    if "!help" == message.content:
        help_cmds(cmds, message.msg_type, message.pseudo, sock, message.target)
        print_message("[!] help called by " + message.pseudo)
        return 1
    for cmd in cmds:
        if isinstance(cmd.keyword, str) or isinstance(cmd.keyword, unicode):
            if message.content == cmd.keyword or message.content + "?" == cmd.keyword:
                if "?" in message:
                    help_cmd(cmd, message.msg_type, message.pseudo, sock, message.target)
                else:
                    print_message("[!] function " + cmd.name + " called by " + message.pseudo)
                    cmd.function(message, sock, controler)
                return 1
        else:
            for key in cmd.keyword:
                if message.content.startswith(key + " ") or message.content == key or message.content + "?" == key:
                    if "?" in message.content:
                        help_cmd(cmd, message.msg_type, message.pseudo, sock, message.target)
                    else:
                        print_message("[!] function " + cmd.name + " called by " + message.pseudo)
                        cmd.function(message, sock, controler)
                    return 1
                elif cmd.match and key in message.content:
                    if "?" in message.content:
                        help_cmd(cmd, message.msg_type, message.pseudo, sock, message.target)
                    else:
                        print_message("[!] function " + cmd.name + " called by " + message.pseudo)
                        cmd.function(message, sock, controler)
                    return 1


def create_transferer(message, sock, controler):
    # geting_param
    import transfert_class, message_parsing, random
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
            print_message("too much :", message.msg_type, sock, message.pseudo, message.target)
            return
        channel = param[2]
        # check existence:
        #create bot
        controler.add_bot(message_parsing.message(server=server_addr, target=channel), transfert_class.Transferrer,
                          server=server_addr, channel=channel,
                          bot_name="user_" + str(num_genrator.randint(1000, 1000 * 1000)), sock=sock)


def help_cmd(cmd, msg_type, pseudo, sock, channel):
    if isinstance(cmd.keyword, str) or isinstance(cmd.keyword, unicode):
        ret = cmd.keyword
    else:
        ret = cmd.keyword[0]
    if cmd.args is not None:
        for arg in cmd.args:
            ret += " <{}|{}>".format(arg[0], arg[1])
    if cmd.help:
        print_message(ret, msg_type, sock, pseudo, channel)


def help_cmds(cmds, msg_type, pseudo, sock, channel):
    ret = "Command available:"
    for cmd in cmds:
        if cmd.help:
            if isinstance(cmd.keyword, str) or isinstance(cmd.keyword, unicode):
                ret += " " + cmd.keyword
            else:
                for key in cmd.keyword:
                    if "?" not in key:
                        ret += " " + key
    print_message(ret, msg_type, sock, pseudo, channel)
