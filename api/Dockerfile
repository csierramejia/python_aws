FROM python:3.6

WORKDIR /app

ADD . /app

COPY app /app

RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install -U spacy && python3 -m spacy download es
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('maxent_ne_chunker'); nltk.download('words')"

ENV PYTHONPATH /app/

ENV FLASK_DEBUG 1
ENV FLASK_APP app/app.py

EXPOSE 5000
CMD flask run --host=0.0.0.0