FROM python:3.8.6-buster

COPY requirements.txt /requirements.txt
COPY api /app
COPY thermofeeler /thermofeeler
COPY model /model
COPY setup.py /setup.py
COPY MANIFEST.in /MANIFEST.in
COPY tokenizer.pickle /tokenizer.pickle
COPY scripts /scripts
COPY .env /.env

RUN pip install --upgrade pip
RUN pip install -e .

CMD uvicorn app.fast:app --host 0.0.0.0 --port $PORT
