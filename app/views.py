from app import app

import json
import plotly.utils
import pandas as pd
from flask import Flask, render_template


@app.route('/<ticker>')
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
    return render_template('base.html', ticker=ticker,
                           ratio=df[ticker].iloc[0],
                           tables=[df.to_html(classes='data')],
                           titles=df.columns.values,
                           graphJSON=graph)
