import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

class VWAPStrategy:
    def __init__(self, symbol='AAPL', order_size=10000):
        self.symbol = symbol
        self.order_size = order_size
        self.data = None
        self.executions = []

    def fetch_data(self):
        self.data = yf.download(self.symbol, period="1d", interval="1m")
        self.data.dropna(inplace=True)

    def execute(self):
        df = self.data.copy()
        total_volume = df['Volume'].sum()
        df['vwap_ratio'] = df['Volume'] / total_volume
        df['target_shares'] = df['vwap_ratio'] * self.order_size
        df['executed_price'] = df['Close']
        self.executions = df[['target_shares', 'executed_price']]
        return self.executions

    def performance_metrics(self):
        df = self.executions.copy()
        df['executed_value'] = df['target_shares'] * df['executed_price']
        total_cost = df['executed_value'].sum()
        avg_price = total_cost / self.order_size
        arrival_price = self.data.iloc[0]['Open']
        implementation_shortfall = avg_price - arrival_price
        return {
            'Average Execution Price': avg_price,
            'Arrival Price': arrival_price,
            'Implementation Shortfall': implementation_shortfall
        }

    def plot_execution(self):
        self.data['VWAP'] = (self.data['Close'] * self.data['Volume']).cumsum() / self.data['Volume'].cumsum()
        plt.figure(figsize=(12,6))
        plt.plot(self.data['Close'], label='Price')
        plt.plot(self.data['VWAP'], label='VWAP', linestyle='--')
        plt.title(f'{self.symbol} Price vs VWAP')
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    strategy = VWAPStrategy(symbol='AAPL', order_size=10000)
    strategy.fetch_data()
    strategy.execute()
    metrics = strategy.performance_metrics()
    print("Performance Metrics:", metrics)
    strategy.plot_execution()
