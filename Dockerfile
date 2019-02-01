FROM python:3

WORKDIR /nba_warehouse

COPY . /nba_warehouse

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install .
