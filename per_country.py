#! /usr/bin/env python3

import argparse
import urllib.request
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

data_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"

idx_first_day = 4

colors = {
        "US"      : "r",
        "Austria" : "m",
        "Italy"   : "g",
        "Spain"   : "y",
        "France"  : "b",
        "Germany" : "k",
        }

values = {}

parser = argparse.ArgumentParser(description='Plot COVID-19 infection data.')
parser.add_argument('-d', '--days', default=30, type=int, help='show only last N days [default 20]')
parser.add_argument('-f', '--fit',  default=5,  type=int, help='fit curve to last N days [default 5]')
args = parser.parse_args()

content = map(lambda r : r.decode('utf-8'), urllib.request.urlopen(data_url))
reader = csv.reader(content, delimiter=',', quotechar='|')
header = next(reader)
idx_first_day = max(idx_first_day, len(header) - args.days)
labels = header[idx_first_day:]
xdata  = [i for i in range(0, len(labels))]

for row in reader:
    cntry = row[1]
    if cntry in colors:
        ydata = [ int(v) for v in row[idx_first_day:] ]
        if not cntry in values:
            values[cntry] = ydata
        else:
            v = values[cntry]
            values[cntry] = [ v[i] + ydata[i] for i in range(0, len(ydata)) ]

def func(x, k, b):
    return np.exp(k * x + b)

for cntry, row in values.items():
    ydata = [ int(v) for v in row ]
    c = colors[cntry]
    plt.plot(xdata, ydata, c+'x')

    last = -args.fit
    popt, pconv = curve_fit(func, xdata[last:], ydata[last:])
    yfit = [ func(x, popt[0], popt[1]) for x in xdata ]
    k = popt[0]
    b = popt[1]
    d = math.log(2) / k
    lab = '{} k={:.2f} b={:.2f} d={:.2f}'.format(cntry, k, b, d)
    plt.plot(xdata, yfit, c, label=lab)

plt.xticks(xdata, labels, rotation='vertical')
plt.ylabel('y')
plt.yscale('log')
plt.legend()
plt.show()
