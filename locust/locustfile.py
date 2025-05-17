from locust import HttpUser, task, between

class ApiUser(HttpUser):
    """
    Usuario virtual que simula peticiones a la API de FastAPI.
    """
    # Tiempo de espera aleatorio entre tareas para simular usuarios reales
    wait_time = between(1, 3)

    @task(5)
    def predict(self):
        # Cuerpo de la petición con los mismos campos que RequestData en FastAPI
        payload = {
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }
        # La URL base se configura en la UI de Locust (host)
        # Aquí usamos ruta relativa al host configurado
        self.client.post("/predict", json=payload)