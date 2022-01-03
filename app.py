import yfinance as yf
import os

from typing import Pattern
from flask import Flask, render_template, request
from patterns import candlestick_patterns


app = Flask(__name__)

@app.route("/")
def index():
    pattern = request.args.get('pattern', None)
    if pattern:
        os.listdir('datasets/daily')
    return render_template('index.html', candlestick_patterns = candlestick_patterns)

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