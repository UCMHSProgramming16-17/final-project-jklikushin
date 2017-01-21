# import the csv module
import csv

# import save module and output file module
from bokeh.io import save, output_file
# import various modules for data visualization
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LogColorMapper,
)

# specify an output file to export into
output_file("hsgraduationmap.html")

# import color palette from bokeh
from bokeh.palettes import Viridis256 as palette
# reverse pallete, so that highest graduation rate is the darkest
palette.reverse()

# import figure module for plotting
from bokeh.plotting import figure

# creates a dictionary 'states' made of state latitudes and longitudes
from bokeh.sampledata.us_states import data as states
# for only mainland states, remove Alaska and Hawaii from 'states' dictionary
states.pop('AK', None)
states.pop('HI', None)

# import high school graduation data from 'graddata.csv' file into a dictionary named 'ratedict'
with open('graddata.csv', mode='r') as infile:
    reader = csv.reader(infile)
    ratedict = {rows[0]:rows[1] for rows in reader}

# turn state latitude and longitude values from 'states' into x and y coordinates
state_xs = [state['lons'] for state in states.values()]
state_ys = [state['lats'] for state in states.values()]

# create lists for state names and graduation rates
state_names = [state['name'] for state in states.values()]
state_rates = [ratedict[row] for row in states]

# define a color mapper to color code each state based on graduation rate
color_mapper = LogColorMapper(palette=palette)

# create a source variable to contain state x and y coordinates, as well as states names and rates
source = ColumnDataSource(
    data=dict(
        x=state_xs,
        y=state_ys,
        name=state_names,
        rate=state_rates,
    )
)

# define tools available in bokeh visualization
TOOLS = "pan,wheel_zoom,box_zoom,reset,save,hover,box_select"

# define attributes of data visualization
p = figure(
    title="Graduation Rate by State",
    x_axis_location=None, y_axis_location=None,
    tools=TOOLS
)
p.grid.grid_line_color = None
# assign state patches by filling in state borders with color mapper
p.patches('x', 'y', source=source, fill_color={'field': 'rate', 'transform': color_mapper}, line_color='navy')

# create a hovertool which will follow user's mouse and show the name of the state and the graduation rate
hover = p.select_one(HoverTool)
hover.point_policy = "follow_mouse"
hover.tooltips = [
    ("Name", "@name"),
    ("Graduation rate", "@rate%"),
]

# save data in html output file
save(p)