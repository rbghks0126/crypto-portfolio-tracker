# crypto-portfolio-tracker

This is a Crypto market / portfolio tracker that I built to aid my personal investment journey in cryptocurrencies.

## Features
By clicking the 'UPDATE' button, various real-time metrics for the 70 tokens that I am interested in are fetched and visualized.
These include:
- price, market cap, market cap rank, all time high price, no. of days since ath, percentage change from ath, recent 24h low, percentage change from recent 24h low, etc.
The point is to identify easily coins that have shot up or coins that still seem to be undervalued. It is also easy to see which sectors/categories I am over/underexposed to. 

On a separate sheet are some basic visualizations of my portfolio and market conditions.

## Examples
Metrics spreadsheet:
![Real-time metrics page](images/metrics.PNG)

Portfolio tracker & market trends:
![Portfolio tracker](images/dashboard.PNG)

There aren't that many features/visualizations implemented but hopefully there are more to come!

## Technologies
- Python
- Google Spreadsheet
- Google Spreadsheet Apps Script
- Coingecko API
- GCP Cloud Function

How?
- Python script fetches real-time, updated market data using Coingecko API
- GCP Cloud Function is used to deploy the Python script as a HTTP request on the Cloud
- Apps Script is used to make the 'button' on the metrics page a trigger for the cloud function
- Google Spreadsheet is then updated and macros are used to produce simple computations & visualizations!

## Requirments
- pandas
- numpy
- pycoingecko
- datetime
- gspread
- oauth2client


