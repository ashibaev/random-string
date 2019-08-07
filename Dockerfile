FROM python:3.7.4-alpine

RUN pip3.7 install aiohttp
ENV PYTHONPATH "$PYTHONPATH:/app:"

COPY prepare-template.py prepare-template.py
COPY app /app
RUN python3 prepare-template.py

ARG PORT
ENV PORT $PORT
EXPOSE $PORT

ENTRYPOINT [ "python3.7", "/app" ]