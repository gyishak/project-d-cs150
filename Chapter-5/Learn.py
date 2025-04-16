from dash import  html, dcc
import dash_bootstrap_components as dbc


learn_text = dcc.Markdown(
    ''' 
Water is an essential part of living, but unclean water can attribute to multiple illness like Cholera, Polio, Typhoid, and even death. This crisis also has effect on the Women's Crisis, Health Crisis, Climate Crisis, and Children's and Education Crisis. But is the Water Crisis still relevant in today's time? Explore this Dashboard to find out. 
Please explore the 4 tabs :

1. Western Europe:
This tab shows the Population using safely managed drinking-water services (%) of Western European countries over the years 2005 to 2021. 

2. Globally:
These two bar graphs show the Population using safely managed drinking-water services (%) of the United States and Japan.

3. Results:
Displays all the raw data.

What do you any trends with the population using safe drinking water over the span of 16 years?


  After this, take a look at 'Globally' tab to see if you notice this same trend in terms of the United States and Japan.


  Please look through the Results tab to see all the data used for this study.

  Thank you!


'''
)
# ========= Learn Tab  Components
learn_card = dbc.Card(
    [
        dbc.CardHeader("Hello!"),
        dbc.CardBody(learn_text),
    ],
)
footer = html.Div(
    dcc.Markdown(
        """
         [Population using safely managed drinking-water services (%)](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/population-using-safely-managed-drinking-water-services-(-))
         [Mortality rate attributed to unsafe WASH services (per 100 000 population)](https://data.who.int/indicators/i/C123B15/ED50112)

        """
    ),
    className="p-2 mt-5 text-white small",
)