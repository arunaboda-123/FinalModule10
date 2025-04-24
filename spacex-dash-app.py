# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read SpaceX launch data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get min and max payload mass for slider configuration
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] +
                [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',  # Default selection
        placeholder="Select a Launch Site",
        searchable=True
    ),
    
    html.Br(),

    # TASK 2: Pie Chart for Success Count
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Add a Range Slider to Select Payload Range
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload, max=max_payload, step=1000,
        marks={i: str(i) for i in range(int(min_payload), int(max_payload) + 1, 2000)},
        value=[min_payload, max_payload]
    ),

    # TASK 4: Scatter Plot for Payload vs Launch Success
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# TASK 2: Callback for Pie Chart based on selected site
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value'))
def update_pie_chart(selected_site):
    if selected_site == "ALL":
        fig = px.pie(spacex_df, values='class', names='Launch Site', title="Success Rates for All Sites")
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class', title=f"Success vs Failure for {selected_site}")
    return fig

# TASK 4: Callback for Scatter Chart based on Site and Payload Range
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    # Filter data based on payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]

    # If a specific site is selected, filter further
    if selected_site != "ALL":
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color="Booster Version",
                     title="Payload Mass vs Launch Success")
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)