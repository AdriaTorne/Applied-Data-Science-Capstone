# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Get the options
options = [{'label': 'All Sites', 'value': 'ALL'}]
values = spacex_df['Launch Site'].unique()
for value in values:
    options.append({'label': value, 'value': value})
print(options)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                html.Div(dcc.Dropdown(id='site-dropdown',
                                                     options=options, 
                                                     value='ALL',
                                                     placeholder="place holder here",
                                                     searchable=True)),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Div(dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={i: str(i) for i in range(0, 10001, 1000)},  # Marca cada 1000
                                                value=[min_payload, max_payload])),
                                #dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, 
                     values='class', 
                     names='Launch Site', 
                     title='Total Success Launched by ALL Sites')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_counts = filtered_df['class'].value_counts()

        # return the outcomes piechart for a selected site
        fig = px.pie(success_counts, 
                     values=success_counts.values,
                     names=success_counts.index, 
                     title='Total Success Launched by Site ' + entered_site)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, payload):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)']>payload[0])&
                            (spacex_df['Payload Mass (kg)']<payload[1])]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df,
                         x='Payload Mass (kg)', 
                         y='class', 
                         color='Booster Version Category', 
                         title='Correlation between Payload and Success for all Sides')
        return fig
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == entered_site)&
                                (spacex_df['Payload Mass (kg)']>payload[0])&
                                (spacex_df['Payload Mass (kg)']<payload[1])]
        fig = px.scatter(filtered_df,
                         x='Payload Mass (kg)', 
                         y='class', 
                         color='Booster Version Category', 
                         title='Correlation between Payload and Success for ' + entered_site)
        
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
