import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import geopandas as gpd





external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app.server
PovertyRates=pd.read_csv('PovertyRates.csv',encoding='Latin-1')
unemp=pd.read_csv('unemploymentRates.csv',encoding='Latin-1')
demographics =[ 'People Living in Poverty','Hispanics','African Americans', 'Adults without Diploma']

fig = go.Figure()
fig.add_trace(go.Scatter(x=PovertyRates['All Tracts'], y=PovertyRates.index, mode='markers', name='All Tracts'))
fig.add_trace(go.Scatter(x=PovertyRates['Designated OZ'], y=PovertyRates.index, mode='markers', name='Designated OZ'))
fig.add_trace(go.Scatter(x=PovertyRates['OZ eligible'], y=PovertyRates.index, mode='markers', name='OZ eligible'))
fig.add_shape(type="line",
              x0=PovertyRates['All Tracts'], x1=PovertyRates['Designated OZ'], y0=1, y1=len(PovertyRates.index) + 1,
              line=dict(color="Black", width=3)
              )
i = 0
for row in PovertyRates.values:
    fig.add_shape(type="line",
                  x0=row[0], x1=row[2], y0=i, y1=i,
                  line=dict(color="Blue", width=1))
    i = i + 1
    continue

fig.update_layout(
    autosize=False,
    width=750,
    height=1500,
    xaxis_title='Poverty Rate',
    yaxis_title='State',
    paper_bgcolor="bisque",
    title='Poverty Rates',
    xaxis=dict(
        title='Percentages',

        tickformat=',.2%',
        range=[0, .5]

    )

)

fig2 = go.Figure()
fig2.add_trace(go.Bar(x=demographics,
                     y=[.30030, .2233, 0.2728, 0.2231],
                     name='OZ Population',
                     marker_color='red'  # ,text=[30.030,22.33,027.28,022.31]

                     ))
fig2.add_trace(go.Bar(x=demographics,
                     y=[0.1624, 0.1526, 0.1216, 0.1264],
                     name='Non-OZ Population',
                     marker_color='rgb(2, 88, 255)'

                     ))
# fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig2.update_layout(
    title='Demographics of Opportunity Zones',
    autosize=False,
    width=800,
    height=500,
    xaxis_tickfont_size=12,
    yaxis=dict(
        title='Percentages',
        titlefont_size=16,
        tickfont_size=14,
        tickformat=',.2%',
        range=[0, .4]

    ),
    legend=dict(
        x=1,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15,  # gap between bars of adjacent location coordinates.
    bargroupgap=0.1  # gap between bars of the same location coordinate.
)
trace1 = {
    "name": "US",
    "type": "bar",
    "x": unemp.index,
    "y": unemp.unemp,
    "marker": {
        "line": {
            "color": "orangered",
            "width": 3
        },
        "color": "orangered"
    }
}
trace2 = {
    "name": "OZ",
    "type": "bar",
    "x": unemp.index,
    "y": unemp.OZdes_umemp,
    "marker": {
        "line": {
            "color": "steelblue",
            "width": 3
        },
        "color": "steelblue"
    }
}
trace3 = {
    "name": "Non OZ (but Eligible)",
    "type": "bar",
    "x": unemp.index,
    "y": unemp.OZ_eligible,
    "marker": {
        "line": {
            "color": "purple",
            "width": 3
        },
        "color": "purple"
    }
}


data1 = [trace2, trace3, trace1]

layout = {

    "title": "Unemployment",
    "xaxis": {
        "ticks": "",
        #  "autotick": True,
        "showgrid": False,
        "showline": True,
        "zeroline": False,
        "autorange": True,
        "showticklabels": True
    },
    "yaxis": {
        "ticks": "",
        # "autotick": True,
        "showgrid": False,
        "showline": True,
        "zeroline": False,
        "autorange": True,
        "showticklabels": True,
        'tickformat': ',.2%',
        'range': [0, 1]
    }
    ,
    "yaxis2": {
        "side": "right",
        "ticks": "",
        # "autotick": True,
        "showgrid": False,
        "showline": True,
        "zeroline": False,
        "autorange": True,
        "overlaying": "y",
        'tickformat': ',.2%',
        'range': [0, 1]

    },
    "barmode": "overlay"
}
fig3 = go.Figure(data=data1, layout=layout)

fig3.update_layout(
    autosize=False,
    width=1750,
    height=700,
    xaxis_title='States',
    yaxis_title='Umemployment Rate',
    paper_bgcolor="White",
)

trace4 = {
    "name": "US",
    "type": "bar",
    "x": unemp.index,
    "y": unemp.lf_pr,
    "marker": {
        "line": {
            "color": "orangered",
            "width": 3
        },
        "color": "orangered"
    }
}
trace5 = {
    "name": "OZ",
    "type": "bar",
    "x": unemp.index,
    "y": unemp.lf_pr_OZdes,
    "marker": {
        "line": {
            "color": "steelblue",
            "width": 3
        },
        "color": "steelblue"
    }
}
trace6 = {
    "name": "Non OZ (but Eligible)",
    "type": "bar",
    "x": unemp.index,
    "y": unemp.lf_pr_OZeligible,
    "marker": {
        "line": {
            "color": "purple",
            "width": 3
        },
        "color": "purple"
    }
}
data4 = [trace4, trace6, trace5]

layout = {

    "title": "Labor Force Participation",
    "xaxis": {
        "ticks": "",
        #  "autotick": True,
        "showgrid": False,
        "showline": True,
        "zeroline": False,
        "autorange": True,
        "showticklabels": True
    },
    "yaxis": {
        "ticks": "",
        # "autotick": True,
        "showgrid": False,
        "showline": True,
        "zeroline": False,
        "autorange": True,
        "showticklabels": True,
        'tickformat': ',.2%',
        'range': [0, 1]
    }
    ,
    "yaxis2": {
        "side": "right",
        "ticks": "",
        # "autotick": True,
        "showgrid": False,
        "showline": True,
        "zeroline": False,
        "autorange": True,
        "overlaying": "y",
        'tickformat': ',.2%',
        'range': [0, 1]

    },
    "barmode": "overlay"
}
fig4 = go.Figure(data=data4, layout=layout)

fig4.update_layout(
    autosize=False,
    width=1750,
    height=700,
    xaxis_title='States',
    yaxis_title='Umemployment Rate',
    paper_bgcolor="White",
)

app.layout = html.Div([
    html.H1("Opportunity Zone Research", style={'text-align': 'center'}),



    html.Div(id='output_container', children=[]),
    html.Br(),
dcc.Markdown('''
### Opportunity Zones

'''),
dcc.Graph(
        id='Poverty_Rates',
        figure=fig
    ),
    dcc.Graph(
        id='Demographics',
        figure=fig2
    ),

    dcc.Graph(
        id='unemployment',
        figure=fig3
    ),
    dcc.Graph(
        id='laborforce',
        figure=fig4
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)