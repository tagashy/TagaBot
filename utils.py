# coding: utf8
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
    """
    clean a string from potentially anoying character
    :param string: the string to remove character
    :return: the string whithout those caracter character
    """
    assert isinstance(string, str) or isinstance(string, unicode)
    return string.replace("..", "").replace("/", "").replace("\b", "").replace("\n", "").replace("\r", "")


def create_irc_socket(addr, bot_name, channel, users_list, port=6667):
    """
    create a socket and authenticate to server
    :param addr: address of the server to connect to
    :param bot_name: the name of the user to authenticate with
    :param channel: the channel to join
    :param users_list: the list of user to store the user of the channel (must be users object or expose a add_user method with 3 parameter)
    :param port: the port of the server to connect to (must be cleartext SSL not supported for now)
    :return: socket (connected to server)
    """
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
    """
    old method to send message on IRC server or STDIN
    :param message: the content to write
    :param msg_type: the type of the message (STDIN/PUBMSG/PRIVMSG)
    :param sock: the socket to send message over
    :param pseudo: the pseudo to send message (used if message is PRIVMSG)
    :param channel: the channel to send message (used if message is PUBMSG)
    :return: Nothing what did you expect
    """
    if msg_type == "PRIVMSG":
        send_private_message(message, pseudo, sock)
    elif msg_type == "PUBMSG":
        send_private_message(message, channel, sock)
    elif msg_type == "STDIN":
        print (message)


def send_private_message(message, pseudo, sock):
    """
    send a private message to a user/channel
    :param message: the content to wrtie
    :param pseudo: the pseudo of the user/channel
    :param sock: the socket to send message over
    :return: Nothing what did you expect
    """
    sock.send("PRIVMSG {} :{}\r\n".format(pseudo, message))


def parse_name_list(msg, name_list_reg, channel="UNKNOWN", server="UNKNOWN"):
    """
    convert a 351 message (user connected to channel) to a user list
    :param msg: the message received (str)
    :param name_list_reg: the regex to use
    :param channel: the channel of the server
    :param server: the address of the server
    :return: users list
    """
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
    """
    cut a string at a character and return the content without all character previous to this one
    :param string: the string to cut
    :param c: the character to cut at
    :return: string whitout the part previous to he character
    """
    index = string.find(c)
    if index != -1:
        return string[index + 1:]
    else:
        return string


def convert_html_to_uni(text):
    """
    convert html character to their unicode version
    :param text: the text to convert
    :return: the text converted
    """
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
    """
    get the text of the html-like balise (XML should also work but not tested)
    :param balise: the balise to get
    :param text: the text to search for this balise
    :return: the content of the balise
    """
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
