import pandas as pd
from forexconnect import ForexConnect
import datetime
import os
from dotenv import load_dotenv
import pathlib

# Load environment variables from .env file
load_dotenv()

def session_status_changed(session, status):
    print(f"Trading session status: {status}")

class ForexConnector:
    def __init__(self, username=None, password=None, url=None, connection_type="Demo"):

        self.username = username or os.environ.get('FOREX_USERNAME')
        self.password = password or os.environ.get('FOREX_PASSWORD')
        self.url = url or os.environ.get('FOREX_URL')
        self.connection_type = connection_type
        self.fx = None
    
    def connect(self):
        
        self.fx = ForexConnect()
        self.fx.login(
            self.username, 
            self.password, 
            self.url,
            self.connection_type, 
            session_status_callback=session_status_changed
        )
        return self.fx
    
    def disconnect(self):

        if self.fx:
            try:
                self.fx.logout()
                print("Successfully logged out")
            except Exception as e:
                print(f"Exception during logout: {str(e)}")
    
    def __enter__(self):
        return self.connect()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        
    def get_data_and_save(self, ticker, timeframe, days_back=45, save_path=None):

        if not self.fx:
            raise ValueError("Not connected to ForexConnect API")
            
        date_to = datetime.datetime.today()
        date_from = date_to - datetime.timedelta(days=days_back)
        
        print(f"Fetching {ticker} {timeframe} data from {date_from.strftime('%Y-%m-%d')} to {date_to.strftime('%Y-%m-%d')}")
        
        history = self.fx.get_history(ticker, timeframe, date_from=date_from, date_to=date_to)
        df = pd.DataFrame(history)
        
        # Create default save path if none provided
        if save_path is None:
            # Create data directory if it doesn't exist
            data_dir = pathlib.Path("FX")
            data_dir.mkdir(exist_ok=True)
            
            # Create formatted filename with ticker, timeframe and date range
            ticker_formatted = ticker.replace('/', '')
            filename = f"{ticker_formatted}_{timeframe}_{date_from.strftime('%Y%m%d')}_to_{date_to.strftime('%Y%m%d')}.csv"
            save_path = data_dir / filename
        
        # Save to CSV if dataframe is not empty
        if not df.empty:
            df.to_csv(save_path)
            abs_path = os.path.abspath(save_path)
            print(f"Data saved to {save_path}")
            print(f"Absolute path: {abs_path}")
            print(f"In Docker container, this maps to your host at: ./app/FX/{os.path.basename(save_path)}")
            return df
        else:
            print(f"No data retrieved for {ticker} {timeframe}")
            return None


def main():

    pathlib.Path("FX").mkdir(exist_ok=True)
    
    ticker = 'USD/JPY'
    timeframes = ['m1','H1']
    days_back = 45
    
    connector = ForexConnector()
    
    try:
        with connector as fx:

            for tf in timeframes:
                data = connector.get_data_and_save(ticker, tf, days_back)
                if data is not None:
                    print(f"Retrieved {len(data)} rows for {ticker} {tf}")
                
    except Exception as e:
        print(f"Exception: {str(e)}")


if __name__ == "__main__":
    main()