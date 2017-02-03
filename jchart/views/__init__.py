from django.views.generic import View
from django.utils.decorators import classonlymethod
from django.core.exceptions import ImproperlyConfigured

from .mixins import JSONResponseMixin
from .. import Chart


def chart_subclass_factory(chart, *args, **kwargs):
    SubClass = type('ChartSubClass', (ChartView, ), {
            'chart_instance': chart
        })

    return SubClass.as_view()


def assert_chart_instance(chart_instance):
    if (chart_instance is None or
            not isinstance(chart_instance, Chart)):
        raise ImproperlyConfigured(
            'Do not subclass ChartView '
            'without overriding property `chart_instance` '
            'with a valid Chart subclass')


class ChartView(View, JSONResponseMixin):
    '''
    Use this View to serve Chart.js configuration asynchronously.
    This view can be used in cooperation with the {% render_chart %}
    template tag.
    '''
    chart_instance = None

    def __init__(self, *args, **kwargs):
        assert_chart_instance(self.chart_instance)
        super(ChartView, self).__init__(*args, **kwargs)

    @classonlymethod
    def from_chart(cls, chart, *args, **kwargs):
        assert_chart_instance(chart)
        return chart_subclass_factory(chart, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Main entry. This View only responds to GET requests.
        """
        context = self.chart_instance.chartjs_configuration(*args, **kwargs)
        return self.render_json_response(context)
