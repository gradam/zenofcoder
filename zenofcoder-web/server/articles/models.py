from typing import List, Union

from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify


from comments.models import Comment


class Tag(models.Model):
    tag = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return '{}'.format(self.tag)


class Article(models.Model):
    title = models.TextField(blank=False, help_text='Title of the article.')
    content = models.TextField(blank=False, help_text='Content of the article.')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, help_text='Author of the article.')
    timestamp = models.DateTimeField(auto_now_add=True, help_text='Time of creation')
    updated = models.DateTimeField(auto_now_add=True)
    publication_date = models.DateTimeField(default=timezone.now, blank=False,
                                            help_text='Time of publication, can be feature.')
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['-timestamp', '-updated']

    __original_title = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_title = self.title

    def save(self, *args, **kwargs):
        if self.pk is None or self.title != self.__original_title:
            slug = create_slug(self.title)
            self.slug = slug
        super().save(*args, **kwargs)
        self.__original_title = self.title

    def add_tags(self, *tags_to_add: str):
        for tag in tags_to_add:
            self.tags.add(Tag.objects.get_or_create(tag=tag)[0])

    def remove_tags(self, *tags_to_remove):
        qs = Tag.objects.filter(tag__in=tags_to_remove)
        self.tags.remove(*qs)

    @property
    def contain_tags(self, tags):
        if set(tags).issubset(self.tags):
            return True
        return False


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


def create_slug(title: Union[str, models.TextField], new_slug=None):
    slug = slugify(title)
    if new_slug is not None:
        slug = new_slug
    qs = Article.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        latest = Article.objects.filter(title=title).order_by('slug')[0]
        try:
            number = int(latest.slug.split('-')[-1])
        except ValueError:
            number = 1
        new_slug = '{}-{}'.format(slug, number+1)
        return create_slug(title, new_slug=new_slug)
    return slug
