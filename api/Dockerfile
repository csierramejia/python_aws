FROM python:3.6

WORKDIR /app

ADD . /app

RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV PYTHONPATH /app/

ENV FLASK_DEBUG 1
ENV FLASK_APP app/app.py

EXPOSE 5000
CMD flask run --host=0.0.0.0