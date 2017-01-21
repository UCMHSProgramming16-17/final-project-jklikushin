# Data used: 2013-2014 high school graduation rate visualied for mainland US states
# Source of data: http://www.governing.com/gov-data/high-school-graduation-rates-by-state.html

# import the csv module
import csv
    # f = open('graddata.csv')
    # csv_f = csv.reader(f)
    # for row in csv_f:
    #     print(row)
    # f.close()


from bokeh.io import save, output_file
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LogColorMapper,
)

# specify an output file to export into
output_file("map1.html")

# import color palette from bokeh
from bokeh.palettes import Viridis256 as palette
from bokeh.plotting import figure
from bokeh.sampledata.us_states import data as states

# for only mainland states, remove Alaska and Hawaii from 'states' directory
states.pop('AK', None)
states.pop('HI', None)

# import data from 'graddata.csv' file into a dictionary named 'ratedict'
with open('graddata.csv', mode='r') as infile:
    reader = csv.reader(infile)
    ratedict = {rows[0]:rows[1] for rows in reader}

# reverse pallete, so that highest graduation rate is the darkest
palette.reverse()

# create state outlines by plotting longitudes and lattitudes for each state
state_xs = [state['lons'] for state in states.values()]
state_ys = [state['lats'] for state in states.values()]


state_names = [state['name'] for state in states.values()]

source = ColumnDataSource(
    data=dict(
        x = state_xs,
        y = state_ys,
    )
)

state_rates = [ratedict[row] for row in states]
color_mapper = LogColorMapper(palette=palette)

source = ColumnDataSource(data=dict(
    x=state_xs,
    y=state_ys,
    name=state_names,
    rate=state_rates,
))

TOOLS = "pan,wheel_zoom,box_zoom,reset,save,hover,box_select"

p = figure(
    title="Graduation Rate by State",
    x_axis_location=None, y_axis_location=None,
    tools=TOOLS
)
p.grid.grid_line_color = None
p.patches('x', 'y', source=source, fill_color={'field': 'rate', 'transform': color_mapper}, line_color='navy')


hover = p.select_one(HoverTool)
hover.point_policy = "follow_mouse"
hover.tooltips = [
    ("Name", "@name"),
    ("Graduation rate", "@rate%"),
]

save(p)

    # print(states.keys())
    # print(sorted(states))
    # print(ratedict)