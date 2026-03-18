from flask import Blueprint, jsonify
from services.database_service import DatabaseService

api_bp = Blueprint('api', __name__)
db_service = DatabaseService()

@api_bp.route('/api/sentimientos', methods=['GET'])
def get_sentimientos():
    """Obtener distribución de sentimientos"""
    try:
        stats = db_service.get_sentiment_stats()

        # Formato para el frontend
        data = {
            'positivo': stats.get('positivo', 0),
            'negativo': stats.get('negativo', 0),
            'neutro': stats.get('neutro', 0)
        }

        total = sum(data.values())

        # Calcular porcentajes
        porcentajes = {}
        if total > 0:
            porcentajes = {
                'positivo': round((data['positivo'] / total) * 100, 1),
                'negativo': round((data['negativo'] / total) * 100, 1),
                'neutro': round((data['neutro'] / total) * 100, 1)
            }

        return jsonify({
            'counts': data,
            'percentages': porcentajes,
            'total': total
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/temas', methods=['GET'])
def get_temas():
    """Obtener frecuencia de temas"""
    try:
        stats = db_service.get_topic_stats()

        # Formato para el frontend (array de objetos para gráficos)
        data = [
            {'tema': tema, 'count': count}
            for tema, count in stats.items()
        ]

        # Ordenar por count descendente
        data.sort(key=lambda x: x['count'], reverse=True)

        return jsonify({
            'data': data,
            'total': sum(item['count'] for item in data)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/mensajes-recientes', methods=['GET'])
def get_mensajes_recientes():
    """Obtener últimos mensajes con análisis"""
    try:
        messages = db_service.get_all_messages(limit=50)

        # Formatear para el frontend
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                'id': msg['_id'],
                'texto': msg['texto_mensaje'],
                'numero': msg['numero_remitente'],
                'timestamp': msg['timestamp'].isoformat() if msg.get('timestamp') else None,
                'sentimiento': msg.get('sentimiento'),
                'tema': msg.get('tema'),
                'resumen': msg.get('resumen')
            })

        return jsonify({
            'messages': formatted_messages,
            'count': len(formatted_messages)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/stats', methods=['GET'])
def get_stats():
    """Obtener estadísticas generales"""
    try:
        # Obtener mensajes
        messages = db_service.get_all_messages(limit=1000)

        # Estadísticas básicas
        total_mensajes = len(messages)

        # Contar sentimientos
        sentimientos = {'positivo': 0, 'negativo': 0, 'neutro': 0}
        temas = {}

        for msg in messages:
            sent = msg.get('sentimiento')
            if sent in sentimientos:
                sentimientos[sent] += 1

            tema = msg.get('tema')
            if tema:
                temas[tema] = temas.get(tema, 0) + 1

        # Calcular tasa de satisfacción
        total_analizados = sum(sentimientos.values())
        tasa_satisfaccion = 0
        if total_analizados > 0:
            tasa_satisfaccion = round((sentimientos['positivo'] / total_analizados) * 100, 1)

        # Tema más mencionado
        tema_principal = max(temas.items(), key=lambda x: x[1])[0] if temas else 'N/A'

        return jsonify({
            'total_mensajes': total_mensajes,
            'tasa_satisfaccion': tasa_satisfaccion,
            'tema_principal': tema_principal,
            'sentimientos': sentimientos,
            'temas': temas
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
