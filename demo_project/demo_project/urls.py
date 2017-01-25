from django.conf.urls import include, url
from django.contrib import admin

from demo import views
from demo import charts
from chart.views import ChartView

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^async/$', views.home_async, name='home_async'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^charts/scatter_line_plot/$',
        ChartView.from_chart(charts.ScatterLineChart()),
        name='scatter_line_plot'),

    url(r'^charts/time_series_plot/$',
        ChartView.from_chart(charts.TimeSeriesChart()),
        name='time_series_plot'),

    url(r'^charts/bar_plot/$',
        ChartView.from_chart(charts.BarChart()),
        name='bar_plot'),

    url(r'^charts/radar_plot/$',
        ChartView.from_chart(charts.RadarChart()),
        name='radar_plot'),

    url(r'^charts/polar_plot/$',
        ChartView.from_chart(charts.PolarChart()),
        name='polar_plot'),

    url(r'^charts/bubble_plot/$',
        ChartView.from_chart(charts.BubbleChart()),
        name='bubble_plot'),
]
