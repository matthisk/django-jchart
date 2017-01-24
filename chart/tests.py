import json

from django.test import TestCase, RequestFactory
from django.utils import six

from .views import BaseChart
from .config import (Title, Legend, Tooltips, Hover,
                     InteractionModes, Animation, Element,
                     ElementArc, Axes, ScaleLabel, Tick, rgba)


class LineChart(BaseChart):
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

    def get_datasets(self):
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        return [dict(label='Test Line Chart', data=data)]


class BarChart(BaseChart):
    chart_type = 'radar'
    title = Title(text='Test Title')

    def get_datasets(self):
        data = []
        return [dict(label='Test Radar Chart', data=data)]


class PolarChart(BaseChart):
    chart_type = 'polarArea'
    title = Title(text='Test Title')

    def get_datasets(self):
        data = []
        return [dict(label='Test Polar Chart', data=data)]


class RadarChart(BaseChart):
    chart_type = 'bar'
    title = Title(text='Test Title')

    def get_datasets(self):
        data = []
        return [dict(label='Test Line Chart', data=data)]


class PieChart(BaseChart):
    chart_type = 'pie'
    title = Title(text='Test Title')

    def get_datasets(self):
        data = []
        return [dict(label='Test Pie Chart', data=data)]


class BubbleChart(BaseChart):
    chart_type = 'bubble'
    title = Title(text='Test Title')

    def get_datasets(self):
        data = []
        return [dict(label='Test Bubble Chart', data=data)]


class ResponseTestToolkit(TestCase):
    classes = None

    @property
    def request(self):
        request_factory = RequestFactory()
        return request_factory.get('/test-url')

    @property
    def responses(self):
        for klass in self.classes:
            yield klass.as_view()(self.request)


class ResponseTestToolkitSolo(ResponseTestToolkit):
    klass = None

    @property
    def response(self):
        return self.klass.as_view()(self.request)

    @property
    def data(self):
        charset = self.response.charset
        data = self.response.content.decode(charset)
        return json.loads(data)


class BaseChartTestCase(ResponseTestToolkit):
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
            content = response.content.decode(response.charset)
            data = json.loads(content)
            self.assertIn('data', data)
            self.assertIn('options', data)
            self.assertIn('type', data)

            self.assertTrue(isinstance(data['data'], dict))
            self.assertTrue(isinstance(data['options'], dict))
            self.assertTrue(isinstance(data['type'], (six.string_types, six.text_type)))

            self.assertIn(data['type'], ['bar', 'line', 'radar', 'polarArea', 'pie', 'bubble'])
            self.assertIn('title', data['options'])


class LineChartTestCase(ResponseTestToolkitSolo):
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
