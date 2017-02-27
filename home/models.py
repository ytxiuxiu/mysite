from __future__ import unicode_literals

from django.db import models
from sorl.thumbnail import get_thumbnail
from ckeditor_uploader.fields import RichTextUploadingField
from adminsortable.models import SortableMixin
from django.utils.encoding import python_2_unicode_compatible

from django.contrib.auth.models import User


@python_2_unicode_compatible
class GroundFloorTimber(models.Model):
  name = models.CharField(max_length = 192, null = True, blank = True)
  image = models.ImageField(upload_to = 'ground-floor-timber')
  added_at = models.DateTimeField()

  def image_thumbnail(self):
    if self.image:
      thumbnail = get_thumbnail(self.image, '125x125')
      return u'<image src="%s">' % thumbnail.url
    else:
      return u'-'
  image_thumbnail.short_description = 'Thumb'
  image_thumbnail.allow_tags = True

  def __str__(self):
    if self.name:
      return self.name
    else:
      return 'Image'

@python_2_unicode_compatible
class Category(models.Model):
  name = models.CharField(max_length = 192)
  link = models.CharField(max_length = 192)
  desc = RichTextUploadingField(null = True, blank = True)

  def __str__(self):
    return self.name

@python_2_unicode_compatible
class Page(models.Model):
  CONTENT_WIDTH = (
    ('2', '2'),
    ('4', '4'),
    ('6', '6'),
    ('8', '8'),
    ('10', '10'),
    ('12', '12'),
  )

  name = models.CharField(max_length = 192)
  link = models.CharField(max_length = 192)
  cover_image = models.ImageField(upload_to = 'page-cover', null = True, blank = True)
  content = RichTextUploadingField()
  content_width = models.CharField(max_length = 2, choices = CONTENT_WIDTH, default = 12)
  user = models.ForeignKey(User)
  category = models.ForeignKey(Category, null = True, blank = True)
  created_at = models.DateTimeField()
  modified_at = models.DateTimeField()

  @property
  def image_thumbnail(self):
    return self.thumbnail_url()

  @property
  def image_size(self):
    if self.cover_image:
      return self.cover_image.width, self.cover_image.height

  def thumbnail_url(self, width = 800, height = 800):
    size = '{0}x{1}'.format(width, height)
    if self.cover_image:
      thumbnail = get_thumbnail(self.cover_image, size)
      return thumbnail.url

  def __str__(self):
    return self.name

@python_2_unicode_compatible
class Link(SortableMixin):
  TARGET = (
    ('_blank', 'New window/tab'),
    ('_self', 'Current window'),
  )
  TYPE = (
    ('p', 'Page'),
    ('c', 'Category'),
    ('e', 'External'),
  )

  name = models.CharField(max_length = 192)
  link_text = models.CharField(max_length = 192)
  target = models.CharField(max_length = 7, choices = TARGET, default = '_self')
  type = models.CharField(max_length = 1, choices = TYPE, default = 'c')
  url = models.CharField(max_length = 255, null = True, blank = True)
  category = models.ForeignKey(Category, related_name = 'link_category', null = True, blank = True)
  page = models.ForeignKey(Page, related_name = 'link_category', null = True, blank = True)
  sort = models.PositiveIntegerField(default = 0, editable = False, db_index = True)

  class Meta:
    ordering = ['sort']

  def __str__(self):
    return self.name




