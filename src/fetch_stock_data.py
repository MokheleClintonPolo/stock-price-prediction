"""
Stock Data Fetcher
This script fetches historical stock data using yfinance and saves it to CSV
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

def fetch_stock_data(ticker, period="1y", interval="1d"):
    """
    Fetch stock data for a given ticker
    
    Parameters:
    - ticker (str): Stock symbol (e.g., 'AAPL', 'MSFT', 'GOOGL')
    - period (str): Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max')
    - interval (str): Data interval ('1m', '5m', '15m', '1h', '1d', '1wk', '1mo')
    
    Returns:
    - DataFrame: Stock data with columns [Open, High, Low, Close, Volume]
    """
    print(f"Fetching data for {ticker}...")
    
    try:
        # Create ticker object
        stock = yf.Ticker(ticker)
        
        # Fetch historical data
        data = stock.history(period=period, interval=interval)
        
        if data.empty:
            print(f"No data found for {ticker}")
            return None
        
        print(f"Successfully fetched {len(data)} rows of data")
        print(f"Date range: {data.index[0]} to {data.index[-1]}")
        
        return data
    
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def save_data(data, ticker, folder="data"):
    """
    Save stock data to CSV file
    
    Parameters:
    - data (DataFrame): Stock data to save
    - ticker (str): Stock symbol
    - folder (str): Folder to save the data
    """
    if data is None or data.empty:
        print("No data to save")
        return
    
    # Create data folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"{folder}/{ticker}_{timestamp}.csv"
    
    # Save to CSV
    data.to_csv(filename)
    print(f"Data saved to: {filename}")
    print(f"File size: {os.path.getsize(filename) / 1024:.2f} KB")


def get_stock_info(ticker):
    """
    Get additional information about the stock
    
    Parameters:
    - ticker (str): Stock symbol
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        print(f"\n--- Stock Information for {ticker} ---")
        print(f"Company: {info.get('longName', 'N/A')}")
        print(f"Sector: {info.get('sector', 'N/A')}")
        print(f"Industry: {info.get('industry', 'N/A')}")
        print(f"Market Cap: ${info.get('marketCap', 0):,}")
        print(f"Currency: {info.get('currency', 'N/A')}")
        
    except Exception as e:
        print(f"Could not fetch stock info: {e}")


def main():
    """
    Main function to demonstrate usage
    """
    print("=" * 50)
    print("Stock Data Fetcher")
    print("=" * 50)
    
    # Example: Fetch Apple stock data
    ticker = "JPM"  # You can change this to any stock symbol
    
    # Get stock information
    get_stock_info(ticker)
    
    # Fetch 1 year of daily data
    data = fetch_stock_data(ticker, period="1y", interval="1d")
    
    if data is not None:
        # Display first few rows
        print("\nFirst 5 rows of data:")
        print(data.head())
        
        # Display basic statistics with explanations
        print("\nBasic Statistics:")
        stats = data['Close'].describe()
        
        print(f"\ncount: {stats['count']:.6f}")
        print("What it means: The number of data points (trading days) in your dataset.")
        
        print(f"\nmean: {stats['mean']:.6f}")
        print(f"What it means: The average closing price across all {int(stats['count'])} days.")
        
        print(f"\nstd: {stats['std']:.6f} (Standard Deviation)")
        print("What it means: How much the stock price varies or spreads out from the average.")
        
        print(f"\nmin: {stats['min']:.6f}")
        print("What it means: The lowest closing price in the dataset.")
        
        print(f"\n25%: {stats['25%']:.6f} (First Quartile)")
        print(f"What it means: 25% of the days, the stock closed at or below ${stats['25%']:.2f}.")
        
        print(f"\n50%: {stats['50%']:.6f} (Median)")
        print("What it means: The middle value. Half the days were above this price, half were below.")
        
        print(f"\n75%: {stats['75%']:.6f} (Third Quartile)")
        print(f"What it means: 75% of the days, the stock closed at or below ${stats['75%']:.2f}.")
        
        print(f"\nmax: {stats['max']:.6f}")
        print("What it means: The highest closing price in the dataset.")
        
        # Summary story
        price_range = stats['max'] - stats['min']
        percent_increase = (price_range / stats['min']) * 100
        iqr_range = stats['75%'] - stats['25%']
        volatility_percent = (stats['std'] / stats['mean']) * 100
        
        print("\n" + "=" * 60)
        print("Putting It All Together - The Story")
        print("=" * 60)
        print("These stats tell us:")
        print(f"1. {ticker} averaged ${stats['mean']:.0f} over the year")
        print(f"2. Prices ranged from ${stats['min']:.0f} to ${stats['max']:.0f} - that's a ${price_range:.0f} spread (about {percent_increase:.0f}% increase from low to high!)")
        print(f"3. Most days (50% of them) the stock was between ${stats['25%']:.0f} and ${stats['75%']:.0f} (the 25%-75% range)")
        print(f"4. Standard deviation of ${stats['std']:.0f} means daily prices typically varied by about {volatility_percent:.0f}% from average")
        
        # Save to CSV
        save_data(data, ticker)
        
        print("\n✅ Data fetch complete!")
    else:
        print("\n❌ Failed to fetch data")


if __name__ == "__main__":
    main()