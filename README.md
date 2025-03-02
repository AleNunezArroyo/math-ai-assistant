# Crea un Asistente de Matemáticas con Gemini 2.0 Flash Thinking, Vertex AI y Gradio

Este repositorio contiene el código para implementar un asistente de matemáticas basado en **Gemini 2.0 Flash Thinking**, utilizando **Vertex AI** y **Gradio**. Si quieres conocer los detalles técnicos y el contexto del proyecto, consulta el artículo publicado en [Medium](https://console.cloud.google.com/).

## Configuración del Proyecto

### 1. Requisitos Previos
Antes de comenzar, asegúrate de contar con lo siguiente:

- Una cuenta en [Google Cloud](https://console.cloud.google.com/)
- Tener habilitada la API de Vertex AI en tu proyecto de Google Cloud
- Python 3.11 o superior
- Conda o un entorno virtual de Python

### 2. Clonar el Repositorio
```bash
git clone https://github.com/AleNunezArroyo/math-ai-assistant.git
cd math-ai-assistant
```

### 3. Creación y Activación del Entorno Virtual
Usando Conda:
```bash
conda create -n math-ai -y
conda activate math-ai
```

O con venv:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 4. Instalación de Dependencias (No necesario si usas el enviroment de Conda)
```bash
pip install -r requirements.txt
```

### 5. Configuración de Credenciales de Google Cloud
Para que la aplicación pueda interactuar con Vertex AI, necesitas configurar las credenciales de Google Cloud.

1. Crea un nuevo proyecto en Google Cloud y habilita Vertex AI.
2. Genera una cuenta de servicio en **API & Services > Credentials**.
3. Descarga el archivo JSON de la cuenta de servicio y guárdalo en la carpeta `config`.
4. Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```ini
GOOGLE_APPLICATION_CREDENTIALS=config/math-ai-assistant-xxxxx.json
GOOGLE_CLOUD_PROJECT=math-ai-assistant-xxxxx
GOOGLE_CLOUD_REGION=us-central1
GCS_BUCKET_NAME=bucket_math_ai
```

### 6. Ejecución del Proyecto
Para iniciar la aplicación con Gradio:
```bash
gradio app.py
```
Esto abrirá una interfaz web donde podrás interactuar con el asistente matemático.

## Referencias
- [Gemini API - Thinking Mode](https://ai.google.dev/gemini-api/docs/thinking)
- [Vertex AI - Thinking Mode](https://cloud.google.com/vertex-ai/generative-ai/docs/thinking)
- [Repositorio Oficial de Google Cloud](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/getting-started/intro_gemini_2_0_flash_thinking_mode.ipynb)

Para más detalles técnicos y ejemplos, consulta el artículo en [Medium](https://console.cloud.google.com/).

Google Cloud credits are provided for this project. #VertexAISprint