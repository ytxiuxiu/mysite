from django.core.serializers.base import Serializer as BaseSerializer
from django.core.serializers.python import Serializer as PythonSerializer
from django.core.serializers.json import Serializer as JsonSerializer

class ExtBaseSerializer(BaseSerializer):

  def serialize_property(self, obj):
    model = type(obj)
    for field in self.selected_fields:
      path = field.split('.')
      self.handle_prop(obj, path, field)

  def handle_prop(self, obj, path, field):
    model = type(obj)
    #print 'model', model, 'path', path, 'feild', field
    #print 'hasattr(model, path[0])', hasattr(model, path[0]), 'type(getattr(model, path[0]))', type(getattr(model, path[0]))
    if hasattr(model, path[0]):
      self._current[field] = getattr(obj, path[0])
      #print 'self._current[field]', self._current[field]
    else:
      raise KeyError('Field `' + path[0] + '` doesn\'t exists in the model `' + str(model) + '`')

    if len(path) > 1:
      del path[0]
      #print 'path', path
      self.handle_prop(self._current[field], path, field)

  def end_object(self, obj):
    self.serialize_property(obj)

    super(ExtBaseSerializer, self).end_object(obj)


class ExtPythonSerializer(ExtBaseSerializer, PythonSerializer):
  pass


class ExtJsonSerializer(ExtPythonSerializer, JsonSerializer):
  pass