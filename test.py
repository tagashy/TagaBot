import IRC
import dispatcher
import controler
from message_parsing import message
import utils
import RandomQuote
import transfert_class
import TagaBot
cr=controler.Controler()
reg=message(pseudo="Tagashy",msg_type="PRIVMSG")
cr.start()
bot=RandomQuote.troll(cr,"loulou","Tagashy","irc.root-me.org","#root-me-bot")
cr.add_bot(reg,bot,channel="#root-me-bot",server="irc.root-me.org",bot_name="loulou")#,sock=sock)#channel="#root-me-bot",server="irc.root-me.org",bot_name="test")
