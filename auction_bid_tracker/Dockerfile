FROM revolutionsystems/python:3.6.3-wee-optimized-lto

COPY . /auction_bid_tracker

WORKDIR /auction_bid_tracker
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh