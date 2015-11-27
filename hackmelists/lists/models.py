from __future__ import unicode_literals

from django.db import models

class ListItem(models.Model):
    text = models.CharField(max_length=256)
    def __unicode(self):
        return self.text
