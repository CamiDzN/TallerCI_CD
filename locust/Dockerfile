# Usa la imagen oficial de Locust
FROM locustio/locust:2.16.0

# Copia tu script al contenedor
COPY locustfile.py /mnt/locust/locustfile.py

WORKDIR /mnt/locust

# Exponer puertos:
# - 8089: UI/master
# - 5557, 5558: RPC master<->workers
EXPOSE 8089 5557 5558

# Comando por defecto; Argo CD o k8s puede pasar args
ENTRYPOINT ["locust"]