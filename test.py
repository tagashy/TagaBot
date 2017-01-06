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
reg=Message(target="#root-me-bot")
cr.start()
bot=TagaBot.Bot(cr,channel="#root-me-bot",server="irc.root-me.org",username="loulou")#transfert_class.Transferrer(cr,"#root-me-bot","loulou","irc.root-me.org")#RandomQuote.Troll(cr,"loulou","ghozt","irc.root-me.org","#root-me-bot")
cr.add_bot(reg,bot,channel="#root-me-bot",server="irc.root-me.org",bot_name="loulou")#,sock=sock)#channel="#root-me-bot",server="irc.root-me.org",bot_name="test")
#cr.join_channel("irc.root-me.org","loulou","#test")
#transfert_class.create_transferer(Message(content="!transfert irc.root-me.org #test"),bot)