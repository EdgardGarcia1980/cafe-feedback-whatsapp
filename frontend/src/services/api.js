import axios from 'axios';

// Usar URL de producción si está en build de producción, sino localhost
const API_BASE_URL = import.meta.env.PROD
  ? 'RAILWAY_URL_PLACEHOLDER/api'  // Se actualizará después del deploy
  : 'http://localhost:5000/api';

export const api = {
  // Obtener estadísticas de sentimientos
  getSentimientos: async () => {
    const response = await axios.get(`${API_BASE_URL}/sentimientos`);
    return response.data;
  },

  // Obtener estadísticas de temas
  getTemas: async () => {
    const response = await axios.get(`${API_BASE_URL}/temas`);
    return response.data;
  },

  // Obtener mensajes recientes
  getMensajesRecientes: async () => {
    const response = await axios.get(`${API_BASE_URL}/mensajes-recientes`);
    return response.data;
  },

  // Obtener estadísticas generales
  getStats: async () => {
    const response = await axios.get(`${API_BASE_URL}/stats`);
    return response.data;
  }
};
