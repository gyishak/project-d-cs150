from dash import Dash, dash_table
from dash import  html
import dash_bootstrap_components as dbc
import pandas as pd

western_europe=["Andorra","Austria","Belgium","Denmark","Finland","France","Germany","Greece","Iceland","Ireland",
                "Italy","Liechtenstein","Luxembourg","Monaco","Netherlands (Kingdom of the)","Norway","Portugal","San Marino","Spain",
                "Sweden","Switzerland","United Kingdom of Great Britain and Northern Ireland","Vatican City"]

df= pd.read_csv("assets/amer2.csv")
df=df[df['country'].isin(western_europe)][['country','year','Value']]
df = df.to_dict('records')

death=pd.read_csv("assets/last.csv")
death=death[death['Country'].isin(western_europe)][['Country','Sex','RATE per 100000']]
death = death.to_dict('records')

americaData=pd.read_csv("assets/americaWater.csv")
americaData = americaData.to_dict('records')
japanData=pd.read_csv("assets/japanWater.csv")
japanData = japanData.to_dict('records')

DataTable=dash_table.DataTable(
   id="DataTable",
   columns=[
               {"name": "country", "id": "country"},
               {"name": "year ", "id": "year"},
               {"name": "Value", "id": "Value"},
           ],
   data=df,
   page_size=15,
   style_table={"overflowX": "scroll"}
)
death_table=dash_table.DataTable(
   id="death_table",
   columns=[
       {"name": "Country", "id": "Country"},
       {"name": "Sex ", "id": "Sex"},
       {"name": "RATE per 100000", "id": "RATE per 100000"},
           ],
   data=death,
   page_size=15,
   style_table={"overflowX": "scroll"}
)
americaTable=dash_table.DataTable(
   id="americaTable",
   columns=[
       {"name": "Year", "id": "Year"},
       {"name": "Percent in America ", "id": "Percent"},

           ],
   data=americaData,
   page_size=15,
   style_table={"overflowX": "scroll"}
)
japanTable = dash_table.DataTable(
    id="japanTable",
    columns=[
        {"name": "Year", "id": "Year"},
        {"name": "Percent in Japan", "id": "Percent"},

    ],
    data=japanData,
    page_size=15,
    style_table={"overflowX": "scroll"}
)

ResultsC= dbc.Card(
   [
       dbc.CardHeader(""),
       html.Div([DataTable, death_table, americaTable, japanTable]),
   ],
   className="mt-4",
)