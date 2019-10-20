FROM python:3.8-alpine

ENV API_VERSION 1
ENV DEBUG 0
ENV SECRET_KEY changeme

RUN pip install \ 
    beautifulsoup4 \
    flask

COPY ./src/ /app

EXPOSE 8080

ENTRYPOINT [ "python", "/app/api.py" ]