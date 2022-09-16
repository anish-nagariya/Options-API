import json

import pandas as pd
import plotly.utils
from flask import render_template

from app import app


@app.route("/")
def start():
    return "Welcome to the Options Application"


@app.route('/xx/<ticker>')
def display(ticker):
    if ticker == 'SPX':
        ticker = '%5ESPX'
    df = pd.read_csv('pcvr.csv')
    df = pd.DataFrame(df)
    df = pd.DataFrame(df[['time', ticker]])
    df = df.reindex(index=df.index[::-1])
    df = df.reset_index()
    df = df.drop(['index'], axis=1)
    pd.options.plotting.backend = "plotly"
    fig = df[::-1].plot(x='time', y=ticker, width=1100, height=650)
    graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html', ticker=ticker,
                           ratio=df[ticker].iloc[0],
                           tables=[df.to_html(classes='data')],
                           titles=df.columns.values,
                           graphJSON=graph)

