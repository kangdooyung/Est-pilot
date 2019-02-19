
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Button, Label
from bokeh.models.widgets import Slider, TextInput, PreText
from bokeh.plotting import figure

import math_func as zz

import convert_latex as xx

# Set up data
N = 2000
x1 = np.linspace(-50, 50, N)
y1 = x1
x2 = np.linspace(-50, 50, N)
y2 = [1 for i in x2]
source1 = ColumnDataSource(data=dict(x=x1, y=y1))
source2 = ColumnDataSource(data=dict(x=x2, y=y2))


# Set up plot
plot1 = figure(plot_height=400, plot_width=400, title="original function",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[-2, 2], y_range=[-2, 2])

plot1.scatter('x', 'y', source=source1, size=3, color="#3A5785", alpha=0.6)

plot2 = figure(plot_height=400, plot_width=400, title="derivative",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[-2, 2], y_range=[-2, 2])

plot2.scatter('x', 'y', source=source2, size=3, color="#3A5785", alpha=0.6)



"""
start
"""
JS_CODE = """
import {Label, LabelView} from "models/annotations/label"

export class LatexLabelView extends LabelView
  render: () ->

    #--- Start of copied section from ``Label.render`` implementation

    # Here because AngleSpec does units tranform and label doesn't support specs
    switch @model.angle_units
      when "rad" then angle = -1 * @model.angle
      when "deg" then angle = -1 * @model.angle * Math.PI/180.0

    panel = @model.panel ? @plot_view.frame

    xscale = @plot_view.frame.xscales[@model.x_range_name]
    yscale = @plot_view.frame.yscales[@model.y_range_name]

    sx = if @model.x_units == "data" then xscale.compute(@model.x) else panel.xview.compute(@model.x)
    sy = if @model.y_units == "data" then yscale.compute(@model.y) else panel.yview.compute(@model.y)

    sx += @model.x_offset
    sy -= @model.y_offset

    #--- End of copied section from ``Label.render`` implementation

    # Must render as superpositioned div (not on canvas) so that KaTex
    # css can properly style the text
    @_css_text(@plot_view.canvas_view.ctx, "", sx, sy, angle)

    # ``katex`` is loaded into the global window at runtime
    # katex.renderToString returns a html ``span`` element
    katex.render(@model.text, @el, {displayMode: true})

export class LatexLabel extends Label
  type: 'LatexLabel'
  default_view: LatexLabelView
"""


class LatexLabel(Label):
    """A subclass of the Bokeh built-in `Label` that supports rendering
    LaTex using the KaTex typesetting library.

    Only the render method of LabelView is overloaded to perform the
    text -> latex (via katex) conversion. Note: ``render_mode="canvas``
    isn't supported and certain DOM manipulation happens in the Label
    superclass implementation that requires explicitly setting
    `render_mode='css'`).
    """
    __javascript__ = ["https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.6.0/katex.min.js"]
   
    __css__ = ["https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.6.0/katex.min.css"]
    __implementation__ = JS_CODE


# Set up widgets

latex1 = LatexLabel(text='x',
                   x=400, y=350, x_units='screen', y_units='screen',
                   render_mode='css', text_font_size='9pt',
                   background_fill_color='#ffffff')

latex2 = LatexLabel(text='1',
                   x=400, y=350, x_units='screen', y_units='screen',
                   render_mode='css', text_font_size='9pt',
                   background_fill_color='#ffffff')

latex3 = LatexLabel(text='0',
                   x=400, y=250, x_units='screen', y_units='screen',
                   render_mode='css', text_font_size='9pt',
                   background_fill_color='#ffffff')

latex4 = LatexLabel(text='0',
                   x=400, y=150, x_units='screen', y_units='screen',
                   render_mode='css', text_font_size='9pt',
                   background_fill_color='#ffffff')
plot1.add_layout(latex1)
plot2.add_layout(latex2)
plot2.add_layout(latex3)
plot2.add_layout(latex4)


text = TextInput(title="Type Function", value='x', width=400)




t1 = TextInput(title="x value", value='0', width=400)
t2 = TextInput(title="y value", value='0', width=400)
t3 = TextInput(title="z value", value='0', width=400)

parse = TextInput(title='Parsed form', value='', width=500)
canon = TextInput(title='Canonical form', value='', width=500)
diffx = TextInput(title='f_x', value='', width=500)
diffy = TextInput(title='f_y', value='', width=500)
diffz = TextInput(title='f_z', value='', width=500)
num = TextInput(title='Function value', value='', width=500)
stats1 = TextInput(title='Continuity', value='', width=500)
stats2 = TextInput(title='Differentiability', value='', width=500)

button = Button(label='RESULT', width = 60)
# button.__javascript__ = ["https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.6.0/katex.min.js"]

# s = '{(x+2)}^(0.5)'


# Set up callbacks
def update_result(attrname, old, new):
	
	canon.value = zz.execute(text.value, t1.value, t2.value, t3.value)[0]
	parse.value = zz.execute(text.value, t1.value, t2.value, t3.value)[1]
	diffx.value = zz.execute(text.value, t1.value, t2.value, t3.value)[2]
	diffy.value = zz.execute(text.value, t1.value, t2.value, t3.value)[3]
	diffz.value = zz.execute(text.value, t1.value, t2.value, t3.value)[4]
	num.value = zz.execute(text.value, t1.value, t2.value, t3.value)[5]
	stats1.value = zz.execute(text.value, t1.value, t2.value, t3.value)[6]
	stats2.value = zz.execute(text.value, t1.value, t2.value, t3.value)[7]
	# latex1.text = xx.pretty_print_latex(s)
	latex1.text = xx.pretty_print_latex('f')+':'+xx.pretty_print_latex(zz.execute(text.value, t1.value, t2.value, t3.value)[0])
	latex2.text = xx.pretty_print_latex('f_x')+':'+xx.pretty_print_latex(zz.execute(text.value, t1.value, t2.value, t3.value)[2])
	latex3.text = xx.pretty_print_latex('f_y')+':'+xx.pretty_print_latex(zz.execute(text.value, t1.value, t2.value, t3.value)[3])
	latex4.text = xx.pretty_print_latex('f_z')+':'+xx.pretty_print_latex(zz.execute(text.value, t1.value, t2.value, t3.value)[4])


	_x = np.linspace(-50, 50, N)
	x1, y1, x2, y2 = zz.plot_eval(text.value, _x)

	source1.data = dict(x=x1, y=y1)
	source2.data = dict(x=x2, y=y2)



text.on_change('value', update_result)
t1.on_change('value', update_result)
t2.on_change('value', update_result)
t3.on_change('value', update_result)
#button.on_click(update_result)




# Set up layouts and add to document
inputs = column(text, t1, t2, t3)
inputs2 = column(plot1, plot2)
inputs3 = column(button, parse, canon, diffx, diffy, diffz, num, stats1, stats2)

curdoc().add_root(row(inputs, inputs3, inputs2, width=800))
curdoc().title = "Pilot Project 1"

