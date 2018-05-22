from extract_wsc import extractWsc

from bokeh.io import show, curdoc, save

from bokeh.plotting import figure, ColumnDataSource

from bokeh.models.widgets import Select, Button, Paragraph

from bokeh.models import HoverTool, LogColorMapper

from bokeh.layouts import column

from bokeh.sampledata.us_states import data as states

from bokeh.palettes import BrBG5 as palette

import pandas as pd


##Input data from extractWsc
allocOrg, ccName, dirCC, reimburseCC, reimburseFac, reimburseBur, reimburseComp = extractWsc()

## Potential data sources- formatted keys identically for easy use- maybe there is a better way?

comp = { 'ccName' : ccName, 'Value' : reimburseComp }

cc = { 'ccName' : ccName, 'Value' : reimburseCC }

fac = { 'ccName' : ccName, 'Value' : reimburseFac }

#bur = { 'ccName' : ccName, 'Value': reimburseBur }


## Conversion to pandas DataFrame for sorting

comp_df = pd.DataFrame.from_dict(comp)

cc_df = pd.DataFrame.from_dict(cc)

fac_df = pd.DataFrame.from_dict(fac)

#bur_df = pd.DataFrame.from_dict(bur)


## Sorting individual DataFrames

comp_dfsort = comp_df.sort_values(by= 'Value', ascending = False)

cc_dfsort = cc_df.sort_values(by= 'Value', ascending = False)

fac_dfsort = fac_df.sort_values(by= 'Value', ascending = False)

#bur_dfsort = bur_df.sort_values(by= 'Value', ascending = False)


## Converting back to dicts for bokeh

comp_sort = comp_dfsort.to_dict(orient = 'list')

cc_sort = cc_dfsort.to_dict(orient = 'list')

fac_sort = fac_dfsort.to_dict(orient ='list')

#bur_sort = bur_dfsort.to_dict(orient ='list')

## Description text

desc = Paragraph(text = """Reimbursement rates for USGS Water Science Centers associated with each 
        state in the contiguous United States""")
##Setting data source

source = ColumnDataSource(data = comp)

## Setting figure params

p = figure(x_range = source.data['ccName'], plot_height = 500, plot_width = 1000, 
        title = "Reimbursement Rates 2018 (%)", min_border_left = 100, tools = "pan, wheel_zoom, reset, save")


## Instantiating hover tool

hover = HoverTool(tooltips=[
    ("Cost Center", "@ccName"),
    ("Reimbursement" , "@Value"),])

p.add_tools(hover)


## Params for bars

p.vbar(x = 'ccName', top = 'Value', color = '#DC5039', width = 0.9 , source = source)


## Changing orientation of axis labels

p.xaxis.major_label_orientation = 1 


## Creating dropdown menu 

select = Select(title = 'Reimbursement Type:', value = 'Composite', 
        options = ['Composite', 'Cost Center', 'Facility'])#, 'Bureau'])


## and a Sort button

sortButton = Button(label = "Sort", button_type = "success")


## Adding WSC and composite reimbursement to each nested state dict
## Nested dictionary led me to cheating and manually directly referencing vals for the choropleth
## rather than dynamic values dictated by select tool and sort button. Defeat.

del states["HI"]
del states["AK"]


## Reading the datafile

with open("states.txt") as f:
    lines = f.readlines()
    for line in lines:
        items = line.split("\t")
        for state_id in states:
            if state_id == items[0]:
                states[state_id]['ccName'] = items[2]
                states[state_id]['reimbursement'] = items[3] 

## Choropleth

choro = figure(title = "Composite Reimbursement by State 2018 (%)", plot_height = 575, plot_width = 1000,
        tools = "pan, wheel_zoom, reset, save")


EXCLUDED = ("ak", "hi", "pr", "gu", "vi", "mp", "as")

state_xs = [states[code]["lons"] for code in states]
state_ys = [states[code]["lats"] for code in states]


## Source data

state_names = [state['name'] for state in states.values()]

state_cc = [state['ccName'] for state in states.values()]

state_rates = [state['reimbursement'] for state in states.values()]

palette.reverse()

color_mapper = LogColorMapper(palette = palette)

choro_source = ColumnDataSource(data = dict(
    x = state_xs,
    y = state_ys,
    name = state_names,
    cost_center = state_cc,
    rate = state_rates,
    ))

## Never could figure out how to configure the legend properly...

choro.patches( 'x', 'y' , source = choro_source, 
        fill_color = {'field': 'rate', 'transform' : color_mapper},
        fill_alpha = 0.7, 
        line_color= "black", line_width = 2, line_alpha = 0.5) #, legend= "Legend") 


hover = HoverTool(tooltips=[
    ("State" , "@name"),
    ("Cost Center", "@cost_center"),
    ("Gross Overhead", "@rate"),])


choro.add_tools(hover)


## function to reassign source to sorted data

def update_button():
    
    if source.data == comp:
        sortSource = comp_sort

    elif source.data == cc:
        sortSource = cc_sort

    elif source.data == fac:
        sortSource = fac_sort

    
    source.data = sortSource
    
    ## Integral to updating the x-axis!!!https://github.com/bokeh/bokeh/issues/4022
    p.x_range.factors = sortSource['ccName']

## function to reassign source of data

def update_plot(attrname, old, new):

    if select.value == 'Composite':
        newSource = comp
    
    elif select.value == 'Cost Center':
        newSource = cc 
    
    elif select.value == 'Facility':
        newSource = fac
    

    source.data = newSource
    

## update the plot 'on change' of select menu

select.on_change('value', update_plot)


## update the plot 'on click' of button

sortButton.on_click(update_button)


## layout of widgets and plots

layout = column(desc, select, sortButton, p, choro)


## Necessary for updating doc upon widget interaction

curdoc().add_root(layout)


## Use 'save' instead of 'output_file' to output the entire layout to 'index.html' instead of single plot!!

save(layout, "index.html")

show(layout)
