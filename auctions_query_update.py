import treasury_gov_pandas

url = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/auctions_query'

treasury_gov_pandas.load_records(url, lookback=10, update=True)