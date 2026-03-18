from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from config import Config

class DatabaseService:
    def __init__(self):
        self.client = MongoClient(Config.MONGODB_URI)
        self.db = self.client[Config.MONGODB_DB_NAME]
        self.collection = self.db[Config.MONGODB_COLLECTION]

    def save_message(self, texto, numero_remitente):
        """Guardar mensaje en MongoDB"""
        documento = {
            'texto_mensaje': texto,
            'numero_remitente': numero_remitente,
            'timestamp': datetime.utcnow(),
            'sentimiento': None,
            'tema': None,
            'resumen': None,
            'metadatos': {}
        }
        result = self.collection.insert_one(documento)
        return str(result.inserted_id)

    def get_message_by_id(self, message_id):
        """Obtener mensaje por ID"""
        return self.collection.find_one({'_id': ObjectId(message_id)})

    def update_message_analysis(self, message_id, sentimiento, tema, resumen, metadatos):
        """Actualizar mensaje con análisis de IA"""
        self.collection.update_one(
            {'_id': ObjectId(message_id)},
            {'$set': {
                'sentimiento': sentimiento,
                'tema': tema,
                'resumen': resumen,
                'metadatos': metadatos
            }}
        )

    def get_all_messages(self, limit=50):
        """Obtener mensajes recientes"""
        messages = list(self.collection.find().sort('timestamp', -1).limit(limit))
        # Convertir ObjectId a string para JSON
        for msg in messages:
            msg['_id'] = str(msg['_id'])
        return messages

    def get_sentiment_stats(self):
        """Obtener estadísticas de sentimientos"""
        pipeline = [
            {'$match': {'sentimiento': {'$ne': None}}},
            {'$group': {
                '_id': '$sentimiento',
                'count': {'$sum': 1}
            }}
        ]
        results = list(self.collection.aggregate(pipeline))
        return {item['_id']: item['count'] for item in results}

    def get_topic_stats(self):
        """Obtener estadísticas de temas"""
        pipeline = [
            {'$match': {'tema': {'$ne': None}}},
            {'$group': {
                '_id': '$tema',
                'count': {'$sum': 1}
            }}
        ]
        results = list(self.collection.aggregate(pipeline))
        return {item['_id']: item['count'] for item in results}
