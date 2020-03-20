
# Readme

This small python script downloads the current covid-19 data from [Johns Hopkins University](https://github.com/CSSEGISandData/2019-nCoV) and displays the new infections for a selection of countries.
The countries can be easily changed by editing the file.
Additionally, the program fits exponential curves to the last N days per country and reports three numbers `k`, `b`, `d` per country where `k` and `b` are the coefficients in `y = exp(kx + b)`
and `d` is the number of days it takes for the number of infections to double.

There are two command line switches:
```
-d DAYS, --days DAYS  show only last N days [default 20]
-f FIT, --fit FIT     fit curve to last N days [default 5]
```

You need `numpy` and `scipy` installed and a working internet connection to download the data.
