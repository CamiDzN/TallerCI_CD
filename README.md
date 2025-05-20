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


```text
TALLERCI_CD/
├── .github/
│   └── workflows/
│       └── ci-cd.yml            # Definición del pipeline de CI/CD en GitHub Actions
├── API/
│   ├── app/
│   │   ├── main.py              # Código principal de FastAPI
│   │   ├── Dockerfile           # Construye la imagen de la API con el modelo entrenado
│   │   ├── requirements.txt     # Dependencias Python
│   │   └── train_model.py       # Script de entrenamiento y serialización del modelo
├── locust/
│   ├── Dockerfile               # Imagen de Locust con dependencias
│   └── locustfile.py            # Escenarios de carga y definición de tareas
├── argo-cd/
│   ├── app.yaml                 # Application de Argo CD para sincronización GitOps
│   └── install.yaml             # Manifiesto de instalación de Argo CD en el clúster
├── manifests/
│   ├── fastapi-deployment.yaml  # Despliegue de la API en Kubernetes
│   ├── fastapi-service.yaml     # Service para exponer la API
│   ├── locust-k8s.yaml          # Despliegue de Locust en el clúster
│   ├── namespace-observability.yaml  # Namespace para Prometheus y Grafana
│   ├── prometheus-configmap.yaml     # Configuración de scraping de métricas
│   ├── prometheus-deployment.yaml    # Despliegue de Prometheus
│   ├── prometheus-service.yaml       # Service para Prometheus
│   ├── grafana-datasources.yaml      # Datasources configurados en Grafana
│   ├── grafana-deployment.yaml       # Despliegue de Grafana
│   ├── grafana-service.yaml          # Service para Grafana
│   └── kustomization.yaml            # Archivo de Kustomize para parametrización de tags
└── .gitignore                       # Archivos y carpetas ignoradas por Git
```

Cada directorio agrupa componentes específicos: la carpeta `.github` define el pipeline de CI/CD; `API/app` contiene la lógica de entrenamiento y servicio de inferencia; `locust` alberga los tests de carga; `argo-cd` centraliza la configuración GitOps; `manifests` contiene los recursos Kubernetes parametrizados con Kustomize.


---

## 🚀 Despliegue Paso a Paso


### 1. Preparación de Imágenes Docker

Previo al desarrollo del pipeline de CI/CD, se crearon y validaron los Dockerfile y archivos de configuración necesarios para:

* **API**: el `Dockerfile` ubicado en `API/app/` incorpora el modelo entrenado (`train_model.py`) y las dependencias definidas en `requirements.txt` para generar una imagen reproducible de la API.
* **Locust**: el `Dockerfile` en la carpeta `locust/` integra Locust, los escenarios definidos en `locustfile.py` y las librerías necesarias para las pruebas de carga.

Estas imágenes sirven de base para las siguientes etapas del flujo, permitiendo un entrenamiento automático del modelo y la creación de artefactos listos para publicarse en el registro Docker.

### 2. Configuración de Kubernetes y Manifiestos

Para preparar el entorno de orquestación, se procedió con los siguientes pasos:

1. **Instalación y configuración de MicroK8s**:

   * Despliegue de un clúster local usando MicroK8s.
   * Habilitar componentes de MicroK8s.

```bash
microk8s enable dns registry ingress
```


2. **Generación de manifiestos Kubernetes**:

   * Creación de archivos en la carpeta `manifests/` para cada componente:

     * **Deployment** y **Service** de FastAPI.
     * **Deployment** y **Service** de Locust.
     * **Namespace** dedicado para observabilidad.
     * **ConfigMap** de Prometheus para scraping de métricas.
     * **Deployment** y **Service** de Prometheus.
     * **Datasources** y **Deployment** de Grafana.
   * Parametrización de tags con **Kustomize** en `kustomization.yaml`, permitiendo inyectar dinámicamente las versiones generadas.

Estos recursos establecen la base declarativa para el despliegue, asegurando que el clúster pueda sincronizarse automáticamente mediante GitOps.

### 3. Desarrollo del Pipeline CI/CD con Github Actions

El workflow, denominado **CI/CD Pipeline**, está definido con permisos de escritura en el repositorio y se dispara automáticamente al hacer push en la rama `main` sobre las carpetas `API/` o `locust/`, o de forma manual desde la UI de GitHub. Se establecen variables de entorno para apuntar al registro Docker y los repositorios de la API y de los tests de carga. El único job (`build-and-push`) se ejecuta sobre un runner Ubuntu, orquestando desde el checkout del código y la generación de un tag semántico, hasta el entrenamiento del modelo, la construcción y publicación de imágenes, la actualización de manifiestos con Kustomize y el commit de los cambios.

A grandes rasgos, el pipeline sigue estas fases:

* **Inicialización**: definición de nombre, permisos y triggers del workflow.
* **Checkout y Versionado**: obtención del código y cálculo de un tag semántico único.
* **Setup y Entrenamiento**: configuración del entorno Python e invocación del script de entrenamiento.
* **Build & Push Docker**: autenticación en Docker Hub y construcción/publicación de las imágenes de API y Locust.
* **Actualización de Manifiestos**: revisión de la carpeta de manifiestos con Kustomize para apuntar al nuevo tag.
* **Commit Final**: registro automático de los cambios y push al branch principal.

---

### 4. Instalar Argo CD desde archivo local

En lugar de instalar desde la URL remota, este proyecto incluye el manifiesto completo de instalación de Argo CD en la carpeta argo-cd/install.yaml. Para instalarlo:

```bash
microk8s kubectl create namespace argocd
microk8s kubectl apply -n argocd -f argo-cd/install.yaml
```
El manifiesto fue descargado desde:
```bash
https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```
#### Obtener contraseña de acceso

```bash
microk8s kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d && echo
```

#### Configuración de Argo CD

Para establecer la sincronización GitOps, se creó la **Application** de Argo CD descrita en `argo-cd/app.yaml`, incluyendo:

* **apiVersion**: `argoproj.io/v1alpha1` y **kind**: `Application`.
* **metadata**: nombre `taller-mlops-daniel` en el namespace `argocd`.
* **spec.project**: `default` para agrupar la aplicación dentro del proyecto estándar.
* **source**:

  * **repoURL**: `https://github.com/CamiDzN/TallerCI_CD`.
  * **targetRevision**: rama `main`.
  * **path**: `manifests` donde residen los YAML de despliegue.
* **destination**:

  * **server**: `https://kubernetes.default.svc` (API interna del clúster).
  * **namespace**: `loadtest` para aislar los recursos de pruebas de carga.
* **syncPolicy.automated**:

  * `selfHeal: true` para corregir configuraciones que diverjan del repositorio.
  * `prune: true` para eliminar recursos obsoletos.

Con esta configuración, Argo CD vigila continuamente el repositorio, detecta cualquier actualización en los manifiestos y aplica automáticamente los cambios al clúster, cerrando el ciclo de entrega continua.


#### Aplicar tu manifiesto app.yaml

```bash
microk8s kubectl apply -f argo-cd/app.yaml -n argocd
```

### 📈 5. Observabilidad con Grafana

Este proyecto incluye un dashboard de Grafana que se crea automáticamente al desplegar el clúster.

#### 🔧 ¿Cómo se logra?

La configuración se realiza mediante los siguientes manifiestos:

- `grafana-dashboards-configmap.yaml`: contiene el JSON del dashboard (`my-dashboard.json`) con las métricas deseadas.
- `grafana-dashboard-provider.yaml`: indica a Grafana dónde encontrar y cómo cargar los dashboards al iniciar.
- `grafana-deployment.yaml`: se actualizó para incluir estos recursos como volúmenes montados.

Todo esto está referenciado en `kustomization.yaml` para que sea desplegado automáticamente con Argo CD.

#### 📊 Dashboard Automático

Una vez desplegado, el dashboard incluye las siguientes métricas clave:

| Métrica                         | Descripción                                      |
|-------------------------------|--------------------------------------------------|
| `inference_requests_total`     | Número total de inferencias realizadas.         |
| `inference_request_latency_seconds` | Latencia promedio de las inferencias.     |
| `process_virtual_memory_bytes` | Memoria usada por el servicio FastAPI.          |


## 🚀 Validación del funcionamiento de la Integración Continua con Github Actions y Despliegue Continuo con Argo CD

Para garantizar el correcto funcionamiento del flujo de CI, se realizaron las siguientes pruebas, registradas con capturas de la interfaz de GitHub Actions, Docker Hub y GitHub:

### 🔍 1. Trigger Automático al Modificar Requirements

Al realizar un cambio en `API/app/requirements.txt` y hacer push a la rama `main`, el workflow **CI/CD Pipeline** se dispara automáticamente. Esto confirma que los **paths filters** (`API/**` y `locust/**`) están correctamente configurados para iniciar el pipeline solo cuando existen cambios relevantes.
*(imagen: captura de inicio de workflow con trigger automático)*

### ✅ 2. Verificación de Ejecución Exitosa

En la consola de GitHub Actions se comprueba que todas las etapas del job `build-and-push` (Checkout, Versionado, Entrenamiento, Build & Push, Actualización de Manifiestos y Commit) finalizan sin errores, mostrando iconos verdes de éxito.
*(imagen: dashboard de GitHub Actions con jobs completados)*

### 🐳 3. Comprobación de Imágenes en Docker Hub

Accedimos a los repositorios **REPO\_API** y **REPO\_LOCUST** en Docker Hub y validamos la aparición de las nuevas etiquetas con formato `YYYYMMDD-RUN`. Cada imagen contiene el artefacto del modelo entrenado y satisface los requisitos de versionado.
*(imagen: listado de tags en Docker Hub mostrando el nuevo tag)*

### 🔄 4. Confirmación de Actualización en Kustomize

Se revisa el diff en GitHub del commit automático que modificó `manifests/kustomization.yaml`, asegurando que los **image tags** se hayan actualizado correctamente al nuevo `IMAGE_TAG`. Este paso valida que la fase de **Kustomize edit set image** funciona según lo esperado.
*(imagen: diff en GitHub mostrando la actualización de tags en kustomization.yaml)*


Después de conectar Argo CD con nuestro repositorio de GitHub mediante `kustomization.yaml`, procedimos a validar que la integración de GitOps funcionaba correctamente con los siguientes pasos:

### 🔐 5. Conexión a la Interfaz de Argo CD

Desde la terminal ejecutamos:

```bash
microk8s kubectl port-forward svc/argocd-server -n argocd 8080:443
```
Esto nos permitió acceder vía navegador a:

```bash
https://localhost:8080
```

### 🧠 6. Visualización en Argo CD
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

### 🧪 7. Validación de Pods Desplegados
Verificamos los contenedores corriendo con:

```bash
microk8s kubectl get pods -n loadtest --sort-by=.metadata.creationTimestamp
```

![Imagen de WhatsApp 2025-05-19 a las 20 26 21_4653d84a](https://github.com/user-attachments/assets/54179989-1561-4caf-b3f5-faec8c1fd070)

✅ Esto confirma que la sincronización de Argo CD no solo actualizó las imágenes automáticamente desde GitHub, sino que también recreó los pods necesarios en el clúster de Kubernetes.



### 🎯 8. Visualización en Grafana

El dashboard generado luce así:

![image](https://github.com/user-attachments/assets/abc5661f-76da-4438-8285-af46280da50c)


> *Grafana toma automáticamente estas configuraciones desde el `ConfigMap`, sin intervención manual después del despliegue.*

---

Esto garantiza que cada vez que se despliega el stack con Argo CD, el dashboard esté disponible de forma inmediata para monitorear la API de inferencia.
---

## Conclusiones y Lecciones Aprendidas

* **Automatización total** del ciclo CI/CD mejora la velocidad de entrega y reduce errores humanos.
* **GitOps** con Argo CD aporta consistencia y visibilidad al estado de la infraestructura.
* **Observabilidad** es fundamental para diagnosticar problemas de rendimiento y garantizar la disponibilidad.
* La combinación de **MicroK8s**, **Kustomize** y **GitHub Actions** facilita la creación de entornos de desarrollo locales replicables.


