from django.conf.urls import include, url
from django.contrib import admin

from demo import views
from demo import charts
from jchart.views import ChartView

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^charts/scatter_line_chart/$',
        ChartView.from_chart(charts.ScatterLineChart()),
        name='scatter_line_chart'),

    url(r'^charts/time_series_chart/$',
        ChartView.from_chart(charts.TimeSeriesChart()),
        name='time_series_chart'),

    url(r'^charts/bar_chart/$',
        ChartView.from_chart(charts.BarChart()),
        name='bar_chart'),

    url(r'^charts/radar_chart/$',
        ChartView.from_chart(charts.RadarChart()),
        name='radar_chart'),

    url(r'^charts/polar_chart/$',
        ChartView.from_chart(charts.PolarChart()),
        name='polar_chart'),

    url(r'^charts/pie_chart/$',
        ChartView.from_chart(charts.PieChart()),
        name='pie_chart'),

    url(r'^charts/bubble_chart/$',
        ChartView.from_chart(charts.BubbleChart()),
        name='bubble_chart'),
]
