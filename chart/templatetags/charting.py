import uuid

from django import template
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

register = template.Library()


def render_html(html_id, url):
    context = dict(html_id=html_id, url=url)
    return render_to_string('charting/async/html.html', context)


def render_js(html_id, url):
    context = dict(html_id=html_id, url=url)
    return render_to_string('charting/async/js.html', context)


@register.simple_tag
def render_chart(url_name, *args, **kwargs):
    html_id = 'chart-{}'.format(uuid.uuid4())
    url = reverse(url_name, args=args, kwargs=kwargs)
    context = {
        'html': render_html(html_id, url),
        'js': render_js(html_id, url),
    }
    return render_to_string('charting/chart.html', context)
