import yfinance as yf
from time import time


def fetch_stock_data(ticker, period='1mo'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


# Find average price in data
def calculate_and_display_average_price(data):
    data_prices = (data['Close'].iloc[i] for i in range(len(data['Close'])))  # Fetch all prices
    data_sum_prices = sum(data_prices)  # Find sum of prices
    print(f'Средняя цена акций за данный период: {data_sum_prices / len(data["Close"])}')  # Print out average sum


# Count divination of price and notify, if threshold is more than divination
def notify_if_strong_fluctuations(data, threshold = 5):
    '''
    Function analyzes closing prices dataframe by mathematical statistic's instruments and notify if price fluctuation was more than current threshold.
    First, aligns the prices in the frame. Next, calculates the mathematical average.
    Then calculates dispersion and price percentage fluctuation.
    :param data: The dataframe of closing prices
    :param threshold: Percentage of price fluctuation
    '''

    # Fetch necessary information
    data_prices = list(data['Close'].iloc)
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
    data.to_csv(encoding='utf-8', path_or_buf=file)
    print(f'Data successfully exported to {file}')
