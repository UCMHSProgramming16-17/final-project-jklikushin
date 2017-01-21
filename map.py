import csv
f = open('graddata.csv')
csv_f = csv.reader(f)
for row in csv_f:
    print(row)
f.close()


from bokeh.io import save, output_file
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LogColorMapper
)

output_file("map.html")

from bokeh.palettes import Spectral6 as palette
from bokeh.plotting import figure
from bokeh.sampledata.us_states import data as states
from bokeh.sampledata.unemployment import data as graduationrate

palette.reverse()


state_xs = states["NJ"]["lons"]
state_ys = states["NJ"]["lats"]

state_names = [state['name'] for state in states.values()]

source = ColumnDataSource(
    data=dict(
        x = state_xs,
        y = state_ys,
        # name = state_names
    )
)

# state_rates = [unemployment[state_id] for state_id in states]
# color_mapper = LogColorMapper(palette=palette)

# source = ColumnDataSource(data=dict(
#     x=state_xs,
#     y=state_ys,
#     name=state_names,
#     rate=state_rates,
# ))

# TOOLS = "pan,wheel_zoom,box_zoom,reset,hover,save"

p = figure(
    title="Graduation Rate by State",
    x_axis_location=None, y_axis_location=None
)
# p.grid.grid_line_color = None

p.patch('x', 'y', source=source)

# hover = p.select_one(HoverTool)
# hover.point_policy = "follow_mouse"
# hover.tooltips = [
#     ("Name", "@name"),
#     ("Unemployment rate)", "@rate%"),
#     ("(Long, Lat)", "($x, $y)"),
# ]

save(p)