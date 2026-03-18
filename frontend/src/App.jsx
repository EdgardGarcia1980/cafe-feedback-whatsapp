import React, { useState, useEffect } from 'react';
import { api } from './services/api';
import StatsCard from './components/StatsCard';
import SentimentChart from './components/SentimentChart';
import TopicsChart from './components/TopicsChart';
import MessageFeed from './components/MessageFeed';

function App() {
  const [stats, setStats] = useState(null);
  const [sentimientos, setSentimientos] = useState(null);
  const [temas, setTemas] = useState(null);
  const [mensajes, setMensajes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  const fetchData = async () => {
    try {
      setError(null);
      const [statsData, sentimientosData, temasData, mensajesData] = await Promise.all([
        api.getStats(),
        api.getSentimientos(),
        api.getTemas(),
        api.getMensajesRecientes()
      ]);

      setStats(statsData);
      setSentimientos(sentimientosData);
      setTemas(temasData);
      setMensajes(mensajesData.messages);
      setLastUpdate(new Date());
      setLoading(false);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Error al cargar los datos. Verifica que el backend esté corriendo.');
      setLoading(false);
    }
  };

  useEffect(() => {
    // Cargar datos inicialmente
    fetchData();

    // Actualizar cada 10 segundos
    const interval = setInterval(fetchData, 10000);

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600 font-semibold">Cargando datos...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="bg-red-100 border border-red-400 text-red-700 px-8 py-6 rounded-lg max-w-md">
          <h2 className="text-xl font-bold mb-2">Error</h2>
          <p>{error}</p>
          <button
            onClick={fetchData}
            className="mt-4 bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded"
          >
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                ☕ Café de El Salvador
              </h1>
              <p className="text-gray-600 mt-1">Dashboard de Análisis de Sentimiento</p>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-500">Última actualización:</p>
              <p className="text-sm font-semibold text-gray-700">
                {lastUpdate.toLocaleTimeString('es-SV')}
              </p>
              <div className="mt-2">
                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  <span className="animate-pulse mr-2">●</span> En vivo
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <StatsCard
            title="Total de Mensajes"
            value={stats?.total_mensajes || 0}
            subtitle="Feedback recibido"
            icon="💬"
            color="blue"
          />
          <StatsCard
            title="Tasa de Satisfacción"
            value={`${stats?.tasa_satisfaccion || 0}%`}
            subtitle="Sentimientos positivos"
            icon="⭐"
            color="green"
          />
          <StatsCard
            title="Tema Principal"
            value={stats?.tema_principal || 'N/A'}
            subtitle="Más mencionado"
            icon="📊"
            color="purple"
          />
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <SentimentChart data={sentimientos} />
          <TopicsChart data={temas} />
        </div>

        {/* Messages Feed */}
        <MessageFeed messages={mensajes} />
      </main>

      {/* Footer */}
      <footer className="bg-white shadow-sm mt-12">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <p className="text-center text-gray-500 text-sm">
            Dashboard desarrollado para análisis de feedback de clientes vía WhatsApp
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
