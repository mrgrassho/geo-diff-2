FROM python:3.8-slim-buster

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

COPY . .

CMD python admin_worker.py
