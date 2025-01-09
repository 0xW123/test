import requests
import json
from datetime import datetime, timedelta

# Function to fetch price data from CoinGecko API
def fetch_price_data(trading_pair, days=1):
    """
    Fetch historical price data for a given trading pair from CoinGecko.
    
    :param trading_pair: str, the trading pair (e.g., 'btc-usd')
    :param days: int, number of days of history to fetch
    :return: dict, containing price data
    """
    url = f"https://api.coingecko.com/api/v3/coins/{trading_pair.split('-')[0]}/market_chart?vs_currency={trading_pair.split('-')[1]}&days={days}"
    response = requests.get(url)
    data = response.json()
    return data['prices']

def calculate_arbitrage(prices, exchanges):
    """
    Calculate arbitrage opportunities by comparing prices across exchanges.
    
    :param prices: dict, where keys are exchange names and values are price lists
    :param exchanges: list, names of exchanges
    :return: list, of arbitrage opportunities with details
    """
    arbitrage_opportunities = []
    for timestamp, price_data in prices.items():
        price_list = [price_data[exchange] for exchange in exchanges if exchange in price_data]
        if len(price_list) > 1:
            min_price = min(price_list)
            max_price = max(price_list)
            if (max_price - min_price) / min_price > 0.01:  # Arbitrary threshold of 1% difference
                arbitrage_opportunities.append({
                    "timestamp": timestamp,
                    "lowest_price": {"exchange": exchanges[price_list.index(min_price)], "price": min_price},
                    "highest_price": {"exchange": exchanges[price_list.index(max_price)], "price": max_price},
                    "percentage_diff": ((max_price - min_price) / min_price) * 100
                })
    return arbitrage_opportunities

def main():
    # Define trading pairs and exchanges
    trading_pairs = ["btc-usd", "eth-usd", "bnb-usd"]
    exchanges = ["binance", "coinbase", "kraken"]  # Note: CoinGecko does not provide exchange-specific data directly; this is simulated

    all_prices = {}
    for pair in trading_pairs:
        pair_prices = fetch_price_data(pair)
        for i, (timestamp, price) in enumerate(pair_prices):
            timestamp = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
            if timestamp not in all_prices:
                all_prices[timestamp] = {}
            # Here we simulate exchange data; in real scenarios, you'd fetch from each exchange API
            all_prices[timestamp][pair] = {ex: price + (exchanges.index(ex) * 10 - 15) for ex in exchanges}
    
    # Detect arbitrage opportunities
    arbitrage_data = []
    for timestamp, price_data in all_prices.items():
        for pair in trading_pairs:
            if pair in price_data:
                opportunities = calculate_arbitrage({timestamp: price_data[pair]}, exchanges)
                arbitrage_data.extend(opportunities)

    # Output to JSON
    with open('arbitrage_opportunities.json', 'w') as f:
        json.dump(arbitrage_data, f, indent=4)

if __name__ == "__main__":
    main()