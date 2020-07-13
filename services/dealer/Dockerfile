FROM python:3.8-slim-buster

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

RUN useradd --create-home geouser
WORKDIR /home/geouser
USER geouser

COPY . .

CMD [ "python", "./dealer.py" ]
