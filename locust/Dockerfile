FROM locustio/locust:2.16.0

COPY locustfile.py /mnt/locust/locustfile.py
WORKDIR /mnt/locust

EXPOSE 8089 5557 5558

ENTRYPOINT ["locust"]
