import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import geopandas as gpd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
# ------------------------------------------------------------------------------------------
#
# Importing Data
#
# ------------------------------------------------------------------------------------------
PovertyRates = pd.read_csv('PovertyRates.csv', encoding='Latin-1')
PovertyRates=PovertyRates.set_index('State_name')
unemp = pd.read_csv('unemploymentRates.csv', encoding='Latin-1')
unemp=unemp.set_index('State_name')
demographics = ['People Living in Poverty', 'Hispanics', 'African Americans', 'Adults without Diploma']

# ------------------------------------------------------------------------------------------
#
#Figure 1 : Lollipop chart
#
# ------------------------------------------------------------------------------------------
fig = go.Figure()
fig.add_trace(go.Scatter(x=PovertyRates['All Tracts'], y=PovertyRates.index, mode='markers', name='All Tracts'))
fig.add_trace(go.Scatter(x=PovertyRates['Designated OZ'], y=PovertyRates.index, mode='markers', name='Designated OZ'))
fig.add_trace(go.Scatter(x=PovertyRates['OZ eligible'], y=PovertyRates.index, mode='markers', name='OZ eligible'))

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
    paper_bgcolor="White",
    title='Average Poverty Rate by Tract Designation and State, 2012-2016',
    xaxis=dict(
        title='Percentages',

        tickformat=',.2%',
        range=[0, .7]

    )

)
# ------------------------------------------------------------------------------------------
#
# Figure 2 : Demographics
#
# ------------------------------------------------------------------------------------------
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
    title='Demographics of Opportunity Zones, 2012-2016',
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
# ------------------------------------------------------------------------------------------
#
# Figure 3 : Unemployment Graphs
#
# ------------------------------------------------------------------------------------------
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
# ------------------------------------------------------------------------------------------
#
# Figure 4 : Labor Force Participation
#
# ------------------------------------------------------------------------------------------
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
# ------------------------------------------------------------------------------------------
#
# Creating app
#
# ------------------------------------------------------------------------------------------
app.layout = html.Div([
    html.H1("Characteristics of Opportunity Zones", style={'text-align': 'center'}),

    html.Div(id='output_container', children=[]),
    html.Br(),
    dcc.Markdown('''
  *The data used in this preliminary analysis comes from the 2016 American Community Survey (ACS), five year estimates*  
#### Opportunity Zone Selection Process
To be eligible for designation, a census tract must 
* Have a poverty rate of at least 20 percent; or
* Have a median income below 80 percent of the State or metropolitan area
* Be contiguous with a census tract meeting one of the above conditions and have median income less than 125% of the 
qualifying contiguous census tract. 

According to the analysis, there are 8,540 low-income tracts and 245 contiguous income tracts. These numbers are 
compared with the Council of Economic Advisors (CEA) report that has 8,537 low-income tracts and 229 contiguous. 
The difference in numbers come from census tracts that may have been split and has the same census tract number 
(*i.e pennisula tracts). 

The data provided also has geographical capabilities enabling the mapping of eligible census tracts that meet the 
qualifications above as well as the census tracts that are currently designated as Opportunity Zones.
*graph is available* 

#### Demographics
Opportunity Zones were created in an attempt to lower capital taxes but with a focus on distressed communities. Below
is a presentation of the differences in designated and non-designated census tracts. The analysis finds that the average 
poverty rate for census tracts designated as OZs are almost double that of all other census tracts and have higher shares
of Hispanics, African Americans, and Adults without Diploma. This is good to see as the purpose behind OZs is to serve areas
that are the more impoverished communities in the United States. 

'''),
    dcc.Graph(
        id='Demographics',
        figure=fig2
    ),
html.Br(),
    dcc.Markdown('''
#### Poverty Rates

The CEA states that, *"Governors could designate up to 25 percent of their qualifying census tracts, or up to 25 tracts
for those States with fewer than 100 eligible tracts. Eligible, contiguous tracts were restricted
to make up no more than 5 percent of designated OZs in any State. "*

The above figure shows that on average, OZs have higher poverty rates than non-designated tracts but it is important
to dive a little deeper to see if this holds true on a state level. Below is a figure that compares the 
average poverty rate of designated OZs, eligible OZs (not designated), and non-eligible census tracts on a state level.
The figure below shows that for every state, there is a higher average poverty rate for the designated OZs compared to
eligible OZs (not designated), and non-eligible census tracts.

*_Note: The poverty rate estimates are from 2016 as these are the estimations that were used for designation._


'''),
    dcc.Graph(
        id='Poverty_Rates',
        figure=fig
    ),
html.Br(),
    dcc.Markdown('''
#### Labor Metrics by State

Below are some additional economic metrics related to unemployment. Each graph compares the unemployment rate
and labor force participation rate of designated OZs, eligible but not Designated and non eligible census tracts.

'''),
    dcc.Graph(
        id='unemployment',
        figure=fig3
    ),
    dcc.Graph(
        id='laborforce',
        figure=fig4
    ),
html.Br(),
    dcc.Markdown('''
#### Next Steps..

After conducting this preliminary analysis, the hope is to use this information as the building blocks for deeper 
analysis. After speaking with Randall Goodnight and Leon Vertz, one additional source of data is CBRE analytics 
(*comparable to dodge data*). This particular data set goes back to 2000 and has information on construction and 
development projects in areas. Each project has lat/long, zip code, county, and state information. This dataset has 
information which includes start date, stage of planning, as well as contact information on owner, contractors and 
architects. 

Given the possible geo-capabilites, it may be possible to overlay markers representing construction projects that 
have been started since 2015 on top of the graph that we already have displaying eligible and designated census tracts.
It may take some time given it is raw data that stills needs to be clean and is currently not presented on the census 
tract level. However, we do have exact lat/long coordinates and it is rumored that HUD users has a crosswalk between 
zip codes and census tracts. 

'''),
    html.Br(),
    html.Br()
])

if __name__ == '__main__':
    app.run_server(debug=True)
