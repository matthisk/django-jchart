import uuid

from django.template.loader import render_to_string
from django.core.exceptions import ImproperlyConfigured
from django.core.serializers.json import DjangoJSONEncoder

# Django 1.5+ compat
try:
    import json
except ImportError:  # pragma: no cover
    from django.utils import simplejson as json


class Chart(object):
    chart_type = None
    scales = None
    layout = None
    title = None
    legend = None
    tooltips = None
    hover = None
    animation = None
    elements = None
    responsive = None
    options = None

    def __init__(self, height=None, width=None,
                 html_id=None, json_encoder_class=DjangoJSONEncoder):
        self.height = height
        self.width = width
        self.json_encoder_class = json_encoder_class
        self.html_id = html_id

        if ((height is not None or width is not None) and
                (self.responsive is None or self.responsive)):
            raise ImproperlyConfigured(
                'Using the height/width parameter will have no '
                'effect if the chart is in responsive mode. '
                'Disable responsive mode by setting chart.responsive '
                'to False')

    def _gen_html_id(self):
        return self.html_id or 'chart-{}'.format(uuid.uuid4())

    def _get_options(self):
        option_keys = {'scales', 'layout', 'title', 'legend',
                       'tooltips', 'hover', 'animation', 'elements',
                       'responsive'}

        result = {}
        if self._has_options_attr('options') and isinstance(self.options, dict):
            result = self.options

        result.update({
            key: self._get_options_attr(key)
            for key in option_keys if self._has_options_attr(key)
        })

        return result

    def _get_options_attr(self, name):
        return getattr(self, name, False)

    def _has_options_attr(self, name):
        return getattr(self, name) is not None

    def _assert_chart_type(self):
        if not getattr(self, 'chart_type'):
            raise ValueError(
                'You should add property `chart_type` to your BaseChart instance.'
                'Which is one of `line` `bar` `radar` `polarArea` `pie` `bubble`'
                'or one a custom chart type.')

    def get_configuration(self, *args, **kwargs):
        config = self.chartjs_configuration(*args, **kwargs)
        return json.dumps(config, cls=self.json_encoder_class)

    def chartjs_configuration(self, *args, **kwargs):
        self._assert_chart_type()

        datasets = self.get_datasets(*args, **kwargs)

        if not isinstance(datasets, list):
            raise ValueError('Expect `get_datasets` method on %s '
                             'to return a list of DataSet objects '
                             'or a list of Python dictionaries.' % self)

        data = {}
        data['type'] = self.chart_type
        data['options'] = self._get_options()
        data['data'] = {
            'labels': self.get_labels(*args, **kwargs),
            'datasets': datasets,
        }

        return data

    def get_labels(self, *args, **kwargs):
        return []

    def get_datasets(self, *args, **kwargs):
        raise NotImplementedError(
            'You should return a list of DataSet dictionaries'
            '(i.e.: [DataSet(**keys), ...]'
            )

    def as_html(self, *args, **kwargs):
        context = {
            'html_id': self._gen_html_id(),
            'chart': self,
            'chart_configuration': self.get_configuration(*args, **kwargs),
        }

        context = {
            'html': self.render_html(context),
            'js': self.render_js(context),
        }
        return render_to_string('charting/chart.html', context)

    def render_js(self, context):
        return render_to_string('charting/js.html', context)

    def render_html(self, context):
        return render_to_string('charting/html.html', context)
