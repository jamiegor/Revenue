import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation, performance_metrics
from fbprophet.plot import plot_cross_validation_metric, plot_yearly, plot_weekly, plot_forecast_component
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

def seasoncompare(seriess, period='year', names=None):
    """Plot the yearly seasonalities of a list of ts objects on a common axis"""
    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot(111)
    for i in range(len(seriess)):
        if period=='week':
            plot_weekly(seriess[i], ax = plt.gca(), weekly_start=0)
        else:
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


def brand_forecaster(df, 
                     save_data=False, filename='revenueforecast', 
                     mode='multiplicative', periods=18, freq='MS',fourier=10,
                      season_prior=10.0, interval_width=0.9):
    """ Construct forecasts for all the brands contained in df, as well as for their sum
    
    INPUT: 
    df -- dataframe indexed by datetime (daily), with brand revenues as columns
           (note: will create extra col for total if it doesn't already exist)
    save_data -- True or False, whether to save results to file. 
                 Outputs uncertainty for totalrev but only predicted values for individual brands       
    filename -- string
    
    **kwargs for 'fitandforecast' function
    
    
    OUTPUT:
    names     -- list of brand names
    series    -- dictionary, with brandnames as keys. Time series output of prophet model
    forecasts -- dictionary, with brandnames as keys. Dataframe containing forecast output from Prophet model
                 (eg. ds, trend, yhat_lower, yearly, yhat, etc etc)    """
    
    series = {}
    forecasts = {}
    names = []
    
    if 'totalrev' not in df.columns:
        df['totalrev'] = df.sum(axis='columns')
    
    for brand in df.columns:
        series[brand], forecasts[brand] = fitandforecast(df, brand, mode=mode, periods=periods, freq=freq, fourier=fourier,
                  season_prior=season_prior, interval_width=interval_width)
        names.append(brand)
    
    selectcols = ['ds', 'yhat', 'yhat_upper', 'yhat_lower']
    renamecols = ['date', 'rev_forecast', 'upper_estimate', 'lower_estimate'] 

    output_total = forecasts['totalrev'][selectcols].rename(columns=dict(zip(selectcols, renamecols)))
    output_by_brand = pd.concat([forecasts[brand]['yhat'].rename(brand) for brand in names], axis=1).set_index(
    forecasts[names[0]]['ds'].values)
    
    if save_data==True:
        output_total.to_csv('output/'+filename+'_tot'+'.csv', index=False)
        output_by_brand.to_csv('output/'+filename+'_byBrand'+'.csv')
    
    return names, series, forecasts



#def modelcompare()
