# coding: utf8
import IRC
import dispatcher
import controller
from message_parsing import Message
import utils
import RandomQuote
import transfert_class
import TagaBot
cr=controller.Controller()
reg=Message(pseudo="ghozt", msg_type="PRIVMSG")
cr.start()
bot=TagaBot.Bot(cr,)#RandomQuote.Troll(cr,"loulou","ghozt","irc.root-me.org","#root-me-bot")
cr.add_bot(reg,bot,channel="#root-me-bot",server="irc.root-me.org",bot_name="loulou")#,sock=sock)#channel="#root-me-bot",server="irc.root-me.org",bot_name="test")
cr.add_bot_listener()