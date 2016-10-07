from itertools import chain

from django.db import models
from django.contrib.postgres import fields
from django.utils import timezone
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.TextField(blank=False, help_text='Title of the article.')
    text = models.TextField(blank=False, help_text='Content of the article.')
    short = models.TextField(blank=False, help_text='Few first lines of the article.')
    author = models.ForeignKey(to=User, help_text='Author of the article.')
    created = models.DateTimeField(default=timezone.now, blank=True, help_text='Time of creation')
    publication_date = models.DateTimeField(default=timezone.now, blank=False,
                                            help_text='Time of publication, can be feature.')
    tags = fields.ArrayField(models.CharField(max_length=100), blank=True)

    def add_tags(self, *tags_to_add: str):
        """
        :param tags_to_add: Tag or tags to add to existing tags.
        """
        self.tags = list({tag for tag in chain(self.tags, tags_to_add)})

    def remove_tags(self, *tags_to_remove: str):
        """
        :param tags_to_remove: Tag or tags to remove from existing tags
        """
        self.tags = list({tag for tag in self.tags if tag not in tags_to_remove})

    def published(self) -> bool:
        return timezone.now() > self.publication_date

    def __str__(self):
        return self.title
