# coding: utf-8

# DO NOT EDIT
# Autogenerated from the notebook statespace_arma_0.ipynb.
# Edit the notebook and then sync the output with this file.
#
# flake8: noqa
# DO NOT EDIT

# # Autoregressive Moving Average (ARMA): Sunspots data

# This notebook replicates the existing ARMA notebook using the
# `statsmodels.tsa.statespace.SARIMAX` class rather than the
# `statsmodels.tsa.ARMA` class.

import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt

import statsmodels.api as sm

from statsmodels.graphics.api import qqplot

# ## Subspots Data

print(sm.datasets.sunspots.NOTE)

dta = sm.datasets.sunspots.load_pandas().data

dta.index = pd.Index(sm.tsa.datetools.dates_from_range('1700', '2008'))
del dta["YEAR"]

dta.plot(figsize=(12, 4))

fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(dta.values.squeeze(), lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(dta, lags=40, ax=ax2)

arma_mod20 = sm.tsa.statespace.SARIMAX(
    dta, order=(2, 0, 0), trend='c').fit(disp=False)
print(arma_mod20.params)

arma_mod30 = sm.tsa.statespace.SARIMAX(
    dta, order=(3, 0, 0), trend='c').fit(disp=False)

print(arma_mod20.aic, arma_mod20.bic, arma_mod20.hqic)

print(arma_mod30.params)

print(arma_mod30.aic, arma_mod30.bic, arma_mod30.hqic)

# * Does our model obey the theory?

sm.stats.durbin_watson(arma_mod30.resid)

fig = plt.figure(figsize=(12, 4))
ax = fig.add_subplot(111)
ax = plt.plot(arma_mod30.resid)

resid = arma_mod30.resid

stats.normaltest(resid)

fig = plt.figure(figsize=(12, 4))
ax = fig.add_subplot(111)
fig = qqplot(resid, line='q', ax=ax, fit=True)

fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(resid, lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(resid, lags=40, ax=ax2)

r, q, p = sm.tsa.acf(resid, qstat=True)
data = np.c_[range(1, 41), r[1:], q, p]
table = pd.DataFrame(data, columns=['lag', "AC", "Q", "Prob(>Q)"])
print(table.set_index('lag'))

# * This indicates a lack of fit.

# * In-sample dynamic prediction. How good does our model do?

predict_sunspots = arma_mod30.predict(start='1990', end='2012', dynamic=True)

fig, ax = plt.subplots(figsize=(12, 8))
dta.loc['1950':].plot(ax=ax)
predict_sunspots.plot(
    ax=ax, style='r')


def mean_forecast_err(y, yhat):
    return y.sub(yhat).mean()


mean_forecast_err(dta.SUNACTIVITY, predict_sunspots)
