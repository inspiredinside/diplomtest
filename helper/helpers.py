import os
import time
import datetime
import pandas as pd
import ssl
import uuid


def generate_filename(file_extension):
    return str(uuid.uuid4()) + '.' + file_extension


def validate(*args):
    filtered = list(filter(lambda arg: arg != "" and arg is not None, args))
    return len(args) == len(filtered)


def convert_dates_to_epoch_format(start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%f%z")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    start_date, end_date = list(map((
        lambda x: int(
            time.mktime(x.replace(microsecond=0, second=00, tzinfo=None, hour=23, minute=59).timetuple()))),
        [start_date, end_date]))
    return start_date, end_date


def get_forecast(period1, period2, ticker='AAPL', interval='1d'):
    generated_filename = generate_filename('csv')
    out_dir = './data'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    fullname = os.path.join(out_dir, generated_filename)
    print(fullname)
    # 1d, 1m
    ssl._create_default_https_context = ssl._create_unverified_context
    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
    df = pd.read_csv(query_string)
    df.to_csv(fullname, index=False)
    return generated_filename
