from itertools import chain
from typing import List

from django.db import models
from django.contrib.postgres import fields
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify
from django.db.models import signals


from comments.models import Comment


class Article(models.Model):
    title = models.TextField(blank=False, help_text='Title of the article.')
    content = models.TextField(blank=False, help_text='Content of the article.')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, help_text='Author of the article.')
    timestamp = models.DateTimeField(auto_now_add=True, help_text='Time of creation')
    updated = models.DateTimeField(auto_now_add=True)
    publication_date = models.DateTimeField(default=timezone.now, blank=False,
                                            help_text='Time of publication, can be feature.')
    slug = models.SlugField(unique=True)
    tags = fields.ArrayField(models.CharField(max_length=100), blank=True)

    class Meta:
        ordering = ['-timestamp', '-updated']

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

    @property
    def published(self) -> bool:
        return timezone.now() > self.publication_date

    @property
    def comments(self) -> List[Comment]:
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return list(qs)

    def __str__(self):
        return self.title


def create_slug(instance: Article, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Article.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        new_slug = '{}-{}'.format(slug, qs.first().id+1)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_article_receiver(sender, instance: Article, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


signals.pre_save.connect(pre_save_article_receiver, sender=Article)



