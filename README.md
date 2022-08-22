# Puts to Calls Volume Ratio :chart_with_upwards_trend:

Get the puts to calls volume ratio for a list of tickers

## Description

This project is aimed towards calculating the puts to calls volume ratio. We are looking at all the option contracts with the closest expiry date. More information on the puts to calls ratio can be found here: https://www.investopedia.com/ask/answers/06/putcallratio.asp. With this data, we plan on forecasting the trend of the underlying security and what the current market sentiment is. More information about this can be found on https://www.investopedia.com/trading/forecasting-market-direction-with-put-call-ratios/. 

## Getting Started

### Dependencies
Any OS should work, I recommend you install PyCharm to make everything easier. 

https://www.jetbrains.com/pycharm/download/ - You can either get the community option or the premium one

Open this github repository as a pycharm project. 

### Executing program

* Execute the following line in the terminal/console
```
pip install -r requirements.txt
```

* Execute the following line in the terminal/console. Wait 2-3 minutes after executing the line. 
```
python3 run_pcv.py
```
* Open a new terminal, Execute the following line in the terminal/console
```
python3 run_flask.py
```

Navigate to http://127.0.0.1:5000/{ticker} where {ticker} represents the data of which symbol you want to view. Please enter "%5SPX" for SPX. 

To reset the data, (Let's say you want to clear previous day's data) go to run_pcv.py and replace line 62 with ```reset = True```

## Help

For any help please message me. 

```
[Unit]
Description=A simple Flask uWSGI application
After=network.target

[Service]
User=anish
Group=www-data
WorkingDirectory=/home/anish/app
Environment="PATH=/home/anish/app/env/bin"
ExecStart=/home/anish/app/env/bin/uwsgi --ini app.ini

[Install]
WantedBy=multi-user.target
```
