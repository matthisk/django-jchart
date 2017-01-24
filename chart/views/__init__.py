from django.views.generic import View

from .mixins import JSONResponseMixin

from ..config import Axes


class BaseChart(View, JSONResponseMixin):
    scales = None
    layout = None
    title = None
    legend = None
    tooltips = None
    hover = None
    animation = None
    elements = None

    def _get_options(self):
        option_keys = {'scales', 'layout', 'title', 'legend',
                       'tooltips', 'hover', 'animation', 'elements'}

        return {key: self._get_options_attr(key)
                for key in option_keys if self._get_options_attr(key)}

    def _get_options_attr(self, name):
        return getattr(self, name, False)

    def _assert_chart_type(self):
        if not getattr(self, 'chart_type'):
            raise ValueError(
                'You should add property `chart_type` to your BaseChart instance.'
                'Which is one of `line` `bar` `radar` `polarArea` `pie` `bubble`'
                'or one a custom chart type.')

    def get(self, request, *args, **kwargs):
        """
        Main entry. This View only responds to GET requests.
        """
        context = self.get_chartjs_context(**kwargs)
        return self.render_json_response(context)

    def get_chartjs_context(self, **kwargs):
        self._assert_chart_type()

        data = {}
        data['type'] = self.chart_type
        data['options'] = self._get_options()
        data['data'] = {
            'labels': self.get_labels(),
            'datasets': self.get_datasets(**kwargs),
        }

        return data

    def get_labels(self):
        return []

    def get_datasets(self, **kwargs):
        raise NotImplementedError(
            'You should return a list of DataSet dictionaries'
            '(i.e.: [DataSet(**keys), ...]'
            )


class TimeChart(BaseChart):
    chart_type = 'line'
    scales = {
        'xAxes': [Axes(type='time', position='bottom')],
    }
