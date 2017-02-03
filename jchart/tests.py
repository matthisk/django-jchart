import json

from django.test import TestCase, RequestFactory
from django.utils import six
from django.core.exceptions import ImproperlyConfigured

from .views import ChartView
from . import Chart
from .config import (Title, Legend, Tooltips, Hover,
                     InteractionModes, Animation, Element,
                     ElementArc, Axes, ScaleLabel, Tick, rgba)


class LineChart(Chart):
    chart_type = 'line'
    title = Title(text='Test Title Line')
    legend = Legend(display=False)
    tooltips = Tooltips(enabled=False)
    hover = Hover(mode='default')
    animation = Animation(duration=1.0)
    scales = {
        'xAxes': [Axes(display=False, type='time', position='bottom')],
        'yAxes': [Axes(type='linear',
                       position='left',
                       scaleLabel=ScaleLabel(fontColor='#fff'),
                       ticks=Tick(fontColor='#fff')
                       )],
    }

    def get_datasets(self, *args, **kwargs):
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        return [dict(label='Test Line Chart', data=data)]


class LineChartParameterized(LineChart):

    def get_datasets(self, currency_type):
        eur_data = list(range(10))
        do_data = list(range(10, 20))

        if currency_type == 'euro':
            return [dict(label='Euro Chart', data=eur_data)]
        elif currency_type == 'dollar':
            return [dict(label='Dollar Chart', data=do_data)]

        raise ValueError('Unkown currency type: {}'.format(currency_type))


class LineChartUnresponsive(LineChart):
    responsive = False


class BarChart(Chart):
    chart_type = 'radar'
    title = Title(text='Test Title')

    def get_datasets(self, *args, **kwargs):
        data = []
        return [dict(label='Test Radar Chart', data=data)]


class PolarChart(Chart):
    chart_type = 'polarArea'
    title = Title(text='Test Title')

    def get_datasets(self, *args, **kwargs):
        data = []
        return [dict(label='Test Polar Chart', data=data)]


class RadarChart(Chart):
    chart_type = 'bar'
    title = Title(text='Test Title')

    def get_datasets(self, *args, **kwargs):
        data = []
        return [dict(label='Test Line Chart', data=data)]


class PieChart(Chart):
    chart_type = 'pie'
    title = Title(text='Test Title')

    def get_datasets(self, *args, **kwargs):
        data = []
        return [dict(label='Test Pie Chart', data=data)]


class BubbleChart(Chart):
    chart_type = 'bubble'
    title = Title(text='Test Title')

    def get_datasets(self, *args, **kwargs):
        data = []
        return [dict(label='Test Bubble Chart', data=data)]


class ChartViewTestToolkit(TestCase):
    classes = None
    url_kwargs = {}

    @property
    def request(self):
        request_factory = RequestFactory()
        return request_factory.get('/test-url')

    @property
    def responses(self):
        for klass in self.classes:
            yield ChartView.from_chart(klass())(self.request, **self.url_kwargs)


class ChartViewTestToolkitSolo(ChartViewTestToolkit):
    klass = None
    url_kwargs = {}

    @property
    def response(self):
        return ChartView.from_chart(self.klass())(self.request, **self.url_kwargs)
        return self.klass.as_view()(self.request)

    @property
    def data(self):
        charset = getattr(self.response, 'charset', 'utf-8')
        data = self.response.content.decode(charset)
        return json.loads(data)


class ChartResponseTestCase(ChartViewTestToolkit):
    classes = (
        LineChart,
        BarChart,
        PolarChart,
        RadarChart,
        PieChart,
        BubbleChart,
    )

    def test_status_code(self):
        for response in self.responses:
            self.assertEquals(response.status_code, 200)

    def test_content_type(self):
        for response in self.responses:
            self.assertEquals(response.get('content-type'), 'application/json')

    def test_chart_config(self):
        for response in self.responses:
            charset = getattr(response, 'charset', 'utf-8')
            content = response.content.decode(charset)
            data = json.loads(content)
            self.assertIn('data', data)
            self.assertIn('options', data)
            self.assertIn('type', data)

            self.assertTrue(isinstance(data['data'], dict))
            self.assertTrue(isinstance(data['options'], dict))
            self.assertTrue(isinstance(data['type'], (six.string_types, six.text_type)))

            self.assertIn(data['type'], ['bar', 'line', 'radar', 'polarArea', 'pie', 'bubble'])
            self.assertIn('title', data['options'])


class LineChartTestCase(ChartViewTestToolkitSolo):
    klass = LineChart

    def test_title(self):
        self.assertEquals(self.data['options']['title']['text'], 'Test Title Line')

    def test_legend(self):
        self.assertEquals(self.data['options']['legend']['display'], False)

    def test_tooltips(self):
        self.assertEquals(self.data['options']['tooltips']['enabled'], False)

    def test_hover(self):
        self.assertEquals(self.data['options']['hover']['mode'], 'default')

    def test_animation(self):
        self.assertEquals(self.data['options']['animation']['duration'], 1.0)

    def test_dataset(self):
        self.assertEquals(len(self.data['data']['datasets']), 1)
        self.assertEquals(len(self.data['data']['labels']), 0)
        self.assertEquals(self.data['data']['datasets'][0]['data'], list(range(1, 10)))


class TestConfigADTS(TestCase):

    def test_rgba(self):
        self.assertEquals(rgba(255, 255, 255), 'rgba(255,255,255,1.0)')
        self.assertEquals(rgba(255, 255, 255, 0.0), 'rgba(255,255,255,0.0)')

    def test_title(self):
        title = Title(text='Hello World')
        self.assertTrue(isinstance(title, dict))
        self.assertRaises(ValueError, lambda: Title(nonsense='something'))

    def test_legend(self):
        title = Legend(display=False)
        self.assertTrue(isinstance(title, dict))
        self.assertRaises(ValueError, lambda: Legend(nonsense='something'))

    def test_tooltips(self):
        title = Tooltips(enabled=True)
        self.assertTrue(isinstance(title, dict))
        self.assertRaises(ValueError, lambda: Tooltips(nonsense='something'))

    def test_hover(self):
        title = Hover(mode='default')
        self.assertTrue(isinstance(title, dict))
        self.assertRaises(ValueError, lambda: Hover(nonsense='something'))

    def test_interaction_modes(self):
        title = InteractionModes(label='Hello World')
        self.assertTrue(isinstance(title, dict))
        self.assertRaises(ValueError, lambda: InteractionModes(nonsense='something'))

    def test_animation(self):
        title = Animation(duration=1.0)
        self.assertTrue(isinstance(title, dict))
        self.assertRaises(ValueError, lambda: Animation(nonsense='something'))

    def test_element(self):
        arc = ElementArc(borderColor=rgba(255, 255, 255, 1))
        title = Element(arc=arc)
        self.assertTrue(isinstance(title, dict))
        self.assertRaises(ValueError, lambda: Element(nonsense='something'))

    def test_scales(self):
        axes = Axes(type='linear',
                    position='left',
                    scaleLabel=ScaleLabel(fontColor='#fff'),
                    ticks=Tick(fontColor='#fff')
                    )
        self.assertTrue(isinstance(axes, dict))
        self.assertRaises(ValueError, lambda: Axes(nonsense='something'))


class ChartViewTestCase(TestCase):

    def test_chart_view(self):
        self.assertTrue(getattr(ChartView, 'from_chart', False))
        self.assertRaises(ImproperlyConfigured,
                          lambda: ChartView())

    def test_chart_view_from_chart_classonly(self):
        ChartViewSubClass = type('ChartViewSubClass', (ChartView, ), {
                'chart_instance': LineChart()
            })
        chart_view = ChartViewSubClass()
        self.assertRaises(AttributeError,
                          lambda: chart_view.from_chart(LineChart()))

    def test_chart_view_from_chart(self):
        self.assertRaises(ImproperlyConfigured,
                          lambda: ChartView.from_chart(dict()))
        self.assertRaises(ImproperlyConfigured,
                          lambda: ChartView.from_chart(LineChart))
        ChartView.from_chart(LineChart())

    def test_chart_view_get(self):
        ChartViewSubClass = type('ChartViewSubClass', (ChartView, ), {
                'chart_instance': LineChart()
            })
        chart_view = ChartViewSubClass()

        request_factory = RequestFactory()
        request = request_factory.get('/test-url')
        response = chart_view.get(request)

        self.assertEquals(response.status_code, 200)
        charset = getattr(response, 'charset', 'utf-8')
        content = response.content.decode(charset)
        data = json.loads(content)

        self.assertIn('data', data)
        self.assertIn('options', data)
        self.assertIn('type', data)

        self.assertTrue(isinstance(data['data'], dict))
        self.assertTrue(isinstance(data['options'], dict))
        self.assertTrue(isinstance(data['type'], (six.string_types, six.text_type)))

        self.assertIn(data['type'], ['bar', 'line', 'radar', 'polarArea', 'pie', 'bubble'])
        self.assertIn('title', data['options'])


class ChartTestCase(TestCase):

    def test_chart_dimension(self):
        line_chart = LineChartUnresponsive(width=1000, height=500)
        self.assertEquals(line_chart.width, 1000)
        self.assertEquals(line_chart.height, 500)

        self.assertIn('height="500"', line_chart.as_html())
        self.assertIn('width="1000"', line_chart.as_html())

    def test_chart_no_dimension(self):
        line_chart = LineChart()
        self.assertEquals(line_chart.width, None)
        self.assertEquals(line_chart.height, None)

        self.assertNotIn('height="', line_chart.as_html())
        self.assertNotIn('width="', line_chart.as_html())

    def test_chart_html_id(self):
        line_chart = LineChart(html_id='test-id')
        self.assertIn('id="test-id"', line_chart.as_html())

    def test_chart_render_html(self):
        line_chart = LineChart()

        context = {
            'html_id': 'test-id',
            'chart': line_chart,
            'chart_configuration': line_chart.get_configuration(),
        }
        html = line_chart.render_html(context)

        self.assertNotIn('<script', html)

    def test_chart_render_js(self):
        line_chart = LineChart()

        context = {
            'html_id': 'test-id',
            'chart': line_chart,
            'chart_configuration': line_chart.get_configuration(),
        }
        js = line_chart.render_js(context)

        self.assertNotIn('<canvas', js)

    def test_responsive_height_width(self):
        LineChartUnresponsive(height=500)
        self.assertRaises(ImproperlyConfigured,
                          lambda: LineChart(height=500))

    def test_chart_parameterization(self):
        chart = LineChartParameterized()

        self.assertNotIn('Dollar Chart', chart.as_html('euro'))
        self.assertIn('Euro Chart', chart.as_html('euro'))

        self.assertNotIn('Euro Chart', chart.as_html('dollar'))
        self.assertIn('Dollar Chart', chart.as_html('dollar'))


class AsyncChartParameterization(ChartViewTestToolkitSolo):
    klass = LineChartParameterized

    def test_euro(self):
        self.url_kwargs = dict(currency_type='euro')
        self.assertEquals('Euro Chart',
                          self.data['data']['datasets'][0]['label'])

    def test_dollar(self):
        self.url_kwargs = dict(currency_type='dollar')
        self.assertEquals('Dollar Chart',
                          self.data['data']['datasets'][0]['label'])
