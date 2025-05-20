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
```

## 🚀 Validación del Despliegue con Argo CD

Después de conectar Argo CD con nuestro repositorio de GitHub mediante `kustomization.yaml`, procedimos a validar que la integración de GitOps funcionaba correctamente con los siguientes pasos:

### 🔐 Conexión a la Interfaz de Argo CD

Desde la terminal ejecutamos:

```bash
microk8s kubectl port-forward svc/argocd-server -n argocd 8080:443
```
Esto nos permitió acceder vía navegador a:

```bash
https://localhost:8080
```

### 🧠 Visualización en Argo CD
En la interfaz de Argo CD pudimos verificar:

- El estado de sincronización ✅ Synced.
- La salud del sistema 💚 Healthy.

![image](https://github.com/user-attachments/assets/7cfbb328-4e0a-4b7a-b8a5-2a8796c849f3)

- Que los manifiestos provenientes de GitHub estaban correctamente aplicados.

![image](https://github.com/user-attachments/assets/30dd76be-316b-4c75-97da-c5deea7343f6)

- La sección de History and Rollback mostraba el historial de despliegues con las imágenes actualizadas:

![Imagen de WhatsApp 2025-05-19 a las 20 24 12_0e221ad4](https://github.com/user-attachments/assets/7c5c3623-2c3d-4908-825a-9e97fa22b2fa)

![Imagen de WhatsApp 2025-05-19 a las 20 24 46_ef280265](https://github.com/user-attachments/assets/89520d08-2365-4e2a-adef-5d5f71a7a3a5)


| Revisión | Imagen FastAPI            | Imagen Locust                |
| -------- | ------------------------- | ---------------------------- |
| b23add2  | `camidzn/api:20250518-1`  | `camidzn/locust:20250518-1`  |
| ad255bf  | `camidzn/api:20250519-10` | `camidzn/locust:20250519-10` |

### 🧪 Validación de Pods Desplegados
Verificamos los contenedores corriendo con:

```bash
microk8s kubectl get pods -n loadtest --sort-by=.metadata.creationTimestamp
```

![Imagen de WhatsApp 2025-05-19 a las 20 26 21_4653d84a](https://github.com/user-attachments/assets/54179989-1561-4caf-b3f5-faec8c1fd070)

✅ Esto confirma que la sincronización de Argo CD no solo actualizó las imágenes automáticamente desde GitHub, sino que también recreó los pods necesarios en el clúster de Kubernetes.

