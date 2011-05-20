from django.db import models

# Create your models here.
class LogEntry(models.Model):
    timestamp = models.DateTimeField('', auto_now_add=True)
    channel = models.CharField('channel', max_length=25)
    user = models.CharField('user', max_length=25)
    type = models.CharField('type', default='pubmsg', max_length=25)
    message = models.TextField('message')
    class Meta:
        pass

    def __unicode__(self):
        return u"%s at %s -> %s" % (self.user, self.timestamp, self.message)


        