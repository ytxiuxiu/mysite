from .models import Page
from .models import Category
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ('name', 'link', 'pages')

class PageSerializer(serializers.ModelSerializer):
  category = CategorySerializer(read_only = True)

  class Meta:
    model = Page
    fields = ('name', 'link', 'category')