import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import geopandas as gpd
import dash_table
import dash_table.FormatTemplate as FormatTemplate

import numpy
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# ------------------------------------------------------------------------------------------
#
# Importing Data
#
# ------------------------------------------------------------------------------------------
GroupByYear=pd.read_csv('Section_8_Newly_Assisted.csv',encoding='Latin-1')
fig = px.line(GroupByYear, x=GroupByYear.S8_1_StartDate, y='S8_Total_AssistingUnits')
fig.update_layout(
    xaxis_title='Year',
    yaxis_title="# of Newly Assisted Units",
    title='Section 8 Newly Assisted Units by Year',
    yaxis=dict(tickformat=",")
)


# There are currently 21,769 properties that are listed as active Section 8 with 1,346,652 units are being assisted by Section 8. Of these properties, there are 1015 properties that have a second Section 8 subsidy that covers an additional 57,549 units.This a total of 1,404,201 units being actively assisted by Section 8.

import plotly.graph_objects as go
UnitsAssistedperYear=pd.read_csv('Total_Assisted_Per_yEAR.csv',encoding='Latin-1')

fig2 = go.Figure()
# fig.add_trace(go.Scatter(x=UnitsAssistedperYear.Year_End,y=UnitsAssistedperYear['FHA'],name='FHA'))
# fig.add_trace(go.Scatter(x=UnitsAssistedperYear.Year_End,y=UnitsAssistedperYear['LIHTC'],name='LIHTC'))
fig2.add_trace(go.Scatter(x=UnitsAssistedperYear.Year_End, y=UnitsAssistedperYear['Section_8'], name='Section 8'))
# fig.add_trace(go.Scatter(x=HousingStock.index, y = HousingStock['HousingStock'],name = 'Housing Stock'))


fig2.update_layout(
    xaxis_title='Year',
    yaxis_title=' Assisted Units per Year',
    title='Assisted Number of Units by Subsidy per Year',
    yaxis=dict(tickformat=",")

)

app.layout = html.Div([
    html.H1("Section 8", style={'text-align': 'center'}),

    html.Div(id='output_container', children=[]),
    html.Br(),
    dcc.Markdown('''
  *The data used comes from the Perservation Database 


'''),
    dcc.Graph(
        id='NewlyAssisted',
        figure=fig
    ),
    html.Br(),
    dcc.Markdown('''
    The graph above shows how many units entered the Section 8 subsidy per year.
'''),
    dcc.Graph(
        id='SubsidyPerYear',
        figure=fig2
    ),
html.Br(),
    dcc.Markdown('''
    The graph above shows the total number of units assisted by the Section 8 subsidy in a given year.
'''),

])

if __name__ == '__main__':
    app.run_server(debug=True)
