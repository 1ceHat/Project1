import pandas as pd
import yfinance as yf
from matplotlib import pyplot as plt
from time import time
from pprint import pprint


def fetch_stock_data(ticker, period='1mo', start_period=None, end_period=None):
    stock = yf.Ticker(ticker)
    data = None
    if start_period is not None:
        if end_period is not None:
            data = stock.history(start=start_period, end=end_period)
        else:
            data = stock.history(start=start_period)
    elif period is not None:
        data = stock.history(period=period)
    return data


def add_moving_average(data: pd.DataFrame, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


# Add EMA indicator
def add_exponential_moving_average(data: pd.DataFrame, window_size=5, create_plot=False):
    '''
    Function adding EMA indicator.
    :param data: data to analysis
    :param window_size: periods to analysis
    :param create_plot: default False, if True will make a plot and return it
    :return: DataFrame with EMA indicator if create_plot=False. If create_plot=True will return (DataFrame, PyPlot.show func)
    '''
    data = add_moving_average(data, window_size=window_size)

    sma = data.get(['Close', 'Moving_Average'])

    n = len(sma)
    k = 2/(n+1)
    ema = []

    for i in range(n):
        win = sma.iloc[i]
        ema.append((win['Close']-win['Moving_Average'])*k + win['Moving_Average'])
    data['EMA'] = ema

    if create_plot:
        plt.close()
        close_and_ema = data.get(['Close', 'EMA'])
        dates = close_and_ema.index.to_numpy()
        plt.plot(dates, close_and_ema['Close'].values, label='Close Price')
        plt.plot(dates, close_and_ema['EMA'].values, label='EMA')
        plt.legend()
        return data, plt.show

    return data


# Add RSI indicator
def add_relative_strength_index(data: pd.DataFrame, window_size=5, high_level=80, low_level=20, create_plot=False):
    '''
    Function adding RSI indicator.
    :param data: data to analysis
    :param window_size: period to analysis
    :param high_level: default 80. Level of overbought
    :param low_level: default 20. Level of oversold
    :param create_plot: default False, if True will make a plot and return it
    :return: DataFrame with RSI indicator if create_plot=False. If create_plot=True will return (DataFrame, PyPlot.show func)
    '''
    diff = data.copy()['Close'].diff()

    up, down = diff.copy(), diff.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    up = up.rolling(window=window_size).mean()
    down = down.abs().rolling(window=window_size).mean()

    rsi = 100 - (100 / (1 + up/down))
    data['RSI'] = rsi

    if create_plot:
        plt.close()
        close_and_rsi = data.get(['Close', 'RSI']).copy()
        cutter = len(close_and_rsi) - len(close_and_rsi['RSI'].dropna())
        close_and_rsi = close_and_rsi[cutter:]
        dates = close_and_rsi.index.to_numpy()
        fig = plt.figure()
        ax1 = fig.add_subplot(2,1,1)
        ax1.plot(dates, close_and_rsi['Close'].values, label='Close Price')
        ax2 = fig.add_subplot(2,1,2)
        ax2.plot(dates, close_and_rsi['RSI'].values, label='RSI')
        ax2.axhline(high_level, color='black', linestyle='--', linewidth=0.5)
        ax2.axhline(low_level, color='black', linestyle='--', linewidth=0.5)
        plt.legend()
        return data, plt.show

    return data


# Add MACD indicator
def add_moving_average_convergence_divergence(data: pd.DataFrame, fast_macd=12, slow_macd=26, indicator_macd=9, create_plot=False):
    '''
    Function analysing price and return MACD indicators.
    :param data: data to analysis
    :param fast_macd: period for Fast MACD
    :param slow_macd: period for Slow MACD
    :param indicator_macd: period for Indicator MACD
    :param create_plot: default False, if True will make a plot and return it
    :return: DataFrame with MACD indicator
    '''

    if len(data) < max(fast_macd, slow_macd, indicator_macd):
        print('Недостаточный период для анализа!')
        if create_plot:
            return data, None
        return data

    data_copy = data.copy()
    fast_ema = add_exponential_moving_average(data_copy, window_size=fast_macd)['EMA']
    slow_ema = add_exponential_moving_average(data_copy, window_size=slow_macd)['EMA']
    indicator_ema = (fast_ema-slow_ema).rolling(window=10).mean()
    data['Fast_MACD'] = fast_ema.values
    data['Slow_MACD'] = slow_ema.values
    data['Indic_MACD'] = indicator_ema.values

    if create_plot:
        plt.close()
        close_and_macd = data.get(['Close', 'Fast_MACD', 'Slow_MACD', 'Indic_MACD']).copy()
        cutter = len(close_and_macd) - len(close_and_macd['Indic_MACD'].dropna())
        close_and_macd = close_and_macd[cutter:]

        dates = close_and_macd.index.to_numpy()
        fig = plt.figure()
        ax1 = fig.add_subplot(2,1,1)
        ax1.plot(dates, close_and_macd['Close'].values, label='Close Price')
        ax1.plot(dates, close_and_macd['Fast_MACD'], label='Fast MACD')
        ax1.plot(dates, close_and_macd['Slow_MACD'], label='Slow MACD')
        plt.legend()
        ax2 = fig.add_subplot(2,1,2)
        ax2.plot(dates, close_and_macd['Indic_MACD'].values, label='Indic MACD')
        plt.legend()
        return data, plt.show

    return data


# Find average price in data
def calculate_and_display_average_price(data: pd.DataFrame):
    data_prices = (data['Close'].iloc[i] for i in range(len(data['Close'])))  # Fetch all prices
    data_sum_prices = sum(data_prices)  # Find sum of prices
    print(f'Средняя цена акций за данный период: {data_sum_prices / len(data["Close"])}')  # Print out average sum


# Count divination of price and notify, if threshold is more than divination
def notify_if_strong_fluctuations(data: pd.DataFrame, threshold=5):
    '''
    Function analyzes closing prices dataframe by mathematical statistic's instruments and notify if price fluctuation was more than current threshold.
    First, aligns the prices in the frame. Next, calculates the mathematical average.
    Then calculates dispersion and price percentage fluctuation.
    :param data: The dataframe of closing prices
    :param threshold: Percentage of price fluctuation
    '''

    # Fetch necessary information
    data_prices = list(data['Close'].copy())
    len_data = len(data_prices)
    min_price = round(min(data_prices)) - 1
    max_price = round(max(data_prices)) + 1
    # List to count mathematical expectation of a sample
    average_list = [[(i, i + 2), (2 * i + 2) / 2, 0] for i in range(min_price, max_price, 2)]

    # Counting number of the prices that are in the intervals
    for price in data_prices:
        for interval in average_list:
            if interval[0][0] <= price < interval[0][1]:
                interval[2] += 1

    # Counting mathematical expectation and dispersion
    mat_expectation = 0
    dispersion = 0
    for interval in average_list:
        mat_expectation += interval[1] * interval[2] / len_data
        dispersion += interval[1] ** 2 * interval[2] / len_data
    dispersion = dispersion - mat_expectation ** 2
    dispersion = dispersion * len_data / (len_data - 1)

    # Counting standard divination
    standard_divination = round((dispersion ** 0.5) * 100 / mat_expectation, 3)
    if threshold < standard_divination:
        print(f'Цена колебалась больше заданного процента! Текущее колебание цены за период: {standard_divination}%')
    else:
        print(f'Цена не колебалась выше {threshold}%. Текущее колебание цены за период: {standard_divination}%')


def export_data_to_csv(data, file):
    '''
    Function exporting data into CSV-file
    :param data: The dataframe of closing prices
    :param file: A name for the CSV-file
    '''

    data.to_csv(encoding='utf-8', path_or_buf=file)
    print(f'Data successfully exported to {file}')
