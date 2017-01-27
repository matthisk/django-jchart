from django.shortcuts import render

from demo import charts


def home(request):
    context = {
        'time_series_chart': charts.TimeSeriesChart(),
        'scatter_line_chart': charts.ScatterLineChart(),
        'bar_chart': charts.BarChart(),
        'radar_chart': charts.RadarChart(),
        'polar_chart': charts.PolarChart(),
        'pie_chart': charts.PieChart(),
        'bubble_chart': charts.BubbleChart(),
    }
    return render(request, 'home.html', context)
