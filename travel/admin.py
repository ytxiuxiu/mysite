# coding=utf-8

from django.contrib import admin
from adminsortable.admin import SortableAdmin

from .models import Photo, Place, TravelConstraint, WorldPlace


class WorldPlaceAdmin(admin.ModelAdmin):
  list_display = ('name', 'type')

class PhotoAdmin(admin.ModelAdmin):
  list_display = ('admin_thumbnail', 'name', 'user', 'added_at', 
    'size', 'parameters', 'time') // 'device', 'lens', 'coordinate', 
  search_fields = ['name', 'description']

  def device(self, obj):
    return obj.image_exif().device()

  def coordinate(self, obj):
    return obj.image_exif().coordinate()

  def size(self, obj):
    if obj.stylish_image_size():
        size = obj.stylish_image_size()
    else:
        size = obj.original_image_size()
    return '{0} × {1}'.format(size[0], size[1])

  def lens(self, obj):
    return obj.image_exif().lens()

  def parameters(self, obj):
    exif = obj.image_exif()
    return 'f/{0} 1/{1} {2}mm ISO{3}'.format(
        exif.aperture(), exif.exposure(), exif.focal_length(), exif.iso()
    )

  def time(self, obj):
    return obj.image_exif().time();

class TravelConstraintInline(admin.StackedInline):
    model = TravelConstraint
    extra = 3

class PlaceAdmin(SortableAdmin):
  list_display = ('name', 'name_en', 'search', 'plan_date', 'plan_time', 'type')

  inlines = [TravelConstraintInline]


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(WorldPlace, WorldPlaceAdmin)