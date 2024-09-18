def calculate_and_display_average_price(data):
    data_prices = (data['Close'].iloc[i] for i in range(len(data['Close'])))
    data_sum_prices = sum(data_prices)
    print(f'Средняя цена акций за данный период: {data_sum_prices / len(data["Close"])}')