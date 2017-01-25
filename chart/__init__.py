import json
import uuid

from django.template.loader import render_to_string
from django.core.exceptions import ImproperlyConfigured


class Chart(object):
    scales = None
    layout = None
    title = None
    legend = None
    tooltips = None
    hover = None
    animation = None
    elements = None
    responsive = None

    def __init__(self, height=None, width=None,
                 html_id=None, url_kwargs=None):
        self.kwargs = url_kwargs
        self.height = height
        self.width = width
        self.html_id = html_id or 'chart-{}'.format(uuid.uuid4())

        if ((height is not None or width is not None) and
                (self.responsive is None or self.responsive)):
            raise ImproperlyConfigured(
                'Using the height/width parameter will have no '
                'effect if the chart is in responsive mode. '
                'Disable responsive mode by setting chart.responsive '
                'to False')

    def _get_options(self):
        option_keys = {'scales', 'layout', 'title', 'legend',
                       'tooltips', 'hover', 'animation', 'elements',
                       'responsive'}

        return {key: self._get_options_attr(key)
                for key in option_keys if self._has_options_attr(key)}

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

    @property
    def configuration(self):
        config = self.chartjs_configuration()
        return json.dumps(config)

    def chartjs_configuration(self, **kwargs):
        self._assert_chart_type()

        data = {}
        data['type'] = self.chart_type
        data['options'] = self._get_options()
        data['data'] = {
            'labels': self.get_labels(**kwargs),
            'datasets': self.get_datasets(**kwargs),
        }

        return data

    def get_labels(self, **kwargs):
        return []

    def get_datasets(self, **kwargs):
        raise NotImplementedError(
            'You should return a list of DataSet dictionaries'
            '(i.e.: [DataSet(**keys), ...]'
            )

    def as_html(self):
        context = {
            'html': self.render_html(),
            'js': self.render_js(),
        }
        return render_to_string('charting/chart.html', context)

    def render_html(self):
        context = {
            'chart': self
        }
        return render_to_string('charting/html.html', context)

    def render_js(self):
        context = {
            'chart': self
        }
        return render_to_string('charting/js.html', context)
