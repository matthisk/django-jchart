# django-jchart

[![Build Status](https://travis-ci.org/matthisk/django-jchart.svg?branch=master)](https://travis-ci.org/matthisk/django-jchart) [![Coverage Status](https://coveralls.io/repos/github/matthisk/django-jchart/badge.svg?branch=master)](https://coveralls.io/github/matthisk/django-jchart?branch=master)
[![PyPI version](https://badge.fury.io/py/django-jchart.svg)](https://badge.fury.io/py/django-jchart)

This Django app enables you to configure and render <a href="http://www.chartjs.org/">Chart.JS</a> charts directly from your Django codebase. Charts can than either be rendered directly into your Django template or served asynchronously to the webbrowser.

- Authors: Matthisk Heimensen
- Licence: BSD
- Compatibility: Django 1.5+, python2.7 up to python3.5
- Project URL: https://github.com/matthisk/django-jchart

### Getting Started

install ``django-jchart``

```
pip install django-jchart
```

Add ``django-jchart`` to your installed apps.

```
INSTALLED_APPS = (
    '...',
    'jchart',
)
```

<p>
    Enable template loading from app folders by adding the following property to your <i>TEMPLATES</i> django configuration:
</p>

<pre><code class="language-python">TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        # ...
    }]
</code></pre>

### (Code) Examples

The [main webpage](http://django-jchart.matthisk.nl/) for this repository contains examples for all different chart types. 

### Documentation

<h4 class="section-title" id="docs-frontend-deps">
    <a class="fragment-link" href="#docs-frontend-deps">
        Frontend Dependencies
    </a>
</h4>

<p>
For the charts to be rendered inside the browser you will
need to include the Chart.JS library. Add the following
HTML before your closing <code>&lt;/body&gt;</code> tag: 
</p>

<pre><code class="language-html">&lt;script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.4.0/Chart.bundle.min.js"&gt;&lt;/script&gt;</code></pre>

<p>
If you want to make use of <a href="#async-charts">asynchronous loading charts</a>
you will also need to include jQuery:
</p>

<pre><code class="language-html">&lt;script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"&gt;&lt;/script&gt;</code></pre>

<h4 class="section-title" id="docs-chart-objects">
    <a class="fragment-link" href="#docs-chart-objects">
        The Chart Class
    </a>
</h4>

<p>
    At the heart of this charting library lies the <code>Chart</code> class. This class describes a chart, and defines which data it should display. The chart's class fields map to <a href="http://www.chartjs.org/docs/#chart-configuration">Chart.JS options</a> which describe how the chart should render and behave. There is a method that should be implemented in the chart class that defines which datasets are to be plotted, this method should be called <code>get_datasets</code>.
</p>

<p>
    To define which type of chart you want to render (e.g. a line or bar chart), your chart class should set it's class field <code>chart_type</code> to one of "line", "bar", "radar", "polarArea", "pie", or "bubble". A chart class without this field is invalid and initialization will result in a <code>ImproperlyConfigured</code> exception.
</p>

<pre><code class="language-python">from jchart import Chart

class LineChart(Chart):
    chart_type = 'line'</code></pre>

<h5 class="section-title" id="docs-get-datasets">
    <a class="fragment-link" href="#docs-get-datasets">
        get_datasets
    </a>
</h5>

<p>
    The <code>get_datasets</code> method should return a list of datasets this chart should display. Where a dataset is a dictionary with key/value configuration pairs (see the Chart.JS <a href="http://www.chartjs.org/docs/#line-chart-dataset-structure">documentation</a>).
</p>

<pre><code class="language-python">from jchart import Chart

class LineChart(Chart):
    chart_type = 'line'

    def get_datasets(self, **kwargs):
        return [{
            'label': "My Dataset",
            'data': [69, 30, 45, 60, 55]
        }]</code></pre>

<h5 class="section-title" id="docs-get-labels">
    <a class="fragment-link" href="#docs-get-labels">
        get_labels
    </a>
</h5>

<p>
    This method allows you to set the Chart.JS <code>data.labels</code> parameter. Which allows you to configure <a href="http://www.chartjs.org/docs/#scales-category-scale">categorical axes</a>. For an example on how to use this feature see this <a href="#pie-chart">pie chart</a>.
</p>

<pre><code class="language-python">from jchart import Chart

class PieChart(Chart):
    chart_type = 'pie'

    def get_labels(self, **kwargs):
        return ['Red', 'Blue']</code></pre>

<h4 class="section-title" id="docs-configuring-charts">
    <a class="fragment-link" href="#docs-configuring-charts">
        Configuring Charts
    </a>
</h4>

<p>
    A chart can be configured through the following class fields:
</p>

<p>
        <code>scales</code>
        <code>layout</code>
        <code>title</code>
        <code>legend</code>
        <code>tooltips</code>
        <code>hover</code>
        <code>animation</code>
        <code>elements</code>
        <code>responsive</code>
</p>

<p>
    All of these fields map to the same key in the Chart.JS <a href="http://www.chartjs.org/docs/#chart-configuration-creating-a-chart-with-options">'options' object</a>. For instance, if you wanted to create a chart that does not render responsively you would set the responsive class field to false:
</p>

<pre><code class="language-python">from jchart import Chart

class UnresponsiveLineChart(Chart):
    chart_type = 'line'
    responsive = False
    # ...</code></pre>

<p>
    Most of these class fields require either a list of dicitonaries or a dictionary. With the exception of <code>responsive</code> which should be a boolean value. Be sure to read the Chart.JS <a href="http://www.chartjs.org/docs/#chart-configuration-common-chart-configuration">documentation</a> on how to use these configuration options.
</p>

<p>
    For your convenience there are some methods located in <code>jchart.config</code> which can be used to produce correct dictionaries to configure Chart.JS properties. Most of these methods only serve as a validation step for your input configuration but some can also transform the input configuration. Lets take a look at an example, how would you configure the X-Axis so it wouldn't be displayed:
</p>

<pre><code class="language-python">from jchart import Chart
from jchart.config import Axes

class LineChart(Chart):
    chart_type = 'line'
    scales = {
        'xAxes': [Axes(display=False)],
    }</code></pre>

<p>
    <code>jchart.config</code> also contains a method to create dataset configuration dictionaries. One of the advantages of using this method is that it includes a special property <code>color</code> which can be used to automatically set the values for: 'backgroundColor', 'pointBackgroundColor', 'borderColor', 'pointBorderColor', and 'pointStrokeColor'.
</p>

<pre><code class="language-python">from jchart import Chart
from jchart.config import Axes

class LineChart(Chart):
    chart_type = 'line'
    
    def get_datasets(self, **kwargs):
        return [DataSet(color=(255, 255, 255), data=[])]</code></pre>

<p>
    The <code>jchart.config</code> module contains methods for the properties listed below. Keep in mind that you are in no way obligated to use these methods, you could also supply Python dictionaries in the place of these method calls.
    
    <h5>Available Configuration Convenience methods:</h5>
    <code>Axes</code>, <code>ScaleLabel</code>, <code>Tick</code>, <code>DataSet</code>, <code>Tooltips</code>, <code>Legend</code>, <code>LegendLabel</code>, <code>Title</code>, <code>Hover</code>, <code>InteractionModes</code>, <code>Animation</code>, <code>Element</code>, <code>ElementArc</code>, <code>ElementLine</code>, <code>ElementPoint</code>, <code>ElementRectangle</code>
</p>

<h4 class="section-title" id="docs-rendering-charts">
    <a class="fragment-link" href="#docs-rendering-charts">
        Rendering Charts
    </a>
</h4>

<p>
    Chart instances can be passed to your Django template context.
    Inside the template you can invoke the method `as_html` on the
    chart instance to render the chart.
</p>

<pre><code class="language-python"># LineChart is a class inheriting from jchart.Chart

def some_view(request):
    render(request, 'template.html', {
        'line_chart': LineChart(),
    })</code></pre>

<p>
    The following code is an example of how to render this line chart
    inside your html template:
</p>

<pre><code class="language-python">&#123;&#123; line_chart.as_html &#125;&#125;</code></pre>

<h4 class="section-title" id="docs-asynchronous-charts">
    <a class="fragment-link" href="#docs-asynchronous-charts">
        Asynchronous Charts
    </a>
</h4>

<p>
    While rendering the chart directly into your HTML template, all the data
    needed for the chart is transmitted on the page's HTTP request. It is
    also possible to load the chart (and its required data) asynchronous.
</p>

<p>
    To do this we need to setup a url endpoint from which to load the chart's data. There is a classmethod available on <code>jchart.ChartView</code> to automatically create a view which exposes the chart's configuration data as JSON on a HTTP get request:
</p>

<pre><code class="language-python">from jchart.views import ChartView

# LineChart is a class inheriting from jchart.Chart
line_chart = LineChart()

urlpatterns = [
    url(r'^charts/line_chart/$', ChartView.from_chart(line_chart), name='line_chart'),
]</code></pre>

<p>
    You can use a custom templatetag inside your Django template to load this chart asynchronously. The custom tag behaves like the Django url templatetag and any positional or keyword arguments supplied to it are used to resolve the url for the given url name. In this example the url does not require any url parameters
    to be resolved:
</p>

<pre><code class="language-python">{&#37; load jchart &#37;}

{&#37; render_chart 'line_chart' &#37;}
</code></pre>

<p>
    This tag will be expanded into the following JS/HTML code:
</p>

<pre><code class="language-html">&lt;canvas class="chart" id="unique-chart-id"&gt;
&lt;/canvas&gt;

&lt;script type="text/javascript"&gt;
window.addEventListener("DOMContentLoaded", function() {
    $.get('/charts/line_chart/', function(configuration) {
        var ctx = document.getElementById("unique-chart-id").getContext("2d");    

        new Chart(ctx, configuration);
    });
});
&lt;/script&gt;</code></pre>

### ToDO

* Composable datasources (instead of having to rely on inheritance)
* Compare django-jchart to other Django chartig libraries (in the readme)


### Contributing

#### Releasing

* To release update the version of the package in `setup.py`.
* Add release to `CHANGELOG.md`.
* Run commands:

```
python setup.py sdist bdist_wheel --universal
twine upload dist/*
```

* Add git tag to commit