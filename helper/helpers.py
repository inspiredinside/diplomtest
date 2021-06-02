import time
import datetime
import pandas as pd
import ssl


def generate():
    return hex(int(time.mktime(time.strptime('1999-12-31 15:00:00', '%Y-%m-%d %H:%M:%S'))) - time.timezone)


def validate(*args):
    filtered = list(filter(lambda arg: arg != "" and arg is not None, args))
    return len(args) == len(filtered)


def get_forecast(ticker='AAPL', interval='1d'):
    period1 = int(time.mktime(datetime.datetime(2020, 12, 1, 23, 59).timetuple()))
    period2 = int(time.mktime(datetime.datetime(2020, 12, 31, 23, 59).timetuple()))
    # 1d, 1m
    ssl._create_default_https_context = ssl._create_unverified_context
    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
    df = pd.read_csv(query_string)
    df.to_csv('AAPL.csv')
