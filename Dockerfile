FROM python:3.7.4-alpine

COPY requirements.txt /requirements.txt
RUN pip3.7 install -r requirements.txt
ENV PYTHONPATH "$PYTHONPATH:/app:"

EXPOSE 8080
RUN mkdir -p /var/log/app

COPY app /app
COPY config /config

ENTRYPOINT [ "python3.7", "/app/main.py" ]