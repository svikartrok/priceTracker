FROM python:3.12.3-alpine3.19

WORKDIR /docker/priceTracker

ADD tracker.py /docker/priceTracker/tracker.py

ADD requirements.txt /docker/priceTracker/requirements.txt

RUN pip install -r requirements.txt


ENTRYPOINT ["python", "tracker.py"]