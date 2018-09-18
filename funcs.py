import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation, performance_metrics
from fbprophet.plot import plot_cross_validation_metric, plot_yearly, plot_forecast_component
from time import strptime

def df_for_forecast(df, column):
    """Given dataframe df indexed by datetime,
    gives correctly formatted input for Prophet.fit(),
    namely a dataframe with two columns:
    'ds'=date and 'y'=seriesdata
    Here seriesdata is contained in the column of df
    called 'column' (string)  """
    return pd.DataFrame({'ds': df.index, 'y': df[column]}, columns=['ds', 'y'])



def fitandforecast(df, col, mode='multiplicative', periods=18, freq='MS',fourier=10,
                  season_prior=10.0, interval_width=0.8):
    """
    Accepts:
        df   - dataframe indexed by datetime (pd.datetime format)
        col  - name of column in df containing the time series data
    Outputs:
        ts   - a time series object
        forecast - dataframe containing the forecast as well as the fit to historical data
    Optional inputs:
        mode - 'multiplicative' (default) or 'additive'
        freq - 'M'
        fourier - fourier order of yearly seasonality
        periods - number of periods to forecast
        seasonality_prior_scale - ...
    """
    ts = Prophet(seasonality_mode=mode, yearly_seasonality=fourier,
                seasonality_prior_scale=season_prior, interval_width=interval_width)
    # interval_width ~ uncertainty interval
    # ts = Prophet(seasonality_mode=mode)
    # m.add_seasonality(
    # name='weekly', period=, fourier_order=fourier, prior_scale=season_prior)
    ts.fit(df_for_forecast(df, col))
    future = ts.make_future_dataframe(periods=periods, freq=freq)
    forecast = ts.predict(future)
    return ts, forecast

def seasoncompare(seriess, names=None):
    """Plot the yearly seasonalities of a list of ts objects on a common axis"""
    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot(111)
    for i in range(len(seriess)):
        plot_yearly(seriess[i], ax = plt.gca(), yearly_start=0)

    clr = ['b', 'g', 'r', 'c', 'm', 'k', 'y', 'k', 'k', 'k', 'k', 'k']
    for i in range(len(seriess)):
        ax.get_lines()[i].set_color(clr[i])
        if names == None:
            ax.get_lines()[i].set_label(str(i+1))
        else:
            ax.get_lines()[i].set_label(names[i])

    plt.legend(bbox_to_anchor=(1.04,1), loc="upper left")
    ## plt.legend([str[k] for k in range(len(seriess))]) #, bbox_to_anchor=(1.04,1), loc="upper left")


#def modelcompare()
