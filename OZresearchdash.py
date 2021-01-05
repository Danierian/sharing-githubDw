import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import geopandas as gpd
import dash_table
import dash_table.FormatTemplate as FormatTemplate

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
# ------------------------------------------------------------------------------------------
#
# Importing Data
#
# ------------------------------------------------------------------------------------------
PovertyRates = pd.read_csv('PovertyRates.csv', encoding='Latin-1')
#PovertyRates = PovertyRates.set_index('State_name')
unemp = pd.read_csv('unemploymentRates.csv', encoding='Latin-1')
unemp = unemp.set_index('State_name')
medinc = pd.read_csv('medhhinc.csv', encoding='Latin-1')
medinc = medinc.set_index('State_name')
SD = pd.read_csv('povrate_SD.csv', encoding='Latin-1')
SD = SD.set_index('State_name')
cou = pd.read_csv('contiguous_count.csv',encoding='Latin-1')
cou = cou.drop(['Unnamed: 0'], axis=1)

demographics = ['People Living in Poverty', 'Hispanics', 'African Americans', 'Adults without Diploma']

# ------------------------------------------------------------------------------------------
#
# Figure 1 : Lollipop chart
#
# ------------------------------------------------------------------------------------------
fig = go.Figure()
fig.add_trace(go.Scatter(x=PovertyRates['All Tracts'], y=PovertyRates.State_name, mode='markers', name='All Tracts'))
fig.add_trace(go.Scatter(x=PovertyRates['Designated OZ'], y=PovertyRates.State_name, mode='markers', name='Designated OZ'))
fig.add_trace(go.Scatter(x=PovertyRates['OZ eligible'], y=PovertyRates.State_name, mode='markers', name='OZ eligible'))

i = 0
for row in PovertyRates.values:
    fig.add_shape(type="line",
                  x0=row[1], x1=row[3], y0=i, y1=i,
                  line=dict(color="Blue", width=1))
    i = i + 1
    continue

fig.update_layout(
    autosize=False,
    width=750,
    height=1500,
    xaxis_title='Poverty Rate',
    yaxis_title='State',
    paper_bgcolor="white",
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
    "name": "Entire State",
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
    "name": "Entire State",
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
# Figure 5: Median income Average Lollipop Chart
#
# ------------------------------------------------------------------------------------------

fig5 = go.Figure()
fig5.add_trace(go.Scatter(x=medinc['medhhinc'], y=medinc.index, mode='markers', name='All Tracts'))
fig5.add_trace(go.Scatter(x=medinc['OZdes_medinc'], y=medinc.index, mode='markers', name='Designated OZ'))
fig5.add_trace(go.Scatter(x=medinc['OZeligible_medinc'], y=medinc.index, mode='markers', name='OZ eligible'))

i = 0
for row in medinc.values:
    fig5.add_shape(type="line",
                  x0=row[1], x1=row[0], y0=i, y1=i,
                  line=dict(color="Blue", width=1))
    i = i + 1
    continue

fig5.update_layout(
    autosize=False,
    width=750,
    height=1500,
    xaxis_title='Median Income Level',
    yaxis_title='State',
    paper_bgcolor="white",
    title='Median Income Level (State Average)',
    xaxis=dict(
        title='Median Income Level',

        tickformat="${:,}"

    )

)

# ------------------------------------------------------------------------------------------
#
# Figure 6: Standard deviations of Poverty Rates
#
# ------------------------------------------------------------------------------------------

fig6 = go.Figure()
fig6.add_trace(go.Bar(y=SD.povrate_SD,
                      x=SD.index,
                      name='OZ Population',
                      marker_color='green'  # ,text=[30.030,22.33,027.28,022.31]

                      ))
fig6.update_layout(
    title='SD of Poverty Rates (OZ Designated Tracts)',
    autosize=False,
    width=1000,
    height=500,
    xaxis_tickfont_size=12,
    yaxis=dict(title='SD of Poverty Rates',range=[0, .25],tickformat=",.2%"),


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
# Figure 7: Which states used 25% of tracts
#
# ------------------------------------------------------------------------------------------


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
(*i.e US territory tracts). 

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

Even though there is a variation of poverty rates on the state level, it is still apparent that the average poverty rate
on the state level is lower that the average poverty rate for designated OZ tracts. A t-test was used to test the 
significance of this difference in means and there is enough statistical evidence to reject the null hypothesis at the 5% level. 
Conducting the t-test returned a t-statistic of 25.656 and a p-value of 0.000 meaning that the average poverty rate for the state
and the average poverty rate for designated OZ tracts are significantly different.

*_Note: The poverty rate estimates are from 2016 as these are the estimations that were used for designation._


'''),
    dcc.Graph(
        id='Poverty_Rates',
        figure=fig
    ),
   #####the table for poverty rates commented out below
#dash_table.DataTable(
 #   id='Povtable',
  #     {
   #         'id': 'State_name',
    #        'name': 'State',
     #       'type': 'text'

      #'id': 'All Tracts',
       # 'name': 'All Tracts',
        #'type': 'numeric',
        #'format': FormatTemplate.percentage(2)
   # }, {
    #    'id': 'OZ eligible',
     ##  'type': 'numeric',
       # 'format': FormatTemplate.percentage(2)

   # }, {
    ##    'id': 'Designated OZ',
      #  'name': 'OZ Designated ',
       ##'format': FormatTemplate.percentage(2)

  #  }

  #  ],
  #  data=PovertyRates.to_dict('records'),
  #  style_cell=dict(textAlign='center'),
  #  style_header=dict(backgroundColor="royalblue",textColor='White'),
  #  style_data=dict(backgroundColor="lavender")
#),

    html.Br(),
    dcc.Graph(
        id='povrate_SD',
        figure=fig6
    ),
    html.Br(),

    dcc.Graph(
        id='medhhinc',
        figure=fig5
    ),
    dash_table.DataTable(
        id='OZContiguousTable',
        columns=[{
            'id': 'State_name',
            'name': 'State',
            'type': 'text'
        }, {
            'id': '# of OZ',
            'name': '# of OZ',
            'type': 'numeric'

        }, {
            'id': 'Contiguous_Count',
            'name': 'Contiguous Tracts',
            'type': 'numeric'

        },
            {
                'id': 'Percentage',
                'name': 'Percentage Contiguous',
                'type': 'numeric'
                #'format': FormatTemplate.percentage(1)
            }
        ],
        data=cou.to_dict('records'),
        style_cell=dict(textAlign='center'),
        style_header=dict(backgroundColor="royalblue",textColor='White'),
        style_data=dict(backgroundColor="lavender")
    ),
    html.Br(),
    dcc.Markdown('''
#### Labor Metrics by State

Below are some additional economic metrics related to unemployment. Each graph compares the unemployment rate
and labor force participation rate of designated OZs, eligible but not Designated and non eligible census tracts.
The average difference between the unemployment rate for all tracts within the a State and only OZ designated tracts is
3.59%. However,  there are several states with an exceptionally higher difference between State poverty rate and OZ 
designated average poverty rate. These states include : Connecticut : 6.22% , District of Columbia : 8.75%, Florida : 8.05%,
 and Illinois : 11.03%.

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

''')
])

if __name__ == '__main__':
    app.run_server(debug=True)
