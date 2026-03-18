# ☕ Dashboard de Sentimiento del Cliente vía WhatsApp
## Café de El Salvador - Sistema de Análisis de Feedback

Sistema completo end-to-end que permite a un negocio local recibir feedback de clientes a través de WhatsApp, analizar automáticamente el sentimiento con IA, y visualizar insights en tiempo real mediante un dashboard interactivo.

---

## 📋 Tabla de Contenidos

- [Características](#características)
- [Arquitectura](#arquitectura)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Requisitos Previos](#requisitos-previos)
- [Instalación y Configuración](#instalación-y-configuración)
- [Uso](#uso)
- [Endpoints API](#endpoints-api)
- [Decisiones Técnicas](#decisiones-técnicas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Deployment](#deployment)
- [Documentación Adicional](#documentación-adicional)

---

## ✨ Características

### Backend
- ✅ Webhook para recibir mensajes de WhatsApp vía Twilio
- ✅ Almacenamiento en MongoDB con esquema flexible
- ✅ Análisis de sentimiento automático con OpenAI GPT-3.5
- ✅ Clasificación por temas (Servicio, Calidad, Precio, Limpieza, Otro)
- ✅ API RESTful para consultar estadísticas
- ✅ Validación de esquemas con Pydantic
- ✅ Trazabilidad completa (metadatos de auditoría)

### Frontend
- ✅ Dashboard interactivo con React + Vite
- ✅ Gráfico de pastel para distribución de sentimientos
- ✅ Gráfico de barras para temas más mencionados
- ✅ Feed en tiempo real de mensajes recientes
- ✅ Actualización automática cada 10 segundos
- ✅ Diseño responsive con TailwindCSS

### Gobernanza
- ✅ Validación estricta de respuestas del LLM
- ✅ Metadatos de auditoría (modelo, latencia, versión de prompt)
- ✅ Manejo robusto de errores
- ✅ Logging detallado

---

## 🏗️ Arquitectura

El sistema sigue una arquitectura de tres capas:

```
┌─────────────┐      WhatsApp     ┌──────────┐
│   Cliente   │ ─────────────────► │  Twilio  │
└─────────────┘                    └─────┬────┘
                                         │ Webhook (HTTPS)
                                         ▼
                                  ┌──────────────┐
                                  │   Backend    │
                                  │ Flask/Python │
                                  └──────┬───────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    ▼                    ▼                    ▼
             ┌────────────┐       ┌───────────┐       ┌──────────┐
             │  MongoDB   │       │  OpenAI   │       │ Frontend │
             │  Database  │       │    API    │       │  React   │
             └────────────┘       └───────────┘       └──────────┘
```

Ver diagramas C4 completos en: [`documentacion/DIAGRAMAS_C4.md`](documentacion/DIAGRAMAS_C4.md)

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.10+**
- **Flask 3.0** - Framework web
- **MongoDB** - Base de datos NoSQL
- **Twilio API** - Integración WhatsApp
- **OpenAI API (GPT-3.5-turbo)** - Análisis de sentimiento
- **Pydantic** - Validación de datos
- **python-dotenv** - Gestión de variables de entorno

### Frontend
- **React 18** - Librería UI
- **Vite** - Build tool
- **TailwindCSS** - Framework CSS
- **Recharts** - Librería de gráficos
- **Axios** - Cliente HTTP

### Infraestructura
- **ngrok** - Exposición de webhook local (desarrollo)
- **MongoDB Atlas** - Base de datos cloud
- **Twilio Sandbox** - Testing WhatsApp

---

## 📦 Requisitos Previos

- **Python 3.10+** instalado
- **Node.js 18+** y npm instalados
- Cuenta de **Twilio** con WhatsApp Sandbox configurado
- Cuenta de **MongoDB Atlas** (o MongoDB local)
- API Key de **OpenAI**
- **ngrok** (para desarrollo local)

---

## ⚙️ Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd prueba_tecnica
```

### 2. Configurar Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Crear archivo `backend/.env`:

```env
# Twilio
TWILIO_ACCOUNT_SID=tu_account_sid
TWILIO_AUTH_TOKEN=tu_auth_token
TWILIO_PHONE_NUMBER=whatsapp:+14155238886

# MongoDB
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/?appName=Cluster0

# OpenAI
OPENAI_API_KEY=tu_openai_api_key

# App Config
PORT=5000
FLASK_ENV=development
```

### 4. Probar conexiones

```bash
python test_connection.py
```

Deberías ver:
```
✓ Conexión exitosa a MongoDB
✓ Credenciales válidas - Cuenta: [Tu cuenta Twilio]
✓ API Key válida
✅ ¡Listo para continuar!
```

### 5. Configurar Frontend

```bash
cd ../frontend

# Instalar dependencias
npm install
```

---

## 🚀 Uso

### Iniciar Backend

```bash
cd backend
venv\Scripts\activate  # Windows
python app.py
```

El servidor estará disponible en `http://localhost:5000`

### Exponer Webhook con ngrok

En otra terminal:

```bash
ngrok http 5000
```

Copiar la URL generada (ejemplo: `https://abc123.ngrok.io`)

### Configurar Twilio

1. Ir a [Twilio Console - WhatsApp Sandbox](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn)
2. En "When a message comes in", pegar: `https://tu-url-ngrok.ngrok.io/webhook/whatsapp`
3. Método: **POST**
4. Guardar

### Iniciar Frontend

En otra terminal:

```bash
cd frontend
npm run dev
```

El dashboard estará disponible en `http://localhost:3000`

### Enviar Mensajes de Prueba

Desde WhatsApp, enviar mensaje al número de Twilio Sandbox:

```
El café estaba delicioso!
```

El sistema:
1. ✅ Recibe el mensaje
2. ✅ Guarda en MongoDB
3. ✅ Analiza con OpenAI
4. ✅ Actualiza el dashboard

---

## 📡 Endpoints API

### Webhook

- **POST** `/webhook/whatsapp` - Recibe mensajes de Twilio
- **GET** `/webhook/status` - Verifica estado del webhook

### API Dashboard

- **GET** `/api/sentimientos` - Distribución de sentimientos
- **GET** `/api/temas` - Frecuencia de temas
- **GET** `/api/mensajes-recientes` - Últimos 50 mensajes
- **GET** `/api/stats` - Estadísticas generales

### Health

- **GET** `/` - Información de la API
- **GET** `/health` - Health check

### Ejemplo de Respuesta

**GET** `/api/sentimientos`:
```json
{
  "counts": {
    "positivo": 15,
    "negativo": 3,
    "neutro": 5
  },
  "percentages": {
    "positivo": 65.2,
    "negativo": 13.0,
    "neutro": 21.7
  },
  "total": 23
}
```

---

## 🧠 Decisiones Técnicas

### MongoDB vs SQL

**Decisión:** MongoDB

**Razones:**
- ✅ Esquema flexible para datos no estructurados (mensajes de texto libre)
- ✅ Fácil adición de nuevos campos sin migrations
- ✅ Pipeline de agregación potente para estadísticas
- ✅ Escalabilidad horizontal nativa
- ✅ JSON nativo (ideal para respuestas del LLM)

**Trade-off:** Menos ACID guarantees, pero no es crítico para este caso de uso.

Ver análisis completo en: [`documentacion/MATRIZ_VALOR_TRADEOFFS.md`](documentacion/MATRIZ_VALOR_TRADEOFFS.md)

### Estrategia de Prompts

**Técnica:** Few-shot learning

**Razones:**
- ✅ Mayor precisión en categorización
- ✅ Formato JSON consistente
- ✅ Ejemplos guían al modelo
- ✅ Menor necesidad de post-procesamiento

**Estructura del Prompt:**
- Contexto claro (analista para un café)
- 4 ejemplos representativos
- Instrucción de devolver solo JSON
- Schema explícito

Ver estrategia completa en: [`documentacion/ESTRATEGIA_PROMPTS.md`](documentacion/ESTRATEGIA_PROMPTS.md)

---

## 📁 Estructura del Proyecto

```
prueba_tecnica/
├── backend/
│   ├── app.py                 # Aplicación Flask principal
│   ├── config.py              # Configuración
│   ├── requirements.txt       # Dependencias Python
│   ├── test_connection.py     # Script de prueba
│   ├── .env                   # Variables de entorno
│   ├── models/
│   │   └── message.py
│   ├── routes/
│   │   ├── webhook_routes.py  # Rutas del webhook
│   │   └── api_routes.py      # Rutas de la API
│   └── services/
│       ├── database_service.py  # Servicio MongoDB
│       └── ai_service.py        # Servicio OpenAI
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Componente principal
│   │   ├── main.jsx           # Entry point
│   │   ├── components/
│   │   │   ├── SentimentChart.jsx
│   │   │   ├── TopicsChart.jsx
│   │   │   ├── MessageFeed.jsx
│   │   │   └── StatsCard.jsx
│   │   └── services/
│   │       └── api.js         # Cliente API
│   ├── package.json
│   └── vite.config.js
└── documentacion/
    ├── DIAGRAMAS_C4.md
    ├── CUSTOMER_JOURNEY_MAP.md
    ├── MATRIZ_VALOR_TRADEOFFS.md
    └── ESTRATEGIA_PROMPTS.md
```

---

## 🌐 Deployment

### Backend - Railway/Render

```bash
# 1. Crear Procfile
echo "web: python app.py" > Procfile

# 2. Configurar variables de entorno en Railway
# 3. Deploy desde GitHub
```

### Frontend - Vercel

```bash
# 1. Actualizar API_BASE_URL en src/services/api.js
# 2. Deploy con Vercel CLI
vercel --prod
```

Ver guía completa de deployment en: `documentacion/DEPLOYMENT.md`

---

## 📚 Documentación Adicional

- [Diagramas C4 (System Context, Container, Component, Deployment)](documentacion/DIAGRAMAS_C4.md)
- [Customer Journey Map](documentacion/CUSTOMER_JOURNEY_MAP.md)
- [Matriz de Valor y Trade-offs](documentacion/MATRIZ_VALOR_TRADEOFFS.md)
- [Estrategia de Prompts](documentacion/ESTRATEGIA_PROMPTS.md)

---

## 🧪 Testing

### Backend

```bash
# Test de conexiones
python test_connection.py

# Test manual del webhook
curl -X POST http://localhost:5000/webhook/whatsapp \
  -d "Body=Test message" \
  -d "From=whatsapp:+1234567890"
```

### Frontend

```bash
npm run dev
# Abrir http://localhost:3000
```

---

## 🐛 Troubleshooting

### Error: MongoDB connection timeout
- Verificar IP whitelist en MongoDB Atlas (0.0.0.0/0)
- Verificar connection string en .env

### Error: Twilio webhook no recibe mensajes
- Verificar que ngrok esté corriendo
- Verificar URL en Twilio Console
- Verificar que backend esté corriendo

### Error: OpenAI quota exceeded
- Verificar créditos en OpenAI
- Considerar usar Anthropic Claude

---

## 👤 Autor

Desarrollado como prueba técnica para evaluación de habilidades full-stack y arquitectura de software.

---

## 📄 Licencia

Este proyecto es para fines educativos y de evaluación técnica.
