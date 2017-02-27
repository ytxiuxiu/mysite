import logging

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse

from .includes.serializer import ExtJsonSerializer
from .models import GroundFloorTimber, Category, Page, Link
from .serializers import PageSerializer
from travel.models import Photo


def index(request):
  if not request.is_ajax():
    return render(request, 'home/index.html', {
      'ground_floor_timber': GroundFloorTimber.objects.order_by('?').first(),
      'nav_links': Link.objects.all(),
    })
  else:
    photos = Photo.objects.order_by('-added_at')[:10]
    return HttpResponse(ExtJsonSerializer().serialize(photos, 
      fields = ['name', 'image_thumbnail', 'image_size']))

def page(request, category, page):
  page = get_object_or_404(Page, link = page)
  return render(request, 'home/page.html', {
    'page': page,
    'nav_links': Link.objects.all(),
  })

def category(request, category):
  try:
    category = Category.objects.get(link = category)
  except (KeyError, Category.DoesNotExist):
    page = get_object_or_404(Page, link = category)
    return render(request, 'home/page.html', {
      'page': page,
      'nav_links': Link.objects.all(),
    })
  
  if not request.is_ajax():
    # category page
    return render(request, 'home/category.html', {
      'ground_floor_timber': GroundFloorTimber.objects.order_by('?').first(),
      'nav_links': Link.objects.all(),
      'category': category,
    })
  else:
    # ajax pages in category
    pages = Page.objects.filter(category = category)
    return HttpResponse(ExtJsonSerializer().serialize(pages, 
      fields = ['name', 'link', 'category.link', 'image_thumbnail', 'image_size']))




