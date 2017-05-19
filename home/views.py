import logging

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse

from .includes.serializer import ExtJsonSerializer
from .models import GroundFloorTimber, Category, Page, PageSection, Link
from travel.models import Photo


def get_index(request):
  return render(request, 'home/index.html', {
    'ground_floor_timber': GroundFloorTimber.objects.order_by('?').first(),
    'nav_links': Link.objects.all(),
  })

def get_index_photos(request):
  photos = Photo.objects.order_by('-added_at')[:10]
  return HttpResponse(ExtJsonSerializer().serialize(photos, 
    fields = ['name', 'image_thumbnail', 'image_size', 'original_image_url', 'stylish_image_url']))

def get_page(request, page):
  page = get_object_or_404(Page, link = page)
  page_sections = PageSection.objects.filter(page = page)
  return render(request, 'home/page.html', {
    'page': page,
    'page_sections': page_sections,
    'nav_links': Link.objects.all(),
  })

def get_category(request, category, page = None):
  # categories / top-level pages
  if page is None:
    try:
      category = Category.objects.get(link = category)
      return render(request, 'home/category.html', {
        'ground_floor_timber': GroundFloorTimber.objects.order_by('?').first(),
        'nav_links': Link.objects.all(),
        'category': category,
      })

    except (KeyError, Category.DoesNotExist):
      return get_page(request, category)

  # pages
  else:
    return get_page(request, page)
  
def get_category_pages(request, category):
  category = Category.objects.get(link = category)
  pages = Page.objects.filter(category = category)
  return HttpResponse(ExtJsonSerializer().serialize(pages, 
    fields = ['name', 'link', 'category.link', 'image_thumbnail', 'image_size']))




