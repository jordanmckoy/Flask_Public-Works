# syntax=docker/dockerfile:1

FROM python
COPY . .
RUN apt-get update
RUN pip3 install -r requirements.txt

RUN python3 run.py