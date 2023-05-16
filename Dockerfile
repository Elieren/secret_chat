FROM python

COPY . /server
WORKDIR /server

EXPOSE 9090

CMD python3 server.py