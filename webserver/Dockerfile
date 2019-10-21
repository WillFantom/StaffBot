FROM python:3.8-alpine

ENV API_HOST https://api.staffbot.net.scc.lancs.ac.uk
ENV API_VERSION 1
ENV ERROR_IMG https://pbs.twimg.com/profile_images/796467399038009344/q7LYPK8U_400x400.jpg
ENV REFRESH_MS 7000

RUN pip install \ 
    requests \
    flask

COPY ./src/ /app

EXPOSE 80

ENTRYPOINT [ "python", "/app/webserver.py" ]