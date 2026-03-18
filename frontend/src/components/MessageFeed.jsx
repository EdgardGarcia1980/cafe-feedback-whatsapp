import React from 'react';

const MessageFeed = ({ messages }) => {
  const getSentimentColor = (sentimiento) => {
    switch (sentimiento) {
      case 'positivo':
        return 'bg-green-100 text-green-800 border-green-300';
      case 'negativo':
        return 'bg-red-100 text-red-800 border-red-300';
      case 'neutro':
        return 'bg-gray-100 text-gray-800 border-gray-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const getSentimentEmoji = (sentimiento) => {
    switch (sentimiento) {
      case 'positivo':
        return '😊';
      case 'negativo':
        return '😞';
      case 'neutro':
        return '😐';
      default:
        return '❓';
    }
  };

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return 'Fecha desconocida';
    const date = new Date(timestamp);
    return date.toLocaleString('es-SV', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (!messages || messages.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Mensajes Recientes</h2>
        <div className="flex items-center justify-center h-64 text-gray-400">
          No hay mensajes disponibles
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-bold text-gray-800 mb-4">
        Mensajes Recientes ({messages.length})
      </h2>
      <div className="space-y-4 max-h-96 overflow-y-auto">
        {messages.map((message) => (
          <div
            key={message.id}
            className="border-l-4 border-blue-500 bg-gray-50 p-4 rounded-r-lg hover:bg-gray-100 transition-colors"
          >
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center space-x-2">
                <span
                  className={`px-3 py-1 rounded-full text-xs font-semibold border ${getSentimentColor(
                    message.sentimiento
                  )}`}
                >
                  {getSentimentEmoji(message.sentimiento)} {message.sentimiento || 'Sin analizar'}
                </span>
                <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-semibold">
                  {message.tema || 'Sin tema'}
                </span>
              </div>
              <span className="text-xs text-gray-500">
                {formatTimestamp(message.timestamp)}
              </span>
            </div>
            <p className="text-gray-800 mb-2 font-medium">"{message.texto}"</p>
            {message.resumen && (
              <p className="text-sm text-gray-600 italic">
                Resumen: {message.resumen}
              </p>
            )}
            <p className="text-xs text-gray-400 mt-2">
              De: {message.numero}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MessageFeed;
