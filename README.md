# ☕ Sistema de Análisis de Opiniones por WhatsApp
## Café de El Salvador

Sistema que permite recibir comentarios de clientes por WhatsApp, analizar automáticamente el sentimiento usando inteligencia artificial, y mostrar los resultados en un tablero web interactivo.

---

## 📋 Contenido

- [Características](#características)
- [Arquitectura](#arquitectura)
- [Tecnologías](#tecnologías)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Endpoints de la API](#endpoints-de-la-api)
- [Decisiones de diseño](#decisiones-de-diseño)
- [Estructura de archivos](#estructura-de-archivos)
- [Despliegue en producción](#despliegue-en-producción)
- [Documentación adicional](#documentación-adicional)

---

## ✨ Características

### Servidor (Backend)
- ✅ Recibe mensajes de WhatsApp a través de Twilio
- ✅ Guarda los mensajes en MongoDB
- ✅ Analiza automáticamente el sentimiento con OpenAI GPT-3.5
- ✅ Clasifica por tema: Servicio, Calidad, Precio, Limpieza u Otro
- ✅ API REST para consultar estadísticas
- ✅ Validación de datos con Pydantic
- ✅ Registra metadatos de auditoría en cada análisis

### Interfaz Web (Frontend)
- ✅ Tablero interactivo con React + Vite
- ✅ Gráfico circular de distribución de sentimientos
- ✅ Gráfico de barras de temas más comentados
- ✅ Lista de mensajes recientes actualizada en tiempo real
- ✅ Se actualiza automáticamente cada 10 segundos
- ✅ Diseño adaptable a móviles con TailwindCSS

### Controles de calidad
- ✅ Validación estricta de respuestas del modelo de IA
- ✅ Registro de metadatos: modelo usado, tiempo de respuesta, versión del prompt
- ✅ Manejo de errores robusto
- ✅ Logs detallados de cada operación

---

## 🏗️ Arquitectura

El sistema tiene tres componentes principales:

```
┌─────────────┐      WhatsApp     ┌──────────┐
│   Cliente   │ ─────────────────► │  Twilio  │
└─────────────┘                    └─────┬────┘
                                         │ HTTPS
                                         ▼
                                  ┌──────────────┐
                                  │   Servidor   │
                                  │ Flask/Python │
                                  └──────┬───────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    ▼                    ▼                    ▼
             ┌────────────┐       ┌───────────┐       ┌──────────┐
             │  MongoDB   │       │  OpenAI   │       │  React   │
             │    Base    │       │    API    │       │   Web    │
             │  de datos  │       │           │       │          │
             └────────────┘       └───────────┘       └──────────┘
```

Ver diagramas C4 completos en: [`documentacion/DIAGRAMAS_C4.md`](documentacion/DIAGRAMAS_C4.md)

---

## 🛠️ Tecnologías

### Servidor
- **Python 3.10+**
- **Flask 3.0** - Para crear la API web
- **MongoDB** - Base de datos NoSQL
- **Twilio API** - Integración con WhatsApp
- **OpenAI API (GPT-3.5-turbo)** - Análisis de sentimientos
- **Pydantic** - Validación de datos
- **python-dotenv** - Manejo de variables de entorno

### Interfaz Web
- **React 18** - Biblioteca de componentes
- **Vite** - Empaquetador rápido
- **TailwindCSS** - Estilos CSS
- **Recharts** - Gráficos
- **Axios** - Peticiones HTTP

### Servicios externos
- **ngrok** - Exponer servidor local (desarrollo)
- **MongoDB Atlas** - Base de datos en la nube
- **Railway** - Hosting del servidor (producción)
- **Vercel** - Hosting de la interfaz web (producción)

---

## 📦 Requisitos

- **Python 3.10+** instalado
- **Node.js 18+** y npm instalados
- Cuenta de **Twilio** con Sandbox de WhatsApp
- Cuenta de **MongoDB Atlas** (o MongoDB local)
- Clave de API de **OpenAI**
- **ngrok** (solo para desarrollo local)

---

## ⚙️ Instalación

### 1. Descargar el proyecto

```bash
git clone https://github.com/EdgardGarcia1980/cafe-feedback-whatsapp.git
cd cafe-feedback-whatsapp
```

### 2. Configurar el servidor

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
MONGODB_URI=mongodb+srv://usuario:contraseña@cluster.mongodb.net/?appName=Cluster0

# OpenAI
OPENAI_API_KEY=tu_clave_api_openai

# Configuración
PORT=5000
FLASK_ENV=development
```

### 4. Probar las conexiones

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

### 5. Configurar la interfaz web

```bash
cd ../frontend

# Instalar dependencias
npm install
```

---

## 🚀 Uso

### Iniciar el servidor

```bash
cd backend
venv\Scripts\activate  # Windows
python app.py
```

El servidor estará en `http://localhost:5000`

### Exponer el servidor con ngrok

En otra terminal:

```bash
ngrok http 5000
```

Copia la URL que te da (ejemplo: `https://abc123.ngrok.io`)

### Configurar Twilio

1. Ir a [Twilio Console - WhatsApp Sandbox](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn)
2. En "When a message comes in", pegar: `https://tu-url-ngrok.ngrok.io/webhook/whatsapp`
3. Método: **POST**
4. Guardar

### Iniciar la interfaz web

En otra terminal:

```bash
cd frontend
npm run dev
```

El tablero estará en `http://localhost:3000`

### Enviar mensajes de prueba

Desde WhatsApp, envía un mensaje al número de Twilio Sandbox:

```
El café estaba delicioso!
```

El sistema:
1. ✅ Recibe el mensaje
2. ✅ Lo guarda en MongoDB
3. ✅ Lo analiza con OpenAI
4. ✅ Actualiza el tablero web

---

## 📡 Endpoints de la API

### Recepción de mensajes

- **POST** `/webhook/whatsapp` - Recibe mensajes de Twilio
- **GET** `/webhook/status` - Verifica estado

### Consulta de datos

- **GET** `/api/sentimientos` - Distribución de sentimientos
- **GET** `/api/temas` - Frecuencia de temas
- **GET** `/api/mensajes-recientes` - Últimos 50 mensajes
- **GET** `/api/stats` - Estadísticas generales

### Estado del sistema

- **GET** `/` - Información de la API
- **GET** `/health` - Verificación de estado

### Ejemplo de respuesta

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

## 🧠 Decisiones de diseño

### ¿Por qué MongoDB en lugar de SQL?

**Razones:**
- Esquema flexible para mensajes de texto
- Fácil agregar campos nuevos sin migraciones
- Agregaciones potentes para estadísticas
- Escala horizontalmente
- Trabaja nativamente con JSON

**Consideración:** Menos garantías ACID, pero no es crítico para este caso.

Ver análisis completo en: [`documentacion/MATRIZ_VALOR_TRADEOFFS.md`](documentacion/MATRIZ_VALOR_TRADEOFFS.md)

### Estrategia del prompt a OpenAI

**Técnica:** Aprendizaje por ejemplos (Few-shot learning)

**Razones:**
- Categorización más precisa
- Formato JSON consistente
- Los ejemplos guían al modelo
- Menos procesamiento posterior

**Estructura:**
- Contexto claro (analista para un café)
- 4 ejemplos representativos
- Instrucción de devolver solo JSON
- Esquema explícito de respuesta

Ver estrategia completa en: [`documentacion/ESTRATEGIA_PROMPTS.md`](documentacion/ESTRATEGIA_PROMPTS.md)

---

## 📁 Estructura de archivos

```
cafe-feedback-whatsapp/
├── backend/
│   ├── app.py                 # Aplicación Flask
│   ├── config.py              # Configuración
│   ├── requirements.txt       # Dependencias Python
│   ├── test_connection.py     # Prueba de conexiones
│   ├── .env                   # Variables de entorno
│   ├── models/
│   │   └── message.py
│   ├── routes/
│   │   ├── webhook_routes.py  # Rutas de Twilio
│   │   └── api_routes.py      # Rutas de consulta
│   └── services/
│       ├── database_service.py  # Lógica de MongoDB
│       └── ai_service.py        # Lógica de OpenAI
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Componente principal
│   │   ├── main.jsx           # Inicio de la aplicación
│   │   ├── components/
│   │   │   ├── SentimentChart.jsx
│   │   │   ├── TopicsChart.jsx
│   │   │   ├── MessageFeed.jsx
│   │   │   └── StatsCard.jsx
│   │   └── services/
│   │       └── api.js         # Cliente para la API
│   ├── package.json
│   └── vite.config.js
└── documentacion/
    ├── DIAGRAMAS_C4.md
    ├── CUSTOMER_JOURNEY_MAP.md
    ├── MATRIZ_VALOR_TRADEOFFS.md
    └── ESTRATEGIA_PROMPTS.md
```

---

## 🌐 Despliegue en producción

### Servidor - Railway

1. Crear cuenta en [Railway.app](https://railway.app)
2. Conectar repositorio de GitHub
3. Configurar Root Directory: `backend`
4. Agregar variables de entorno (las mismas del `.env`)
5. Railway desplegará automáticamente

### Interfaz Web - Vercel

1. Crear cuenta en [Vercel.com](https://vercel.com)
2. Importar repositorio de GitHub
3. Configurar Root Directory: `frontend`
4. Vercel desplegará automáticamente

### Configurar Twilio para producción

1. Ir a Twilio Console
2. Actualizar "When a message comes in" con la URL de Railway:
   ```
   https://tu-app.up.railway.app/webhook/whatsapp
   ```
3. Guardar

---

## 📚 Documentación adicional

- [Diagramas C4 (Sistema, Contenedores, Componentes, Despliegue)](documentacion/DIAGRAMAS_C4.md)
- [Mapa del recorrido del cliente](documentacion/CUSTOMER_JOURNEY_MAP.md)
- [Matriz de valor y consideraciones técnicas](documentacion/MATRIZ_VALOR_TRADEOFFS.md)
- [Estrategia de prompts para IA](documentacion/ESTRATEGIA_PROMPTS.md)

---

## 🧪 Pruebas

### Servidor

```bash
# Probar conexiones
python test_connection.py

# Probar manualmente el webhook
curl -X POST http://localhost:5000/webhook/whatsapp \
  -d "Body=Mensaje de prueba" \
  -d "From=whatsapp:+1234567890"
```

### Interfaz Web

```bash
npm run dev
# Abrir http://localhost:3000
```

---

## 🐛 Solución de problemas

### Error: MongoDB connection timeout
- Verificar que tu IP esté en la lista blanca de MongoDB Atlas (0.0.0.0/0 permite todas)
- Revisar el connection string en `.env`

### Error: Twilio no recibe mensajes
- Verificar que ngrok esté corriendo
- Revisar la URL en Twilio Console
- Verificar que el servidor esté corriendo

### Error: OpenAI quota exceeded
- Verificar créditos disponibles en OpenAI
- Agregar método de pago para aumentar el límite

---

## 👤 Autor

Proyecto desarrollado como prueba técnica para demostrar habilidades en desarrollo full-stack y arquitectura de software.

---

## 📄 Licencia

Este proyecto es para fines educativos y de evaluación técnica.
