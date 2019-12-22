FROM revolutionsystems/python:3.6.3-wee-optimized-lto

COPY . /auction_bid_tracker

WORKDIR /auction_bid_tracker
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python manage.py migrate

CMD gunicorn --workers=4 -b 0.0.0.0:8000 auction_bid_tracker.wsgi:application --access-logfile -