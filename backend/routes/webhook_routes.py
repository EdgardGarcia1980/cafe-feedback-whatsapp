from flask import Blueprint, request, jsonify
from services.database_service import DatabaseService
from services.ai_service import AIService

webhook_bp = Blueprint('webhook', __name__)
db_service = DatabaseService()
ai_service = AIService()

@webhook_bp.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """Recibe mensajes de Twilio WhatsApp"""
    try:
        # Obtener datos del mensaje
        texto_mensaje = request.form.get('Body', '').strip()
        numero_remitente = request.form.get('From', '')

        if not texto_mensaje:
            print("⚠️  Mensaje vacío recibido")
            return '', 200

        print(f"\n📩 Mensaje recibido:")
        print(f"   De: {numero_remitente}")
        print(f"   Texto: {texto_mensaje}")

        # Guardar mensaje en MongoDB
        message_id = db_service.save_message(texto_mensaje, numero_remitente)
        print(f"💾 Mensaje guardado con ID: {message_id}")

        # Analizar con IA
        print(f"🤖 Analizando con IA...")
        analisis = ai_service.analizar_sentimiento(texto_mensaje)

        # Actualizar mensaje con análisis
        db_service.update_message_analysis(
            message_id,
            analisis['sentimiento'],
            analisis['tema'],
            analisis['resumen'],
            analisis['metadatos']
        )

        print(f"✅ Análisis completado:")
        print(f"   Sentimiento: {analisis['sentimiento']}")
        print(f"   Tema: {analisis['tema']}")
        print(f"   Resumen: {analisis['resumen']}")
        print(f"   Latencia: {analisis['metadatos'].get('latencia_ms', 0)}ms\n")

        return '', 200

    except Exception as e:
        print(f"❌ Error procesando webhook: {e}")
        import traceback
        traceback.print_exc()
        return str(e), 500

@webhook_bp.route('/webhook/status', methods=['GET'])
def webhook_status():
    """Endpoint para verificar que el webhook está activo"""
    return jsonify({
        'status': 'active',
        'message': 'Webhook funcionando correctamente'
    }), 200
