from django.http import HttpResponse
from django.core.exceptions import ImproperlyConfigured
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import six

# Django 1.5+ compat
try:
    import json
except ImportError:  # pragma: no cover
    from django.utils import simplejson as json


class JSONResponseMixin(object):
    content_type = None
    json_encoder_class = DjangoJSONEncoder

    def get_content_type(self):
        if (self.content_type is not None and
            not isinstance(self.content_type,
                           (six.string_types, six.text_type))):
            raise ImproperlyConfigured(
                '{0} is missing content type. Define {0}.content_type, '
                'or override {0}.get_content_type().'.format(
                    self.__class__.__name__))
        return self.content_type or "application/json"

    def render_json_response(self, context, status=200):
        """
        Serialize the context dictionary as JSON and return it
        as a HTTP Repsonse object. This method only allows
        serialization of simple objects (i.e. no model instances)
        """
        json_context = json.dumps(context, cls=self.json_encoder_class)

        return HttpResponse(json_context,
                            content_type=self.get_content_type(),
                            status=status)
