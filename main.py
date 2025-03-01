import logging
from pathlib import Path
import os
import re
from typing import Optional, Union
import gradio as gr
from dotenv import load_dotenv
from google import genai
from google.genai.types import Part
from scr.gcs_utils import upload_image
import time

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
LOCATION = os.getenv('GOOGLE_CLOUD_REGION')
BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')

if not PROJECT_ID or not LOCATION or not BUCKET_NAME:
    logger.error("Las variables de entorno necesarias no están definidas.")
    raise EnvironmentError("Faltan variables de entorno para la configuración.")

client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
MODEL_ID = "gemini-2.0-flash-thinking-exp-01-21"

def convert_equations_to_latex(text: str) -> str:
    """
    Convierte ecuaciones en el texto a formato LaTeX.
    - Ecuaciones delimitadas por triple backticks se convierten a modo display.
    """
    if not text:
        return text

    def repl_display(match: re.Match) -> str:
        content = match.group(1).strip()
        return f"$$\n{content}\n$$" if "\n" in content else f"${content}$"

    return re.sub(r"```(.*?)```", repl_display, text, flags=re.DOTALL)

def get_mime_type(file_path: Union[str, Path]) -> str:
    """
    Determina el MIME type de la imagen basándose en la extensión del archivo.
    """
    source_file = Path(file_path)
    extension = source_file.suffix.lstrip('.').lower()
    return f"image/{extension}" if extension else "image/*"

def build_prompt(user_text: Optional[str] = None, include_image: bool = False) -> str:
    """
    Construye un prompt modular basado en una estructura base y agrega:
        - La pregunta del usuario, si se proporciona.
        - Una indicación de utilizar la imagen, si se requiere.
    """
    base_prompt = (
        "Responde de manera detallada a la pregunta del usuario, explicando la solución paso a paso. "
        "Incluye ejemplos claros y relevantes para facilitar la comprensión."
    )
    if user_text:
        base_prompt += f" Pregunta del usuario: {user_text}"
    if include_image:
        base_prompt += " Utiliza la imagen proporcionada para contextualizar la respuesta."
    return base_prompt

def process_input(image_path: Optional[str], user_text: Optional[str], progress=gr.Progress()):
    """
    Procesa la entrada del usuario generando la respuesta mediante:
        - Subida de la imagen si se proporciona.
        - Construcción modular del prompt según los datos disponibles.
    """
    if not user_text and not image_path:
        return "Por favor, ingrese al menos una imagen o un texto."

    time.sleep(0.1)
    progress(0.1, desc="Inicializando...")

    include_image = bool(image_path)
    prompt = build_prompt(user_text, include_image)

    contents = None
    if include_image:
        logger.info("Subiendo imagen: %s", image_path)
        progress(0.3, desc="Subiendo imagen...")
        upload_image(image_path)
        mime_type = get_mime_type(image_path)
        image_part = Part.from_uri(file_uri=f"gs://{BUCKET_NAME}/{Path(image_path).name}", mime_type=mime_type)
        contents = [image_part, prompt]
    else:
        logger.info("Procesando solo texto.")
        progress(0.3, desc="Procesando texto...")
        contents = prompt

    try:
        progress(0.6, desc="Generando respuesta...")
        model_response = client.models.generate_content(
            model=MODEL_ID,
            contents=contents,
        )
    except Exception as e:
        logger.error("Error al generar contenido con el modelo: %s", e)
        progress(1.0, desc="Error al procesar la solicitud.")
        return "Ocurrió un error al procesar su solicitud."

    response_text = model_response.text if model_response and hasattr(model_response, 'text') else ""
    progress(1.0, desc="Procesamiento completado")
    print(response_text)
    return convert_equations_to_latex(response_text)

# Configurar la interfaz de Gradio
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    with gr.Sidebar(position="left"):
        gr.Markdown("# 🤓 Gemini Math AI Assistant")
        gr.Markdown("Resuelve cualquier problema matemático con Gemini Flash Thinking.")
    with gr.Column():
        gr.Markdown("## Subir Imagen y/o Texto")
        text_input = gr.Textbox(label="Ingresar texto", placeholder="Escribe tu pregunta aquí...")
        image_input = gr.Image(type="filepath", label="Subir imagen")
        submit_button = gr.Button("Procesar")
        markdown_output = gr.Markdown(label="Resultado", latex_delimiters=[{"left": "$", "right": "$", "display": True}])

    # Lógica del botón con indicador visual
    submit_button.click(fn=process_input, inputs=[image_input, text_input], outputs=markdown_output)

demo.queue()

if __name__ == "__main__":
    demo.launch()