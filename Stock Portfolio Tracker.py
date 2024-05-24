import requests
import pandas as pd
from tabulate import tabulate

# Alpha Vantage API setup
api_key = 'YFUC1ZV5T7HR9VWM'  # Replace with your actual API key
base_url = 'https://www.alphavantage.co/query'


# Function to get real-time stock data
def get_stock_data(symbol):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',
        'apikey': api_key
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if "Time Series (1min)" in data:
        time_series = data["Time Series (1min)"]
        latest_timestamp = sorted(time_series.keys(), reverse=True)[0]
        return time_series[latest_timestamp]
    else:
        return None


# Function to validate stock symbol
def is_valid_symbol(symbol):
    params = {
        'function': 'SYMBOL_SEARCH',
        'keywords': symbol,
        'apikey': api_key
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if "bestMatches" in data:
        for match in data["bestMatches"]:
            if match["1. symbol"].upper() == symbol.upper():
                return True
    return False


# Function to print a list of common stock symbols
def print_common_symbols():
    common_symbols = {
        "AAPL": "Apple Inc.",
        "MSFT": "Microsoft Corporation",
        "GOOGL": "Alphabet Inc. (Google)",
        "AMZN": "Amazon.com Inc.",
        "META": "Meta Platforms, Inc. (Facebook)",
        "JPM": "JPMorgan Chase & Co.",
        "BAC": "Bank of America Corporation",
        "GS": "Goldman Sachs Group Inc.",
        "WFC": "Wells Fargo & Company",
        "MS": "Morgan Stanley",
        "KO": "The Coca-Cola Company",
        "PEP": "PepsiCo, Inc.",
        "PG": "Procter & Gamble Co.",
        "JNJ": "Johnson & Johnson",
        "DIS": "The Walt Disney Company",
        "PFE": "Pfizer Inc.",
        "MRK": "Merck & Co., Inc.",
        "ABT": "Abbott Laboratories",
        "AMGN": "Amgen Inc.",
        "MRNA": "Moderna, Inc.",
        "BA": "Boeing Company",
        "CAT": "Caterpillar Inc.",
        "GE": "General Electric Company",
        "MMM": "3M Company",
        "HON": "Honeywell International Inc."
    }
    print("\nAvailable Stock Symbols:")
    for symbol, name in common_symbols.items():
        print(f"{symbol}: {name}")


# Portfolio class to manage stocks
class Portfolio:
    def __init__(self):
        self.stocks = {}

    def add_stock(self, symbol, shares):
        if symbol in self.stocks:
            self.stocks[symbol]['shares'] += shares
        else:
            if is_valid_symbol(symbol):
                stock_data = get_stock_data(symbol)
                if stock_data:
                    self.stocks[symbol] = {
                        'shares': shares,
                        'data': stock_data
                    }
                else:
                    print(f"Failed to retrieve data for {symbol}.")
            else:
                print(f"Invalid stock symbol: {symbol}")

    def remove_stock(self, symbol):
        if symbol in self.stocks:
            del self.stocks[symbol]
        else:
            print(f"Stock {symbol} not found in portfolio.")

    def update_stock_data(self):
        for symbol in self.stocks:
            self.stocks[symbol]['data'] = get_stock_data(symbol)

    def display_portfolio(self):
        self.update_stock_data()
        data = []
        for symbol, info in self.stocks.items():
            price = float(info['data']['1. open']) if info['data'] else None
            value = price * info['shares'] if price else None
            data.append({'Symbol': symbol, 'Shares': info['shares'], 'Price': price, 'Value': value})

        df = pd.DataFrame(data)
        print(tabulate(df, headers='keys', tablefmt='grid'))


# Main function to interact with the portfolio
def main():
    portfolio = Portfolio()

    while True:
        print("\nOptions: add, remove, view, list, exit")
        choice = input("Choose an option: ").strip().lower()

        if choice == 'add':
            print_common_symbols()
            symbol = input("Enter stock symbol: ").strip().upper()
            try:
                shares = int(input("Enter number of shares: "))
                portfolio.add_stock(symbol, shares)
            except ValueError:
                print("Invalid number of shares. Please enter an integer.")
        elif choice == 'remove':
            symbol = input("Enter stock symbol: ").strip().upper()
            portfolio.remove_stock(symbol)
        elif choice == 'view':
            portfolio.display_portfolio()
        elif choice == 'list':
            print_common_symbols()
        elif choice == 'exit':
            break
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()

