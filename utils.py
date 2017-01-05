from __future__ import unicode_literals

import re
from socket import *

from users import User


class ConnectionError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Unable to establish connection due to error {}".format(self.value)


def clean(string):
    assert isinstance(string, str) or isinstance(string, unicode)
    return string.replace("..", "").replace("/", "").replace("\b", "").replace("\n", "").replace("\r", "")


def create_irc_socket(addr, bot_name, channel, users_list, port=6667):
    name_list_reg = re.compile("(?<= 353 {} = {} :).*".format(bot_name, channel))
    users = []
    recv_sock = socket(AF_INET, SOCK_STREAM)
    recv_sock.connect((addr, port))
    recv_sock.send("USER {} Bot Bot Bot\r\n".format(bot_name))
    recv_sock.send("NICK {} \r\n".format(bot_name))
    res = ""
    print_message("[!] Authentification to {} send".format(addr))
    recv_sock.settimeout(2)
    try:
        while 1:
            res = recv_sock.recv(1024).decode('utf-8', errors='replace')
            if "[Throttled]" in res:
                raise ConnectionError("Throttled")
            elif "[Registration timeout]" in res:
                raise ConnectionError("Registration Timeout")
            elif "ERROR :Closing link:" in res:
                raise ConnectionError("Closing Link")
    except timeout:
        recv_sock.send("JOIN {} \r\n".format(channel))
        recv_sock.settimeout(None)
        print_message("[!] join {}".format(channel))
    while " 366 " not in res:
        res = recv_sock.recv(1024).decode('utf-8', errors='replace')
        if " 353 " in res:
            print_message("[!] creation of user list")
            users += parse_name_list(res, name_list_reg, channel, "{}:{}".format(addr, port))
            for user in users:
                users_list.add_user(user, "{}:{}".format(addr, port), channel)
    return recv_sock


def print_message(message, msg_type="STDIN", sock=None, pseudo=None, channel=None):
    if msg_type == "PRIVMSG":
        send_private_message(message, pseudo, sock)
    elif msg_type == "PUBMSG":
        send_private_message(message, channel, sock)
    elif msg_type == "STDIN":
        print (message)


def send_private_message(message, pseudo, sock):
    sock.send("PRIVMSG {} :{}\r\n".format(pseudo, message))


def parse_name_list(msg, name_list_reg, channel="UNKNOWN", server="UNKNOWN"):
    name_list_res = name_list_reg.search(msg)
    if name_list_res:
        name_list = name_list_res.group(0)
        names = name_list.split()
        users = []
        for name in names:
            users.append(User(name, channel, server))
        return users
    return []


def cut_at_cara(string, c):
    index = string.find(c)
    if index != -1:
        return string[index + 1:]
    else:
        return string


def convert_html_to_uni(text):
    htmlcodes = ['&Aacute;', '&aacute;', '&Agrave;', '&Acirc;', '&agrave;', '&Acirc;', '&acirc;', '&Auml;', '&auml;',
                 '&Atilde;', '&atilde;', '&Aring;', '&aring;', '&Aelig;', '&aelig;', '&Ccedil;', '&ccedil;', '&Eth;',
                 '&eth;', '&Eacute;', '&eacute;', '&Egrave;', '&egrave;', '&Ecirc;', '&ecirc;', '&Euml;', '&euml;',
                 '&Iacute;', '&iacute;', '&Igrave;', '&igrave;', '&Icirc;', '&icirc;', '&Iuml;', '&iuml;', '&Ntilde;',
                 '&ntilde;', '&Oacute;', '&oacute;', '&Ograve;', '&ograve;', '&Ocirc;', '&ocirc;', '&Ouml;', '&ouml;',
                 '&Otilde;', '&otilde;', '&Oslash;', '&oslash;', '&szlig;', '&Thorn;', '&thorn;', '&Uacute;',
                 '&uacute;', '&Ugrave;', '&ugrave;', '&Ucirc;', '&ucirc;', '&Uuml;', '&uuml;', '&Yacute;', '&yacute;',
                 '&yuml;', '&copy;', '&reg;', '&trade;', '&euro;', '&cent;', '&pound;', '&lsquo;', '&rsquo;', '&ldquo;',
                 '&rdquo;', '&laquo;', '&raquo;', '&mdash;', '&ndash;', '&deg;', '&plusmn;', '&frac14;', '&frac12;',
                 '&frac34;', '&times;', '&divide;', '&alpha;', '&beta;', '&infin']
    funnychars = ['\xc1', '\xe1', '\xc0', '\xc2', '\xe0', '\xc2', '\xe2', '\xc4', '\xe4', '\xc3', '\xe3', '\xc5',
                  '\xe5', '\xc6', '\xe6', '\xc7', '\xe7', '\xd0', '\xf0', '\xc9', '\xe9', '\xc8', '\xe8', '\xca',
                  '\xea', '\xcb', '\xeb', '\xcd', '\xed', '\xcc', '\xec', '\xce', '\xee', '\xcf', '\xef', '\xd1',
                  '\xf1', '\xd3', '\xf3', '\xd2', '\xf2', '\xd4', '\xf4', '\xd6', '\xf6', '\xd5', '\xf5', '\xd8',
                  '\xf8', '\xdf', '\xde', '\xfe', '\xda', '\xfa', '\xd9', '\xf9', '\xdb', '\xfb', '\xdc', '\xfc',
                  '\xdd', '\xfd', '\xff', '\xa9', '\xae', '\u2122', '\u20ac', '\xa2', '\xa3', '\u2018', '\u2019',
                  '\u201c', '\u201d', '\xab', '\xbb', '\u2014', '\u2013', '\xb0', '\xb1', '\xbc', '\xbd', '\xbe',
                  '\xd7', '\xf7', '\u03b1', '\u03b2', '\u221e']
    for i in range(len(htmlcodes)):
        htmlcode = htmlcodes[i]
        text = text.replace(htmlcode, funnychars[i])
    return text


def parse_html_balise(balise, text):
    assert (isinstance(balise, str) or isinstance(balise, unicode)) and (
        isinstance(text, str) or isinstance(text, unicode))

    if balise.startswith(u"<"):
        balise_name = balise.split()[0][1:]
        balise_end = u"</{}>".format(balise_name)
    else:
        balise_name = balise
        balise = u"<{}".format(balise_name)
        balise_end = u"</{}>".format(balise_name)

    start_index = text.index(balise)
    end_index = text.index(balise_end)
    part_text = text[start_index:end_index]
    start_index = part_text.index(">")
    return part_text[start_index + 1:]
