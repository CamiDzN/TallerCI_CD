# app/main.py
from fastapi import FastAPI, Response
from pydantic import BaseModel, Field
import joblib
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Cargar modelo
model = joblib.load('app/model.pkl')

# Métricas Prometheus
PREDICTIONS = Counter(
    'inference_requests_total',
    'Total de peticiones de inferencia'
)
LATENCIES = Histogram(
    'inference_request_latency_seconds',
    'Latencia de las peticiones de inferencia (segundos)',
    # Buckets en segundos: ajusta según tu caso de uso
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5]
)

app = FastAPI()

class RequestData(BaseModel):
    sepal_length: float = Field(..., alias='sepal_length')
    sepal_width: float = Field(..., alias='sepal_width')
    petal_length: float = Field(..., alias='petal_length')
    petal_width: float = Field(..., alias='petal_width')

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(payload: RequestData):
    PREDICTIONS.inc()
    data = payload.dict(by_alias=True)
    features = [
        data['sepal_length'],
        data['sepal_width'],
        data['petal_length'],
        data['petal_width']
    ]
    with LATENCIES.time():
        result = model.predict([features])[0]
    return {"prediction": int(result)}

@app.get("/metrics")
def metrics():
    # Endpoint para Prometheus
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)