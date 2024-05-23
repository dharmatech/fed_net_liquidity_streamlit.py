#!/usr/bin/bash

. /home/dharmatech/.bashrc # for FRED_API_KEY

. /home/dharmatech/python-environments/env-3.10-streamlit/bin/activate

cd /var/www/dharmatech.dev/data/temp/fed_net_liquidity_streamlit.py

# streamlit run Fed_Net_Liquidity.py

#streamlit run \
#	--browser.serverAddress dharmatech.dev \
#	--browser.serverPort 8501 \
#	--server.sslCertFile /home/dharmatech/fullchain.pem \
#	--server.sslKeyFile /home/dharmatech/privkey.pem \
#	--server.baseUrlPath fed-net-liquidity \
#	Fed_Net_Liquidity.py

streamlit run \
        --browser.serverPort 8501 \
        --server.sslCertFile /home/dharmatech/fullchain.pem \
        --server.sslKeyFile /home/dharmatech/privkey.pem \
	--server.baseUrlPath fed-net-liquidity \
	--server.enableCORS false \
        Fed_Net_Liquidity.py



# streamlit run \
#        --browser.serverPort 8501 \
#        --server.baseUrlPath fed-net-liquidity \
#        Fed_Net_Liquidity.py
