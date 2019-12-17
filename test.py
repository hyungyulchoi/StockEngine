from flask import Flask, render_template, request,flash, redirect, session, abort
from flask_bootstrap import Bootstrap
from alpha_vantage.timeseries import TimeSeries
import time
import datetime
import calendar, math
import os
import requests


flag = False
message=""
app = Flask(__name__);
Bootstrap(app)

ts = TimeSeries(key='RZ4TKEIH4QXPN7VB')
data, meta_data = ts.get_daily_adjusted("AAPL")
print(data)

if __name__=='__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=3000)