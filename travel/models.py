from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import get_thumbnail
from adminsortable.models import SortableMixin
from django.utils.encoding import python_2_unicode_compatible

from .includes.exif import Exif


class WorldPlace(models.Model):
  TYPE = (
    ('been', 'Been'),
    ('plan', 'Plan'),
    ('home', 'Home'),
  );
  name = models.CharField(max_length = 196)
  type = models.CharField(max_length = 4, choices = TYPE)
  latitude = models.DecimalField(max_digits = 17, decimal_places = 14)
  longitude = models.DecimalField(max_digits = 17, decimal_places = 14)
  

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

  type = models.CharField(max_length = 196)
  name = models.CharField(max_length = 196)
  name_en = models.CharField(max_length = 196, null = True, blank = True)
  search = models.CharField(max_length = 196, null = True, blank = True)
  icon = models.URLField(null = True, blank = True)
  address = models.TextField()
  latitude = models.DecimalField(max_digits = 17, decimal_places = 14)
  longitude = models.DecimalField(max_digits = 17, decimal_places = 14)

  # travel_type = models.CharField(max_length = 7, choices = TRAVEL_TYPE, null = True, blank = True)
  # transit_no = models.CharField(max_length = 19, null = True, blank = True)
  # transit_time = models.TimeField(null = True, blank = True)
  # transit_arrive_time = models.TimeField(null = True, blank = True)
  # transit_ticket_price = models.DecimalField(max_digits = 9, decimal_places = 2, null = True, blank = True)

  plan_date = models.DateField(null = True, blank = True)
  plan_time = models.CharField(max_length = 9, choices = PLAN_TIME, null = True, blank = True)

  added_at = models.DateTimeField()
  sort = models.PositiveIntegerField(default = 0, editable = False, db_index = True)

  

  class Meta:
    ordering = ['sort']

  def __str__(self):
    return self.name + ' @ ' + str(self.plan_date) + ' ' + str(self.plan_time)
  

class TravelConstraint(models.Model):
  TYPE = (
    ('departure-before', 'Must departure before'),
    ('departure-after', 'Must departure after'),
    ('arrive-before', 'Must arrive before'),
    ('arrive-after', 'Must arrive after'),
  );

  type = models.CharField(max_length = 16, choices = TYPE)
  time = models.TimeField()
  place = models.ForeignKey(Place)


class Transit(models.Model):
  # TYPE = (
  #   ('driving', 'Driving'),
  #   ('walking', 'Walking'),
  #   ('train', 'Train'),
  #   ('public', 'Public transport'),
  #   ('flight', 'Flight'),
  #   ('ferry', 'Ferry'),
  # );

  STATUS = (
    ('decided', 'Decided'),
    ('yet-decided', 'Yet decided'),
  )

  # type = models.CharField(max_length = 7, choices = TYPE)
  status = models.CharField(max_length = 11, choices = STATUS)
  # no = models.CharField(max_length = 19, null = True, blank = True)
  # no_en = models.CharField(max_length = 19, null = True, blank = True)
  # departure_time = models.TimeField(null = True, blank = True)
  # arrive_time = models.TimeField(null = True, blank = True)
  ticket_price = models.DecimalField(max_digits = 9, decimal_places = 2, null = True, blank = True)
  a = models.OneToOneField(Place, related_name = 'from+')
  b = models.OneToOneField(Place, related_name = 'to+')


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
    











