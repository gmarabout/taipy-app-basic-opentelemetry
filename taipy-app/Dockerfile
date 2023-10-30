FROM  python:3.11

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Instrument dependencies
RUN opentelemetry-bootstrap -a install

COPY . . 

EXPOSE 5000

CMD [ "opentelemetry-instrument", "python3", "main.py"]