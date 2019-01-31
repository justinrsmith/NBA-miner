FROM python:3

WORKDIR /home/justin/nba_warehouse

COPY requirements.txt ./
RUN pip install -r requirements.txt
