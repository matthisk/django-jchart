def assert_keys(name, allowed_keys, kwargs):
    remainder_keys = set(kwargs.keys()) - allowed_keys

    if len(remainder_keys) > 0:
        msg = 'Use of illegal keyword arguments for {}: {}'
        msg = msg.format(name, remainder_keys)
        raise ValueError(msg)


def assert_color(colors):
    if len(colors) != 3:
        raise ValueError('Expected colors tuple of length 3')


def Axes(**kwargs):
    allowed_keys = {'type', 'display', 'position', 'id', 'gridLines', 'scaleLabel', 'ticks',
                    'barPercentage', 'categoryPercentage', 'barThickness', 'maxBarThickness'}

    assert_keys('Axes', allowed_keys, kwargs)

    return dict(**kwargs)


def ScaleLabel(**kwargs):
    allowed_keys = {'display', 'labelString', 'fontColor', 'fontFamily', 'fontSize',
                    'fontStyle'}

    assert_keys('ScaleLabel', allowed_keys, kwargs)

    return dict(**kwargs)


def Tick(**kwargs):
    allowed_keys = {'autoSkip', 'autoSkipPadding', 'callback', 'display', 'fontColor',
                    'fontFamily', 'fontSize', 'fontStyle', 'labelOffset', 'maxRotation',
                    'minRotation', 'mirror', 'padding', 'reverse'}

    assert_keys('Tick', allowed_keys, kwargs)

    return dict(**kwargs)


def DataSet(**kwargs):
    allowed_keys = {'type', 'data', 'label', 'xAxisID', 'yAxisID', 'fill',
                    'cubicInterpolationMode', 'lineTension', 'backgroundColor',
                    'borderWidth', 'borderColor', 'borderCapStyle', 'borderDash',
                    'borderDashOffset', 'borderJoinStyle', 'pointBorderColor',
                    'pointBackgroundColor', 'pointBorderWidth', 'pointRadius',
                    'pointHoverRadius', 'pointHitRadius', 'pointHoverBackgroundColor',
                    'pointHoverBorderColor', 'pointHoverBorderWidth', 'pointStyle',
                    'showLine', 'spanGaps', 'steppedLine', 'color',
                    'data', 'label', 'fill', 'lineTension', 'backgroundColor',
                    'borderWidth', 'borderColor', 'borderCapStyle', 'borderDash',
                    'borderDashOffset', 'borderJoinStyle', 'pointBorderColor',
                    'pointBackgroundColor', 'pointBorderWidth', 'pointRadius',
                    'pointHoverRadius', 'hitRadius', 'pointHoverBackgroundColor',
                    'pointHoverBorderColor', 'pointHoverBorderWidth', 'pointStyle',
                    'data', 'label', 'backgroundColor', 'borderColor', 'borderWidth',
                    'hoverBackgroundColor', 'hoverBorderColor', 'hoverBorderWidth',
                    'hoverRadius'}

    assert_keys('DataSet', allowed_keys, kwargs)

    result = dict(**kwargs)

    if 'color' in kwargs:
        color = kwargs['color']

        assert_color(color)

        set_colors = dict(
            backgroundColor=rgba(*color, a=0.2),
            pointBackgroundColor=rgba(*color, a=0.5),
            borderColor=rgba(*color, a=0.5),
            pointBorderColor=rgba(*color, a=1),
            pointStrokeColor=rgba(*color, a=1),
        )
        result.update(**set_colors)

    return result


def Tooltips(**kwargs):
    allowed_keys = {'enabled', 'custom', 'mode', 'intersect', 'position', 'itemSort', 'filter',
                    'backgroundColor', 'titleFontFamily', 'titleFontSize', 'titleFontStyle',
                    'titleFontColor', 'titleSpacing', 'titleMarginBottom', 'bodyFontFamily',
                    'bodyFontSize', 'bodyFontStyle', 'bodyFontColor', 'bodySpacing',
                    'footerFontFamily', 'footerFontSize', 'footerFontStyle', 'footerFontColor',
                    'footerSpacing', 'footerMarginTop', 'xPadding', 'yPadding', 'caretSize',
                    'cornerRadius', 'multiKeyBackground', 'displayColors'}

    assert_keys('Tooltips', allowed_keys, kwargs)

    return dict(**kwargs)


def Legend(**kwargs):
    allowed_keys = {'display', 'position', 'fullWidth', 'labels', 'reverse'}

    assert_keys('Legend', allowed_keys, kwargs)

    return dict(**kwargs)


def LegendLabel(**kwargs):
    allowed_keys = {'boxWidth', 'fontSize', 'fontStyle', 'fontColor', 'fontFamily',
                    'padding', 'generateLabels', 'usePointStyle'}

    assert_keys('LegendLabel', allowed_keys, kwargs)

    return dict(**kwargs)


def Title(**kwargs):
    allowed_keys = {'display', 'position', 'fullWidth', 'fontSize', 'fontFamily',
                    'fontColor', 'fontStyle', 'padding', 'text'}

    assert_keys('Title', allowed_keys, kwargs)

    return dict(**kwargs)


def Hover(**kwargs):
    allowed_keys = {'mode', 'intersect', 'animationDuration'}

    assert_keys('Hover', allowed_keys, kwargs)

    return dict(**kwargs)


def InteractionModes(**kwargs):
    allowed_keys = {'point', 'nearest', 'single', 'label', 'index',
                    'x-axis', 'dataset', 'x', 'y'}

    assert_keys('InteractionModes', allowed_keys, kwargs)

    return dict(**kwargs)


def Animation(**kwargs):
    allowed_keys = {'duration', 'easing'}

    assert_keys('Animation', allowed_keys, kwargs)

    return dict(**kwargs)


def Element(**kwargs):
    allowed_keys = {'arc', 'line', 'point', 'rectangle'}

    assert_keys('Element', allowed_keys, kwargs)

    return dict(**kwargs)


def ElementArc(**kwargs):
    allowed_keys = {'backgroundColor', 'borderColor', 'borderWidth'}

    assert_keys('Element', allowed_keys, kwargs)

    return dict(**kwargs)


def ElementLine(**kwargs):
    allowed_keys = {'tension', 'backgroundColor', 'borderWidth', 'borderColor',
                    'borderCapStyle', 'borderDash', 'borderDashOffset', 'borderJoinStyle',
                    'capBezierPoints', 'fill', 'stepped'}

    assert_keys('ElementLine', allowed_keys, kwargs)

    return dict(**kwargs)


def ElementPoint(**kwargs):
    allowed_keys = {'radius', 'pointStyle', 'backgroundColor', 'borderWidth',
                    'borderColor', 'hitRadius', 'hoverRadius', 'hoverBorderWidth'}

    assert_keys('ElementPoint', allowed_keys, kwargs)

    return dict(**kwargs)


def ElementRectangle(**kwargs):
    allowed_keys = {'backgroundColor', 'borderWidth', 'borderColor', 'borderSkipped'}

    assert_keys('ElementRectangle', allowed_keys, kwargs)

    return dict(**kwargs)


def rgba(r, g, b, a=1.0):
    return "rgba({},{},{},{})".format(r, g, b, a)
