# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("Downloads/spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()
sites = spacex_df["Launch Site"].unique().tolist()

colorScheme = px.colors.sequential.Aggrnyl

# Create a dash application
app = dash.Dash(__name__)
app.title = "Akram SpcaeT Project"

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        # dcc.Dropdown(id='site-dropdown',...)
        dcc.Dropdown(
            id="in_site",
            options=[{"label": "All", "value": "All"}]
            + [{"label": x, "value": x} for x in sites],
            value="All",
        ),
        html.Br(),
        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        # dcc.RangeSlider(id='payload-slider',...)
        dcc.RangeSlider(id="in_payload", min=min_payload, max=max_payload, value=[min_payload, max_payload]),
        html.P(id="out_payload"),
        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        # html.Div(dcc.Graph(id='success-payload-scatter-chart')),
        html.Div(dcc.Graph(id="out_payload_chart")),
    ]
)

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output


@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    [Input(component_id="in_site", component_property="value")],
)
def pieChart(site_selected):

    # spacex_df = spacex_df.copy()

    pie_successCount_data = (
        spacex_df.groupby(["Launch Site", "class"])["class"]
        .count()
        .reset_index(name="count")
    )

    success_allSites = pie_successCount_data[pie_successCount_data["class"] == 1]
    pie_chart = px.pie(
        data_frame=success_allSites,
        names="Launch Site",
        values="count",
        color_discrete_sequence=colorScheme,
    )

    if site_selected != "All":

        successFail_oneSite = pie_successCount_data[
            pie_successCount_data["Launch Site"] == site_selected
        ]
        successFail_oneSite["class"] = successFail_oneSite["class"].replace(
            {0: "Fail", 1: "Success"}
        )

        pie_chart = px.pie(
            data_frame=successFail_oneSite,
            names="class",
            values="count",
            color_discrete_sequence=colorScheme,
            
        )
        

    return pie_chart


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    [
        Output(component_id="out_payload", component_property="children"),
        Output(component_id="out_payload_chart", component_property="figure"),
    ],
    Input(component_id="in_payload", component_property="value"),
)
def update_payload(payload_range):
    
    min_selected = payload_range[0]
    max_selected = payload_range[1]
    
    newDF = spacex_df[(spacex_df["Payload Mass (kg)"] > min_selected) & (spacex_df["Payload Mass (kg)"] < max_selected)]
    newDF["class"] = newDF["class"].replace({0: "No", 1: "Yes"})
    
    theFigure = px.scatter(data_frame= newDF, x= "Payload Mass (kg)", y= "class")
    theFigure.update_layout(title = "Success vs Payload", xaxis_title = "Payload Mass (kg)", yaxis_title = "Success")
    
    return [f"({min_selected}, {max_selected})", theFigure]


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
