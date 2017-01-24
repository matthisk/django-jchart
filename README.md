# django-chart

[![Build Status](https://travis-ci.org/matthisk/django-chart.svg?branch=master)](https://travis-ci.org/matthisk/django-chart)

A Django App to plot charts using the excellent Chart.JS library.
This library enables you to create any Chart.JS chart using Django class based views. The configuration data for the chart is generated as a JSON http repsonse which can be loaded directly in to the Chart.JS library.

- Authors: Matthisk Heimensen
- Licence: BSD
- Compatibility: Django 1.5+, python2.7 up to python3.3
- Project URL: https://github.com/matthisk/django-chart

### Getting Started

install ``django-chart``

```
pip install django-chart
```

Add ``django-chart`` to your installed apps.

```
INSTALLED_APPS = (
    '...',
    'chart',
)
```

### Documentation

...