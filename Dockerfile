# Copyright 2023 jwalkiew
# Author: jwalkiew

FROM python:3.9-slim

WORKDIR /opt/kwscanner

RUN apt-get -y update
RUN apt-get install -y wget && apt-get install -y curl && apt-get install -yqq unzip && apt-get install -y gnupg

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update && apt-get install -y google-chrome-stable

RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d .

RUN pip install selenium
RUN pip install selenium-wire

COPY kwscanner.py ./
