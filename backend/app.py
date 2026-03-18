from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from routes.webhook_routes import webhook_bp
from routes.api_routes import api_bp

# Crear aplicación Flask
app = Flask(__name__)

# Configurar CORS para permitir requests desde el frontend
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",  # Desarrollo local
            "https://*.vercel.app"     # Producción en Vercel
        ]
    },
    r"/webhook/*": {"origins": "*"}  # Twilio puede venir de cualquier IP
})

# Registrar blueprints
app.register_blueprint(webhook_bp)
app.register_blueprint(api_bp)

@app.route('/')
def home():
    """Endpoint raíz"""
    return jsonify({
        'message': 'Café Feedback API',
        'status': 'running',
        'version': '1.0',
        'endpoints': {
            'webhook': '/webhook/whatsapp',
            'api_sentimientos': '/api/sentimientos',
            'api_temas': '/api/temas',
            'api_mensajes': '/api/mensajes-recientes',
            'api_stats': '/api/stats'
        }
    }), 200

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 INICIANDO SERVIDOR FLASK")
    print("="*50)
    print(f"Puerto: {Config.PORT}")
    print(f"Modo: {Config.FLASK_ENV}")
    print(f"MongoDB: Conectado")
    print(f"Endpoints disponibles:")
    print(f"  - GET  /")
    print(f"  - GET  /health")
    print(f"  - POST /webhook/whatsapp")
    print(f"  - GET  /api/sentimientos")
    print(f"  - GET  /api/temas")
    print(f"  - GET  /api/mensajes-recientes")
    print(f"  - GET  /api/stats")
    print("="*50 + "\n")

    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.FLASK_ENV == 'development'
    )
