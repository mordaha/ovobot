from django.db import models
import socket

# Create your models here.
class LogEntry(models.Model):
    timestamp = models.DateTimeField('', auto_now_add=True)
    channel = models.CharField('channel', max_length=25)
    user = models.CharField('user', max_length=25)
    type = models.CharField('type', default='pubmsg', max_length=25)
    message = models.TextField('message')

    #auto fields
    user_ip = models.CharField('ip', max_length=16)
    nick = models.CharField('nick', max_length=25)

    class Meta:
        pass

    def __unicode__(self):
        return u"%s at %s -> %s" % (self.user, self.timestamp, self.message)

    def get_nick(self):
        return self.user.split('!', 1)[0]

    def save(self, *args, **kwargs):
        
        try:
            host = self.user.split('@', 1)[1]
            ai = socket.getaddrinfo(host, None)
            self.user_ip = ai[0][4][0]
        except (IndexError, socket.gaierror):
            pass

        self.nick = self.get_nick()

        super(LogEntry, self).save(*args, **kwargs)
        