import yfinance as yf
import os
import pandas as pd
import talib
import csv

from typing import Pattern
from flask import Flask, render_template, request
from patterns import candlestick_patterns


app = Flask(__name__)

@app.route("/")
def index():
    pattern = request.args.get('pattern', None)
    stocks = {}
    results = {}

    with open('datasets/symbols.csv') as f :
         for row in csv.reader(f):
             stocks[row[0]] = {'company' : row[1]}

    if pattern:
        datafiles = os.listdir('datasets/daily')
        for filename in datafiles:
            df = pd.read_csv('datasets/daily/{}'.format(filename))
                

            try:
                if pattern == 'ALL TICKER' :
                    symbol = filename.split('.')[0]
                    stocks[symbol][pattern] = 'Neutral'
                    
                else :
                    pattern_function = getattr(talib, pattern)
                    symbol = filename.split('.')[0]
                    results = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
                    last = results.tail(1).values[0]
                print(results)
                #shows which ticker triggered the pattern
                if last > 0 :
                    stocks[symbol][pattern] = 'bullish'
                elif last < 0:
                    stocks[symbol][pattern] = 'bearish'
                else:
                    stocks[symbol][pattern] = None
            except Exception as e:
                pass
    return render_template('index.html', candlestick_patterns = candlestick_patterns, stocks=stocks, pattern=pattern)

@app.route('/snapshot')
def snapshot():
    with open('datasets/symbols.csv') as f:
        symbols = f.read().splitlines()
        for symbols in symbols:
            ticker = symbols.split(',')[0]
            df = yf.download(ticker, start="2021-01-01", end="2021-12-31")
            df.to_csv('datasets/daily/{}.csv.'.format(ticker))

    return {
        'code': 'success'
    }