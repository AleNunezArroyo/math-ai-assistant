import os
from pathlib import Path
from google.cloud import storage
from google.api_core.exceptions import GoogleAPICallError, RetryError
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Validar que la variable de entorno esté configurada
bucket_name = os.getenv('GCS_BUCKET_NAME')
if not bucket_name:
    raise ValueError("La variable de entorno 'GCS_BUCKET_NAME' no está configurada.")

def upload_image(source_file_path: str) -> None:
    """
    Sube una imagen a un bucket de Google Cloud Storage.

    Args:
        source_file_path (str): Ruta local del archivo a subir.

    Raises:
        FileNotFoundError: Si el archivo no existe en la ruta especificada.
        GoogleAPICallError: Si ocurre un error al interactuar con Google Cloud Storage.
    """
    source_file = Path(source_file_path)
    
    # Verificar si el archivo existe
    if not source_file.is_file():
        raise FileNotFoundError(f"El archivo '{source_file_path}' no existe.")

    try:
        # Configurar el cliente de Google Cloud Storage
        storage_client = storage.Client()
        
        # Obtener el bucket
        bucket = storage_client.bucket(bucket_name)
        
        # Crear un blob (objeto) en el bucket
        destination_blob_name = source_file.name
        blob = bucket.blob(destination_blob_name)

        # Subir el archivo al blob
        blob.upload_from_filename(source_file_path, timeout=300, retry=storage.retry.DEFAULT_RETRY)

        print(f"Imagen '{source_file_path}' subida como '{destination_blob_name}' en el bucket '{bucket_name}'.")
    
    except (GoogleAPICallError, RetryError) as e:
        print(f"Error al subir la imagen a Google Cloud Storage: {e}")
        raise