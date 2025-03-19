# Forex_API

## Overview

This project fetches and saves forex data using the ForexConnect API in different timeframes (M1, H1).

## Prerequisites

- Docker and Docker Compose installed
- ForexConnect API credentials

## Setup

1. Clone the repository:

   ```sh
   git clone [repository_url]
   cd Forex_API
   ```

2. Create an environment file:
   Create a file named `.ENV` in the `app` directory with your ForexConnect credentials:
   ```
   FC_USERNAME=your_username
   FC_PASSWORD=your_password
   FC_URL=your_api_url
   ```

## Running the Application

### Using Docker

1. Build and run the container using Docker Compose:

   ```sh
   docker-compose up --build
   ```

2. The application will:
   - Connect to the ForexConnect API
   - Download USD/JPY data in M1 and H1 timeframes for the past 45 days
   - Save the data as CSV files in the `app/FX` directory

## Project Structure

- `app/Data.py`: Main script containing the `ForexConnector` class for API interaction
- `app/FX`: Directory where CSV data files are saved
- `dockerfile`: Docker configuration for the application
- `docker-compose.yml`: Docker Compose configuration for container orchestration
- `requirements.txt`: List of Python dependencies

## Data Files

The application saves data in CSV format with filenames structured as:

```
[TICKER]_[TIMEFRAME]_[START_DATE]_to_[END_DATE].csv
```

Example: `USDJPY_H1_20250202_to_20250319.csv`

## Notes

- The application is configured to fetch data for the past 45 days by default
- Data is currently configured to fetch USD/JPY pair in M1 (1-minute) and H1 (1-hour) timeframes
- The Docker setup maps the data directory to a volume so files persist between container runs

## Customization

To change the ticker or timeframes, modify the variables in the `main()` function in `app/Data.py`:

```python
ticker = 'USD/JPY'
timeframes = ['m1','H1']
days_back = 45
```

And re-run the docker.
