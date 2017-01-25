from random import randint
from datetime import datetime, timedelta

from chart import Chart
from chart.config import Axes, DataSet, rgba


class TimeSeriesChart(Chart):
    chart_type = 'line'
    scales = {
        'xAxes': [Axes(type='time', position='bottom')],
    }

    def get_datasets(self, **kwargs):
        start_date = datetime(2017, 1, 1)
        end_date = datetime(2017, 2, 1)

        data = []

        date_point = start_date
        i = 0
        while date_point < end_date:
            date_point += timedelta(days=1)
            data.append({
                    'x': date_point.isoformat(),
                    'y': i * i
                })
            i += 1

        return [DataSet(
            type='line',
            label='Time Series',
            data=data,
        )]


class ScatterLineChart(Chart):
    chart_type = 'line'
    scales = {
        'xAxes': [Axes(type='time', position='bottom')],
    }

    def get_datasets(self, **kwargs):
        start_date = datetime(2017, 1, 1)
        end_date = datetime(2017, 2, 1)

        data_scatter = []
        data_line = []

        date_point = start_date
        while date_point < end_date:
            date_point += timedelta(days=1)
            data_line.append({
                    'x': date_point.isoformat(),
                    'y': randint(1, 25)
                })

        date_point = start_date
        while date_point < end_date:
            date_point += timedelta(hours=randint(1, 24))
            data_scatter.append({
                    'x': date_point.isoformat(),
                    'y': randint(1, 25),
                })

        return [
            DataSet(type='line',
                    label='Scatter',
                    showLine=False,
                    data=data_scatter),
            DataSet(type='line',
                    label='Line',
                    borderColor='red',
                    data=data_line)
        ]


class BarChart(Chart):
    chart_type = 'bar'

    def get_labels(self, **kwargs):
        return ["January", "February", "March", "April",
                "May", "June", "July"]

    def get_datasets(self, **kwargs):
        data = [10, 15, 29, 30, 5, 10, 22]
        colors = [
            rgba(255, 99, 132, 0.2),
            rgba(54, 162, 235, 0.2),
            rgba(255, 206, 86, 0.2),
            rgba(75, 192, 192, 0.2),
            rgba(153, 102, 255, 0.2),
            rgba(255, 159, 64, 0.2)
        ]

        return [DataSet(label='Bar Chart',
                        data=data,
                        borderWidth=1,
                        backgroundColor=colors,
                        borderColor=colors)]


class RadarChart(Chart):
    chart_type = 'radar'

    def get_labels(self):
        return ["Eating", "Drinking", "Sleeping", "Designing", "Coding", "Cycling", "Running"]

    def get_datasets(self, **kwargs):
        return [DataSet(label="My First dataset",
                        color=(179, 181, 198),
                        data=[65, 59, 90, 81, 56, 55, 40]),
                DataSet(label="My Second dataset",
                        color=(255, 99, 132),
                        data=[28, 48, 40, 19, 96, 27, 100])
                ]


class PolarChart(Chart):
    chart_type = 'polarArea'

    def get_labels(self, **kwargs):
        return ["Red", "Green", "Yellow", "Grey", "Blue"]

    def get_datasets(self, **kwargs):
        return [DataSet(label="My DataSet",
                        data=[11, 16, 7, 3, 14],
                        backgroundColor=[
                            "#FF6384",
                            "#4BC0C0",
                            "#FFCE56",
                            "#E7E9ED",
                            "#36A2EB"
                        ])
                ]


class PieChart(Chart):
    chart_type = 'pie'

    def get_datasets(self, **kwargs):
        return [DataSet(data=[])]


class BubbleChart(Chart):
    chart_type = 'bubble'

    def get_datasets(self, **kwargs):
        data = [{
            'x': randint(1, 10),
            'y': randint(1, 25),
            'r': randint(1, 10),
        } for i in range(25)]

        return [DataSet(label="First DataSet",
                        data=data,
                        backgroundColor='#FF6384',
                        hoverBackgroundColor='#FF6384')]
