#!/bin/bash
# shellcheck disable=SC2164
cd Desktop/OptionsAPI2
pip install yfinance
pip install aiohttp
pip install pandas
pip install plotly
pip install flask
pip install flask_restful
python run_pcv.py & python run_flask.py
