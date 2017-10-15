## Changelog

### Version 0.5.0

* Better Django backwards compatibility
* Improved sizing of the chart container html element

### Version 0.4.0

* Added custom chart configuration options through the use of the `options` class field

### Version 0.3.2

* `get_datasets` method is type checked. When an instance of the `Chart` class returns somtehing different than a list this results in a ValueError

### Version 0.3.1

* Added support for several bar chart specific Axes config properties (e.g. barPercentage)

### Version 0.3.0

* Added support for non async chart parameterization with `render_chart` template tag
