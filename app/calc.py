import datetime
import time
import asyncio
import aiohttp
import yfinance as yf
from multiprocessing import Pool

tickers = ["SPY", "QQQ", "TSLA", "AMZN", "NFLX", "META", "AAPL", "MSFT", "NVDA", "AMD", "TWTR", "NIO", "GOOGL", "SHOP",
           "BA", "ROKU", "DIA", "MRNA", "BABA", "DIS", "BAC", "JPM", "F", "AMC", "GME", "INTC", "UBER", "SNAP", "SQ",
           "PYPL", "COIN", "MARA", "RIOT", "QCOM", "ZM", "%5ESPX"]

api_key = 'vu0jeGy1YyyZQR2hECjyrauPu4UzOdoq'
url = 'https://api.polygon.io/v3/snapshot/options/{}/O:{}?apiKey=vu0jeGy1YyyZQR2hECjyrauPu4UzOdoq'


def calc(ticker):
    chains = yf.Ticker(ticker).option_chain()
    # start = time.time()
    result = {'Puts': 0, 'Calls': 0}

    def get_tasks(session, type_):
        tasks = []
        for contract in type_:
            tasks.append(session.get(url.format(ticker, contract), ssl=False))
        return tasks

    async def get_options_vol(calls_=True):
        global results
        if calls_:
            data = chains.calls['contractSymbol']
        else:
            data = chains.puts['contractSymbol']
        async with aiohttp.ClientSession() as session:
            tasks = get_tasks(session, data)
            all_resp = await asyncio.gather(*tasks)
            for resp in all_resp:
                if calls_:
                    try:
                        result['Calls'] += (await resp.json())['results']['day']['volume']
                    except KeyError:
                        pass
                else:
                    try:
                        result['Puts'] += (await resp.json())['results']['day']['volume']
                    except KeyError:
                        pass

    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.get_event_loop().run_until_complete(get_options_vol(calls_=True))
    asyncio.get_event_loop().run_until_complete(get_options_vol(calls_=False))
    # asyncio.run(get_options_vol(calls_=True))
    # asyncio.run(get_options_vol(calls_=False))
    # print('Puts Volume: {}'.format(result['Puts']))
    # print('Calls Volume: {}'.format(result['Calls']))
    # print('Puts/Calls Ratio: {}'.format(result['Puts'] / result['Calls']))
    # print('It took {} seconds to make the API calls'.format(time.time() - start))
    return ticker, round(result['Puts'] / result['Calls'], 3)


if __name__ == "__main__":
    p = Pool(8)
    results = {}
    for t in tickers: results[t] = []
    reset = False
    if reset:
        f = open('pcvr.csv', 'w')
        f.write("time,")
        for t in tickers:f.write(f'{t},')
        f.write('\n')
        f.close()

    while datetime.datetime.now().second > 5: time.sleep(1)
    while True:
        start_ = time.time()
        f = open('pcvr.csv', 'a')
        # print('Running...')
        f.write(f"{(datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=5)).strftime('%Y-%m-%d %H:%M')},")
        resp = p.map(calc, tickers)
        for r in resp:
            results[r[0]].append([r[1], (datetime.datetime.now(
                datetime.timezone.utc) - datetime.timedelta(hours=5)).strftime('%Y-%m-%d %H:%M')])
            f.write(f'{r[1]},')
        f.write('\n')
        f.close()
        # print(results)
        # print('Time Taken {}'.format(time.time() - start_))
        # print('\n')
        try:
            time.sleep(60 - (time.time() - start_))
        except Exception:
            time.sleep(120 - (time.time() - start_))
