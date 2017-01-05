from django.contrib import admin

from .models import GroundFloorTimber, Category, Page, Link


class GroundFloorTimberAdmin(admin.ModelAdmin):
  list_display = ('name', 'image_thumbnail', 'added_at')
  search_fields = ['name']

class CategoryAdmin(admin.ModelAdmin):
  list_display = ('name', 'link')
  search_fields = ['name', 'link']

class PageAdmin(admin.ModelAdmin):
  list_display = ('name', 'user', 'modified_at')
  search_fields = ['name', 'content']

class LinkAdmin(admin.ModelAdmin):
  list_display = ('name', 'link_text', 'type', 'link_to')
  search_fields = ['name', 'link_text']

  def link_to(self, obj):
    if obj.type == 'c':
      return obj.category
    elif obj.type == 'p':
      return obj.page
    elif obj.type == 'e':
      return obj.url

admin.site.register(GroundFloorTimber, GroundFloorTimberAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Link, LinkAdmin)