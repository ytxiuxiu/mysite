from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import get_thumbnail
from adminsortable.models import SortableMixin
from django.utils.encoding import python_2_unicode_compatible

from .includes.exif import Exif


@python_2_unicode_compatible
class Place(SortableMixin):
  PLAN_TIME = (
    ('allday', 'All day'),
    ('midnight', 'Midnight'),
    ('dawn', 'Dawn'),
    ('morning', 'Morning'),
    ('noon', ' Noon'),
    ('afternoon', 'Afternoon'),
    ('dust', 'Dust'),
    ('evening', 'Evening'),
  );

  name = models.CharField(max_length = 196, null = True, blank = True)
  plan_date = models.DateField()
  plan_time = models.CharField(max_length = 9, choices = PLAN_TIME, null = True, blank = True)
  visited_at = models.DateTimeField(null = True, blank = True)
  added_at = models.DateTimeField()
  sort = models.PositiveIntegerField(default = 0, editable = False, db_index = True)

  class Meta:
    ordering = ['sort']

  def __str__(self):
    return self.name + ' @ ' + str(self.plan_date) + ' ' + str(self.plan_time)
  

class Photo(models.Model):
  name = models.CharField(max_length = 196, null = True, blank = True)
  description = models.TextField(null = True, blank = True)
  user = models.ForeignKey(User)
  original_image = models.ImageField(upload_to = 'travel/photo')
  stylish_image = models.ImageField(upload_to = 'travel/photo', null = True, blank = True)
  added_at = models.DateTimeField()

  @property
  def image_thumbnail(self):
    return self.thumbnail_url()

  @property
  def image_size(self):
    if self.stylish_image:
      return self.stylish_image_size()
    else:
      return self.original_image_size()


  def admin_thumbnail(self):
    thumbnail_url = self.thumbnail_url(125, 125)
    return '<image src="{0}">'.format(thumbnail_url)

  admin_thumbnail.short_description = 'Thumb'
  admin_thumbnail.allow_tags = True


  def original_image_size(self):
    return self.original_image.width, self.original_image.height

  def stylish_image_size(self):
    if self.stylish_image:
      return self.stylish_image.width, self.stylish_image.height

  def thumbnail_url(self, width = 800, height = 800):
    size = '{0}x{1}'.format(width, height)
    if self.stylish_image:
      thumbnail = get_thumbnail(self.stylish_image, size)
      return thumbnail.url
    elif self.original_image:
      thumbnail = get_thumbnail(self.original_image, size)
      return thumbnail.url

  def image_exif(self):
    return Exif(self.original_image)
    











