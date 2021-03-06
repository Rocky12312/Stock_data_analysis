import os
import re
import sys
import dash
from datetime import datetime
import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import pandas_datareader.data as web
from datetime import date, timedelta
from dash.dependencies import Input, Output, State


#Launching the app
app = dash.Dash()


nsdq_df = pd.read_csv("companylist.csv")
nsdq_df.set_index("Symbol", inplace=True)
options = []
for tic in nsdq_df.index:
    options.append({"label": "{} {}".format(tic, nsdq_df.loc[tic]["Name"]), "value": tic})


#Creating a div that contain headers, boxes, graphs
app.layout = html.Div([
    html.H1("Stock Dashboard"),
    html.Div([
        html.H3("Select the desired stock symbol:", style={"paddingRight": "30px"}),
        dcc.Dropdown(
            id="my_ticker_symbol",
            options=options,
            value=["TSLA"],
            multi=True
        )
     ],
        style={"display": "inline-block", "verticalAlign": "top"}),
    html.Div([
        html.H3("Select start and end dates:"),
        dcc.DatePickerRange(
            id="my_date_picker",
            min_date_allowed=datetime(2015, 1, 1),
            max_date_allowed=datetime.today(),
            start_date=datetime(2018, 1, 1),
            end_date=datetime.today()
        )
    ],
        style={"display": "inline-block"}),
    html.Div([
        html.Button(
            id="submit-button",
            n_clicks=0,
            children="Submit",
            style={"fontSize": 24, "marginLeft": "30px"}
        ),
    ],
        style={"display": "inline-block"}),
    dcc.Graph(
        #Id to graph
        id="My Graph",
        figure={
            "data": [
                {
                    "x": [1, 2],
                    "y": [3, 4]
                }
            ]
        }
    )
])


#Adding a callback function
@app.callback(
    Output("My Graph", "figure"),
    [Input("submit-button", "n_clicks")],
    [
        State("my_ticker_symbol", "value"),
        State("my_date_picker", "start_date"),
        State("my_date_picker", "end_date")
    ]
)
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    traces = []
    for tic in stock_ticker:
        df = web.DataReader(tic, "iex", start, end, api_key="##Enter your api token##")
        traces.append({"x": df.index, "y": df.close, "name": tic})
    fig = {
        "data": traces,
        "layout": {"title": ", ".join(stock_ticker) + " Closing Prices"}
    }
    return fig


if __name__ == "__main__":
    app.run_server()



