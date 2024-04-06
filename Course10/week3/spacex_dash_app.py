# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# filtered_df = spacex_df[spacex_df['Launch Site'].str.contains('KSC')].groupby('class')['class'].count()
# print(filtered_df)
# fig = px.pie(filtered_df, values=list(filtered_df.columns), 
#         names=list(filtered_df.columns), 
#         title='title')
# print(fig)
# exit()

site_options = [{"label":site,"value":site} for site in spacex_df["Launch Site"].unique()]
# Create a dash application
app = dash.Dash(__name__)




# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                  dcc.Dropdown(id='site-dropdown',
                                    options=[{'label': 'All Sites', 'value': 'ALL'}]+site_options,
                                    value='ALL',
                                    placeholder="...Search",
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0',
                                        100: '100'},
                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df.groupby(by='Launch Site')['class'].sum().to_frame()
    if entered_site == 'ALL':        
        fig = px.pie(filtered_df, values='class', 
        names=list(filtered_df.T.columns), 
        title='Total successful launches from All Sites')
    else:  
        filtered_df = spacex_df[spacex_df['Launch Site'].str.contains('KSC')].groupby('class')['class'].count()         
        fig = px.pie(filtered_df, values='class', 
        names=["Failed","Success"], 
        title='Success vs. Failed launches from site '+entered_site) 
    
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(entered_site, payload_range):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])]    
    if entered_site == 'ALL':    
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
            color="Booster Version Category",
            title='Payload and Launch success')
    else:  
        filtered_df = filtered_df[filtered_df['Launch Site'].str.contains(entered_site)]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
            color="Booster Version Category",
            title='Payload and Launch success')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
