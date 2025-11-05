#!/usr/bin/bash

# . /home/dharmatech/.bashrc # for FRED_API_KEY

. /home/dharmatech/keys    # for FRED_API_KEY

. /home/dharmatech/python-environments/env-3.10-streamlit/bin/activate

export PYTHONPATH=$PYTHONPATH:/home/dharmatech/python-libs/yfinance_download.py

cd /var/www/dharmatech.dev/data/temp/fed_net_liquidity_streamlit.py

streamlit run \
        --server.address 127.0.0.1 \
        --server.port 8501 \
        --server.baseUrlPath fed-net-liquidity \
	--server.enableCORS false \
	--server.enableXsrfProtection false \
        Fed_Net_Liquidity.py
