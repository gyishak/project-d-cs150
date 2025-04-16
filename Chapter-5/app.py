import plotly.graph_objs as go
from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from Results import ResultsC
from Learn import learn_card, footer


app = Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])
western_europe=["Andorra","Austria","Belgium","Denmark","Finland","France","Germany","Greece","Iceland","Ireland",
                "Italy","Liechtenstein","Luxembourg","Monaco","Netherlands (Kingdom of the)","Norway","Portugal","San Marino","Spain",
                "Sweden","Switzerland","United Kingdom of Great Britain and Northern Ireland","Vatican City"]


indicators = {
    "Value": "Value",
}
df= pd.read_csv("assets/amer2.csv")
df=df[df['country'].isin(western_europe)][['country','year','Value']]

death=pd.read_csv("assets/last.csv")
death=death[death['Country'].isin(western_europe)][['Country','Sex','RATE per 100000']]

americaData=pd.read_csv("assets/americaWater.csv")
japanData=pd.read_csv("assets/japanWater.csv")

fig=px.bar(americaData, x="Year", y="Percent", color="Percent")
fig2=px.bar(japanData, x="Year", y="Percent", color="Percent")


app.layout = dbc.Container(
    [
        dbc.Tabs([
            dbc.Tab([learn_card],tab_id="tab-5", label="Learn", className="pb-4"),
dbc.Tab([
        dbc.Row(
            dbc.Col(
                [
                    html.H1(
                        "Population Using Safe Drinking-Water (%) in Western Europe",
                        style={"textAlign": "center"},
                    ),

                    dcc.Graph(id="my-choropleth", figure={}),
                ],
                width=12,
            )
        ),
        dbc.Row([
            dbc.Col(
                [
                    dbc.Label(
                        "Select Years:",
                        className="fw-bold",
                        style={"textDecoration": "underline", "fontSize": 20},
                    ),
                    dcc.RangeSlider(
                        id="years-range",
                        min=2005,
                        max=2021,
                        step=1,
                        value=[2005, 2006],
                        marks={
                            2005: "2005",
                            2006: "'06",
                            2007: "'07",
                            2008: "'08",
                            2009: "'09",
                            2010: "'10",
                            2011: "'11",
                            2012: "'12",
                            2013: "'13",
                            2014: "'14",
                            2015: "'15",
                            2016: "'16'",
                            2017: "'17",
                            2018: "'18",
                            2019: "'19",
                            2020:"'20",
                            2021: "2021"

                        },
                    ),

                ],
                width=6,
            ),
        ]),
        dbc.Row(
            [dbc.Col([
                dbc.Button(
                    id="my-button",
                    children="Submit",
                    color="primary",
                    className="fw-bold d-flex justify-content-end"
                ),
            ],
                width=12,
            )],
        ),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="line-graph", figure={}),
        ])
    ]),
],tab_id="tab-1", label="Western Europe", className="pb-4"),
    dbc.Tab([
        dbc.Row([
            dbc.Col([
                    dbc.Label(
                        "US Population Using Safely Managed Drinking Water Services(%):",
                        className="fw-bold",
                        style={"textDecoration": "underline", "fontSize": 18},
                    ),
                dcc.Graph(id="my-graph", figure=fig),
            ]),
            dbc.Col([
                dbc.Label(
                        "Japan Population Using Safely Managed Drinking Water Services(%):",
                        className="fw-bold",
                        style={"textDecoration": "underline", "fontSize": 18},
                    ),
                dcc.Graph(id="my-graph2", figure=fig2)])
        ]),
 ], tab_id="tab-2", label="Globally", className="pb-4"),
dbc.Tab( [ResultsC],
    tab_id="tab-4", label="Results", className="pb-4"),

        dcc.Store(id="storage", storage_type="session", data={}),
        dcc.Interval(id="timer", interval=1000 * 60, n_intervals=0),
]), footer
    ],

)

@app.callback(Output("line-graph","figure"),Input("my-choropleth", "clickData"),)
def count_line(clickData):
    if clickData is None:
        return go.Figure()

    country = clickData["points"][0]["location"]
    data = death[death["Country"] == country]
    count=df[df["country"]==country]
    if data.empty:
        fit= px.bar(count, x="year", y="Value", hover_data={"country": True},title="Population using safely managed drinking-water services (%)")
        return fit

    figs=px.bar(data,x="Sex", y="RATE per 100000", hover_data={"Country": True}, title="Mortality Rate from Unsafe WASH in 2019")
    return figs


@app.callback(Output("storage", "data"), Input("timer", "n_intervals"), )
def store_data(n_time):
    return df.to_dict("records")


@app.callback(
    Output("my-choropleth", "figure"),
    Input("my-button", "n_clicks"),
    Input("storage", "data"),
    State("years-range", "value"),
)
def update_graph(n_clicks, stored_dataframe, years_chosen):
    dff = pd.DataFrame.from_records(stored_dataframe)
    dff.year=dff.year.astype(int)


    if years_chosen[0] != years_chosen[1]:
        dff = dff[dff.year.between(years_chosen[0], years_chosen[1])]
        dff = dff.groupby(["country"]).mean()
        dff = dff.reset_index()

        fig = px.choropleth(
            data_frame=dff,
            locations="country",
            locationmode="country names",
            color="Value",
            scope="europe",
            hover_data={"country": True},
            labels={
                indicators["Value"]: "Value",
            },
        )
        fig.update_layout(
            geo={"projection": {"type": "natural earth"}},
            margin=dict(l=50, r=50, t=50, b=50),
        )
        return fig

    if years_chosen[0] == years_chosen[1]:
        dff = dff[dff["year"].isin(years_chosen)]
        fig = px.choropleth(
            data_frame=dff,
            locations="country",
            locationmode="country names",
            color="Value",
            scope="europe",
            hover_data={ "country": True},
            labels={
                indicators["Value"]: "Value",
            },
        )
        fig.update_layout(
            geo={"projection": {"type": "natural earth"}},
            margin=dict(l=50, r=50, t=50, b=50),

        )
        return fig


if __name__ == "__main__":
    app.run_server(debug=True)
