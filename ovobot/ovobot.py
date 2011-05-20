#!bin/python
# coding: utf8

import ircbot
from django.conf import settings
from ovobot.ovolog.models import *



class OVOBot(ircbot.SingleServerIRCBot, object):
    def __init__(self, server, port, nickname, channels):
        super(OVOBot, self).__init__( [(server, port)], nickname, nickname)
        self.nickname = nickname
        self._channels = channels

    def on_welcome(self, c, e):
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
                message = 'kicked by %s' % who,
            )
            obj.save()


    def on_pubmsg(self, c, e):
        obj = LogEntry(
            channel = e.target(),
            user = e.source(),
            type = 'pubmsg',
            message = ''.join(e.arguments()),
        )
        obj.save()

    def on_action(self, c, e):
        obj = LogEntry(
            channel = e.target(),
            user = e.source(),
            type = 'action',
            message = ''.join(e.arguments()),
        )
        obj.save()

    def on_join(self, c, e):
        obj = LogEntry(
                channel = e.target(),
                user = e.source(),
                type = 'join',
                message = 'joins',
            )
        obj.save()


bot = OVOBot( settings.IRC_SERVER, settings.IRC_PORT, settings.IRC_NICK, settings.IRC_CHANNELS)
bot.start()
