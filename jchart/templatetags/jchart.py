import uuid

from django import template
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

from .. import Chart

register = template.Library()


def render_html(html_id, url):
    context = dict(html_id=html_id, url=url)
    return render_to_string('charting/async/html.html', context)


def render_js(html_id, url):
    context = dict(html_id=html_id, url=url)
    return render_to_string('charting/async/js.html', context)

def render_chart_inline(chart, *args, **kwargs):
    return chart.as_html(*args, **kwargs)

def render_chart_async(url_name, *args, **kwargs):
    html_id = 'chart-{}'.format(uuid.uuid4())
    url = reverse(url_name, args=args, kwargs=kwargs)
    context = {
        'html': render_html(html_id, url),
        'js': render_js(html_id, url),
    }
    return render_to_string('charting/chart.html', context)

@register.simple_tag
def render_chart(chart_or_url_name, *args, **kwargs):
    if isinstance(chart_or_url_name, Chart):
        return render_chart_inline(chart_or_url_name, *args, **kwargs)
    else:
        return render_chart_async(chart_or_url_name, *args, **kwargs)
