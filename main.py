from matplotlib import pyplot as plt
import data_download as dd
import data_plotting as dplt


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc):»")
    period = input("Введите период для данных (например, '1mo' для одного месяца) или даты в формате ГГГГ-ММ-ДД через пробел (по умолчанию конец - сегодня): ").split(' ')
    # period = '2001-10-30'.split(' ')
    # ticker = 'MSFT'
    if len(period) == 2:
        period = {'start_period': period[0], 'end_period': period[1]}
    elif len(period) == 1:
        if '-' in period[0]:
            period = {'start_period': period[0]}
            # stock_data = dd.fetch_stock_data(ticker, start_period=period[0])
        else:
            period = {'period': period[0] if period[0] != "" else "1mo"}
            # stock_data = dd.fetch_stock_data(ticker, period=period[0])
    else:
        print('Введите корректный период или диапазон дат')
        return None


    # Fetch stock data
    stock_data = dd.fetch_stock_data(ticker, **period)
    period = '--'.join(map(str, period.values()))

    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data)

    # Print out average sum prices
    # dd.calculate_and_display_average_price(stock_data)

    # Print out notify
    # threshold = input('Введите процент колебания цены для проверки (default = 5): ')
    # dd.notify_if_strong_fluctuations(stock_data, int(threshold) if threshold != '' else 5)

    # Asking about exporting data to CSV format
    # if input('Сохранить данные в формате CSV? (yes/no) ') in ('y', 'yes'):
    #     file = input('Введите название файла (можно оставить пустым)')
    #     file = file if file != '' else f'{ticker}_{period}_stock_price_chart.csv'
    #     dd.export_data_to_csv(stock_data, file)

    # Add EMA indicator to DataFrame. Uncomment ema_ind to show plot
    # stock_data, ema_ind = dd.add_exponential_moving_average(stock_data, create_plot=True)
    # ema_ind()

    # Add RSI indicator to DataFrame. Uncomment rsi_ind to show plot
    # stock_data, rsi_ind = dd.add_relative_strength_index(stock_data, create_plot=True)
    # rsi_ind()

    # Add MACD indicator to DataFrame. Uncomment macd_ind to show plot
    # stock_data, macd_ind = dd.add_moving_average_convergence_divergence(stock_data, create_plot=True)
    # macd_ind()

    # Providing a choice of style
    if input("Хотите выбрать стиль оформления графика? ") in ['y', 'ye', 'yes', 'да', 'д']:
        for style in plt.style.available:
            print(f'{f"|{plt.style.available.index(style) + 1}: {style}":30}', end=" ")
            if not ((plt.style.available.index(style) + 1) % 4):
                print("|")
        numbers = input('Выберите из представленных выше стиль и напишите его номер (или несколько через пробел): ').split(' ')
        if len(numbers) == 1 and numbers[0] != '':
            style = plt.style.available[int(numbers[0])-1]
        elif len(numbers) > 1:
            style = [plt.style.available[int(num)-1] for num in numbers]
        else:
            print('Вы что-то напутали в вводе, поэтому сделаем стандартный стиль')
            style = None

        dplt.create_and_save_plot(stock_data, ticker, period, style=style)
    else:
        # Plot the data
        dplt.create_and_save_plot(stock_data, ticker, period)


if __name__ == "__main__":
    main()
