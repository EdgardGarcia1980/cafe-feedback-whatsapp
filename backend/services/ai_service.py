from openai import OpenAI
from config import Config
import json
import time

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = "gpt-3.5-turbo"
        self.prompt_version = "1.0"

    def analizar_sentimiento(self, texto):
        """Analizar sentimiento del mensaje usando OpenAI"""
        start_time = time.time()

        prompt = f"""Eres un analista de sentimientos para un café. Analiza el siguiente mensaje de feedback de un cliente y devuelve ÚNICAMENTE un JSON con esta estructura exacta:

{{
  "sentimiento": "positivo" | "negativo" | "neutro",
  "tema": "Servicio al Cliente" | "Calidad del Producto" | "Precio" | "Limpieza" | "Otro",
  "resumen": "Descripción breve del feedback en una oración"
}}

Ejemplos:

Mensaje: "El café estaba delicioso pero tardaron mucho en atenderme"
Respuesta: {{"sentimiento": "neutro", "tema": "Servicio al Cliente", "resumen": "Cliente satisfecho con café pero insatisfecho con tiempo de espera"}}

Mensaje: "Excelente atención, volveré pronto!"
Respuesta: {{"sentimiento": "positivo", "tema": "Servicio al Cliente", "resumen": "Cliente muy satisfecho con la atención recibida"}}

Mensaje: "El baño estaba sucio y el lugar descuidado"
Respuesta: {{"sentimiento": "negativo", "tema": "Limpieza", "resumen": "Cliente insatisfecho con limpieza del establecimiento"}}

Mensaje: "Los precios están muy altos para la calidad"
Respuesta: {{"sentimiento": "negativo", "tema": "Precio", "resumen": "Cliente considera que precios no justifican la calidad"}}

Ahora analiza este mensaje:
Mensaje: "{texto}"
Respuesta:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un analista experto en análisis de sentimientos para negocios de café. Siempre respondes en formato JSON válido."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )

            # Obtener respuesta
            content = response.choices[0].message.content.strip()

            # Parsear JSON
            try:
                analisis = json.loads(content)
            except json.JSONDecodeError:
                # Si no es JSON válido, intentar extraerlo
                if '{' in content and '}' in content:
                    json_start = content.index('{')
                    json_end = content.rindex('}') + 1
                    analisis = json.loads(content[json_start:json_end])
                else:
                    raise ValueError("No se pudo parsear la respuesta como JSON")

            # Validar campos requeridos
            required_fields = ['sentimiento', 'tema', 'resumen']
            if not all(field in analisis for field in required_fields):
                raise ValueError("Faltan campos requeridos en la respuesta")

            # Validar valores de sentimiento
            if analisis['sentimiento'] not in ['positivo', 'negativo', 'neutro']:
                analisis['sentimiento'] = 'neutro'

            # Validar valores de tema
            temas_validos = ['Servicio al Cliente', 'Calidad del Producto', 'Precio', 'Limpieza', 'Otro']
            if analisis['tema'] not in temas_validos:
                analisis['tema'] = 'Otro'

            # Calcular latencia
            latencia_ms = int((time.time() - start_time) * 1000)

            # Agregar metadatos
            analisis['metadatos'] = {
                'modelo_id': self.model,
                'latencia_ms': latencia_ms,
                'version_prompt': self.prompt_version,
                'tokens_used': response.usage.total_tokens
            }

            return analisis

        except Exception as e:
            print(f"Error en análisis de IA: {e}")
            # Retornar valores por defecto en caso de error
            return {
                'sentimiento': 'neutro',
                'tema': 'Otro',
                'resumen': f'Error en análisis: {str(e)[:100]}',
                'metadatos': {
                    'modelo_id': self.model,
                    'latencia_ms': int((time.time() - start_time) * 1000),
                    'version_prompt': self.prompt_version,
                    'error': str(e)
                }
            }
