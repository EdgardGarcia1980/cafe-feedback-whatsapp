import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

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
