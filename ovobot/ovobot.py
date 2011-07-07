#!bin/python
# coding: utf8

import ircbot
from django.conf import settings
from ovobot.ovolog.models import *
import re



def do_parse(bot, channel, user, message):
    if re.match(r'\s*slaps\s+' + bot.c.get_nickname(), message):
        return u"ах ты сучка!"


class OVOBot(ircbot.SingleServerIRCBot, object):
    def __init__(self, server, port, nickname, channels):
        super(OVOBot, self).__init__( [(server, port)], nickname, nickname)
        self.nickname = nickname
        self._channels = channels

    def do_log(self, channel, user, type, message):
            obj = LogEntry(
                channel = channel,
                user = user,
                type = type,
                message = message,
            )
            obj.save()

    def do_pubmsg(self, channel, s, log=True):
        if s.startswith('/me '):
            self.c.action(channel, s.encode('utf-8').split(' ', 1)[-1].lstrip())
            if log:
                self.do_log(channel, self.c.get_nickname(), 'action', s)
        else:
            self.c.privmsg(channel, s.encode('utf-8'))
            if log:
                self.do_log(channel, self.c.get_nickname(), 'pubmsg', s)


    def on_welcome(self, c, e):
        self.c = c
        for channel in self._channels:
            c.join(channel)

    def _dispatcher(self, c, e):
        if settings.DEBUG:
            print e.eventtype()
            print e.source()
            print e.target()
            print e.arguments()
            print
        super(OVOBot, self)._dispatcher(c,e)

    def on_kick(self, c, e):
        whom = e.arguments()[0]
        who = e.arguments()[1]
        #print 'kicked %s by %s from %s' % (c.get_nickname(), who, e.target())
        if whom == c.get_nickname():
            #print 'rejoin in 60 sec'
            c.execute_delayed( 60, c.join, arguments=(e.target(),) )
        else:
            obj = LogEntry(
                channel = e.target(),
                user = e.source(),
                type = 'kick',
                message = 'kicked %s' % whom,
            )
            obj.save()


    def on_pubmsg(self, c, e):
        message = ''.join(e.arguments())
#        obj = LogEntry(
#            channel = e.target(),
#            user = e.source(),
#            type = 'pubmsg',
#            message = msg,
#        )
#        obj.save()
        self.do_log(e.target(), e.source(), 'pubmsg', message)
        out = do_parse(self, e.target(), e.source(), message)
        if out:
            self.do_pubmsg(e.target(), out)


    def on_action(self, c, e):
        message = ''.join(e.arguments())
#        obj = LogEntry(
#            channel = e.target(),
#            user = e.source(),
#            type = 'action',
#            message = msg,
#        )
#        obj.save()

        self.do_log(e.target(), e.source(), 'action', message)

        out = do_parse(self, e.target(), e.source(), message)
        if out:
            self.do_pubmsg(e.target(), out)



    def on_join(self, c, e):
#        obj = LogEntry(
#                channel = e.target(),
#                user = e.source(),
#                type = 'join',
#                message = 'joins',
#            )
#        obj.save()
        self.do_log(e.target(), e.source(), 'join', 'joins')

#        user = e.source()
#        cnt = LogEntry.objects.filter(user=user, type='action').count()
#        if cnt:
#            self.do_pubmsg(e.target(), u'еще один припёрся...')



bot = OVOBot( settings.IRC_SERVER, settings.IRC_PORT, settings.IRC_NICK, settings.IRC_CHANNELS)
bot.start()
