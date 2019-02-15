
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Button
from bokeh.models.widgets import Slider, TextInput, PreText
from bokeh.plotting import figure

import test as zz

# Set up data
N = 1600
x = np.linspace(-50, 50, N)
y = x
source = ColumnDataSource(data=dict(x=x, y=y))


# Set up plot
plot = figure(plot_height=400, plot_width=400, title="x",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[-1, 1], y_range=[-1, 1])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)


# Set up widgets
text = TextInput(title="Type Function", value='x', width=400)
t1 = TextInput(title="x value", value='0', width=400)
t2 = TextInput(title="y value", value='0', width=400)
t3 = TextInput(title="z value", value='0', width=400)

parse = TextInput(title='Parsed form', value='', width=500)
diffx = TextInput(title='f_x', value='', width=500)
diffy = TextInput(title='f_y', value='', width=500)
diffz = TextInput(title='f_z', value='', width=500)
num = TextInput(title='Function value', value='', width=500)
stats1 = TextInput(title='Continuity', value='', width=500)
stats2 = TextInput(title='Differentiability', value='', width=500)

button = Button(label='RESULT', width = 60)


# Set up callbacks
def update_result(attrname, old, new):
	
	plot.title.text = zz.execute(text.value, t1.value, t2.value, t3.value)[0]
	parse.value = zz.execute(text.value, t1.value, t2.value, t3.value)[1]
	diffx.value = zz.execute(text.value, t1.value, t2.value, t3.value)[2]
	diffy.value = zz.execute(text.value, t1.value, t2.value, t3.value)[3]
	diffz.value = zz.execute(text.value, t1.value, t2.value, t3.value)[4]
	num.value = zz.execute(text.value, t1.value, t2.value, t3.value)[5]
	stats1.value = zz.execute(text.value, t1.value, t2.value, t3.value)[6]
	stats2.value = zz.execute(text.value, t1.value, t2.value, t3.value)[7]

	x = np.linspace(-50, 50, N)
	y = [zz.plot_eval(text.value, i, 0, 0) for i in x]
	source.data = dict(x=x, y=y)



text.on_change('value', update_result)
t1.on_change('value', update_result)
t2.on_change('value', update_result)
t3.on_change('value', update_result)
#button.on_click(update_result)




# Set up layouts and add to document
inputs = column(text, t1, t2, t3, plot)
inputs2 = column(button, parse, diffx, diffy, diffz, num, stats1, stats2)

curdoc().add_root(row(inputs, inputs2, width=800))
curdoc().title = "Sliders"

