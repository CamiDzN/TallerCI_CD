# 📘 Taller CI/CD y GitOps con MLOps en Kubernetes

## 🎯 Descripción del Proyecto
Este proyecto implementa un flujo de **despliegue continuo (CI/CD)** con enfoque **GitOps** para una API de inferencia desarrollada en FastAPI, desplegada en un clúster de **Kubernetes (MicroK8s)**. El sistema incluye **monitoreo con Prometheus y Grafana**, pruebas de carga con Locust y automatización del despliegue con **Argo CD**. Todo el flujo está integrado con GitHub Actions para construir imágenes Docker y actualizar automáticamente el entorno productivo.
## 🧱 Componentes Principales

| Componente         | Función                                                    |
|--------------------|------------------------------------------------------------|
| **FastAPI**        | API de inferencia con modelo ML (Random Forest)            |
| **Locust**         | Pruebas de carga sobre el endpoint `/predict`              |
| **Prometheus**     | Recolección de métricas de la API                          |
| **Grafana**        | Visualización de métricas desde Prometheus                 |
| **Argo CD**        | Despliegue automático desde GitHub (GitOps)                |
| **DockerHub**      | Repositorio de imágenes para API y Locust                  |
| **GitHub Actions** | Entrenamiento del modelo, construcción y push de imágenes  |

---
## 📁 Estructura del Proyecto
```
TallerCI_CD/
├── API/
│ ├── app/
│ │ └── main.py
│ ├── train_model.py
│ ├── Dockerfile
│ └── requirements.txt
├── locust/
│ └── locustfile.py
├── Dockerfile
├── manifests/
│ ├── fastapi-deployment.yaml
│ ├── fastapi-service.yaml
│ ├── locust-k8s.yaml
│ ├── prometheus-configmap.yaml
│ ├── prometheus-deployment.yaml
│ ├── prometheus-service.yaml
│ ├── grafana-datasources.yaml
│ ├── grafana-deployment.yaml
│ ├── grafana-service.yaml
│ ├── namespace-observability.yaml
│ └── kustomization.yaml
├── argo-cd/
│ ├── app.yaml
│ └── install.yaml
└── .github/
└── workflows/
└── ci-cd.yml
```
---

## 🚀 Despliegue Paso a Paso

### 1. Habilitar complementos en MicroK8s

```bash
microk8s enable dns registry ingress
```
### 2. Instalar Argo CD desde archivo local

En lugar de instalar desde la URL remota, este proyecto incluye el manifiesto completo de instalación de Argo CD en la carpeta argo-cd/install.yaml. Para instalarlo:

```bash
microk8s kubectl create namespace argocd
microk8s kubectl apply -n argocd -f argo-cd/install.yaml
```
El manifiesto fue descargado desde:
```bash
https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```
### 3. Obtener contraseña de acceso

```bash
microk8s kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d && echo
```

### 4 . Obtener contraseña de acceso

```bash
microk8s kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d && echo
```
### 4 . Obtener contraseña de acceso

```bash
microk8s kubectl apply -f argo-cd/app.yaml -n argocd
```
## Servicios desplegados (puertos locales)

| Servicio   | URL local                                                  | Puerto  |
| ---------- | ---------------------------------------------------------- | ------- |
| FastAPI    | [http://localhost:30080/docs](http://localhost:30080/docs) | `30080` |
| Prometheus | [http://localhost:30090](http://localhost:30090)           | `30090` |
| Grafana    | [http://localhost:30030](http://localhost:30030)           | `30030` |
| Locust UI  | [http://localhost:30009](http://localhost:30009)           | `30009` |
| Argo CD    | [http://localhost:8080](http://localhost:8080)             | `8080`  |

## 📊 Observabilidad

**Prometheus** recolecta métricas desde el endpoint `/metrics` expuesto por FastAPI.

**Grafana** visualiza métricas clave del modelo, tales como:

- `inference_requests_total` – Total de solicitudes de inferencia recibidas.
- `inference_request_latency_seconds` – Histograma de latencia de las inferencias en segundos.

Estas métricas están habilitadas gracias a la librería `prometheus_client` y están configuradas en Kubernetes mediante el archivo:

```yaml
manifests/grafana-datasources.yaml
