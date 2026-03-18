# Diagramas C4 - Dashboard de Sentimiento del Cliente

Este documento contiene las especificaciones detalladas para los 4 diagramas C4 del sistema.

**Herramientas recomendadas:**
- [draw.io](https://app.diagrams.net/)
- [Miro](https://miro.com/)
- [Lucidchart](https://www.lucidchart.com/)
- [PlantUML](https://plantuml.com/) (código)

---

## 1. System Context Diagram

### Propósito
Muestra el sistema en su contexto más amplio, con los actores y sistemas externos que interactúan con él.

### Elementos

#### Actores (Personas)
1. **Cliente**
   - Rol: Usuario del café que envía feedback
   - Interacción: Envía mensajes de WhatsApp

2. **Gerente**
   - Rol: Administrador del café
   - Interacción: Visualiza el dashboard para tomar decisiones

#### Sistemas Externos
1. **WhatsApp**
   - Descripción: Plataforma de mensajería
   - Interacción: Cliente envía mensajes

2. **Twilio**
   - Descripción: API Gateway para WhatsApp
   - Interacción: Recibe mensajes y los envía al sistema vía webhook

#### Sistema Principal
**"Sistema de Análisis de Feedback - Café de El Salvador"**
- Descripción: Plataforma que recibe, analiza y visualiza feedback de clientes

### Relaciones

```
Cliente ──[envía feedback]──> WhatsApp
WhatsApp ──[reenvía mensajes]──> Twilio
Twilio ──[webhook HTTPS]──> Sistema de Análisis de Feedback
Sistema de Análisis de Feedback ──[muestra dashboard]──> Gerente
```

### Descripción de Flujo
1. Cliente envía mensaje de WhatsApp al número del café
2. WhatsApp reenvía a Twilio
3. Twilio envía webhook al sistema
4. Sistema procesa, analiza y almacena
5. Gerente visualiza resultados en dashboard web

---

## 2. Container Diagram

### Propósito
Muestra los principales contenedores (aplicaciones/servicios) del sistema y cómo se comunican entre sí.

### Contenedores

1. **React Frontend (SPA)**
   - Tecnología: React 18 + Vite + TailwindCSS
   - Puerto: 3000
   - Responsabilidad: Dashboard interactivo para visualizar datos
   - Actualización: Polling cada 10 segundos

2. **Backend API**
   - Tecnología: Python + Flask
   - Puerto: 5000
   - Responsabilidad:
     - Recibir webhooks de Twilio
     - Analizar mensajes con IA
     - Proveer API REST para frontend
   - Componentes:
     - Webhook Controller
     - AI Analysis Service
     - Database Service

3. **MongoDB Database**
   - Tecnología: MongoDB Atlas
   - Responsabilidad: Almacenar mensajes y análisis
   - Colecciones:
     - `mensajes` - Mensajes con análisis de sentimiento

4. **OpenAI API** (Sistema Externo)
   - Servicio: GPT-3.5-turbo
   - Responsabilidad: Análisis de sentimiento y categorización

5. **Twilio API** (Sistema Externo)
   - Servicio: WhatsApp Business API
   - Responsabilidad: Gateway de mensajería

### Relaciones y Protocolos

```
[React Frontend] ──HTTP/REST──> [Backend API]
                     (JSON)

[Backend API] ──MongoDB Driver──> [MongoDB Database]
              (BSON/JSON)

[Backend API] ──HTTPS/REST──> [OpenAI API]
              (JSON)

[Twilio API] ──HTTPS Webhook──> [Backend API]
             (POST /webhook/whatsapp)
```

### Endpoints Clave

**Backend API:**
- `POST /webhook/whatsapp` - Recibe mensajes de Twilio
- `GET /api/sentimientos` - Distribución de sentimientos
- `GET /api/temas` - Frecuencia de temas
- `GET /api/mensajes-recientes` - Últimos mensajes
- `GET /api/stats` - Estadísticas generales

---

## 3. Component Diagram (Backend)

### Propósito
Descompone el Backend API en sus componentes internos.

### Componentes

#### 1. **Webhook Controller** (`routes/webhook_routes.py`)
- **Responsabilidad:**
  - Recibir requests HTTP de Twilio
  - Validar firma de Twilio (seguridad)
  - Extraer datos del mensaje
  - Orquestar el flujo de procesamiento
- **Dependencias:**
  - Message Service
  - AI Analysis Service
- **Endpoints:**
  - `POST /webhook/whatsapp`
  - `GET /webhook/status`

#### 2. **API Controller** (`routes/api_routes.py`)
- **Responsabilidad:**
  - Exponer endpoints REST para el frontend
  - Formatear respuestas en JSON
  - Manejo de errores HTTP
- **Dependencias:**
  - Database Service
- **Endpoints:**
  - `GET /api/sentimientos`
  - `GET /api/temas`
  - `GET /api/mensajes-recientes`
  - `GET /api/stats`

#### 3. **Database Service** (`services/database_service.py`)
- **Responsabilidad:**
  - Operaciones CRUD en MongoDB
  - Agregaciones para estadísticas
  - Gestión de conexión a BD
- **Métodos:**
  - `save_message(texto, numero)`
  - `update_message_analysis(id, sentimiento, tema, resumen)`
  - `get_all_messages(limit)`
  - `get_sentiment_stats()`
  - `get_topic_stats()`

#### 4. **AI Analysis Service** (`services/ai_service.py`)
- **Responsabilidad:**
  - Comunicación con OpenAI API
  - Construcción del prompt (Few-shot)
  - Validación de respuesta JSON
  - Manejo de errores de IA
  - Cálculo de latencia
- **Métodos:**
  - `analizar_sentimiento(texto)` → `{sentimiento, tema, resumen, metadatos}`
- **Metadatos generados:**
  - `modelo_id`: Modelo usado (gpt-3.5-turbo)
  - `latencia_ms`: Tiempo de respuesta
  - `version_prompt`: Versión del prompt
  - `tokens_used`: Tokens consumidos

#### 5. **Config Module** (`config.py`)
- **Responsabilidad:**
  - Cargar variables de entorno
  - Centralizar configuración
  - Validar credenciales
- **Variables:**
  - Twilio credentials
  - MongoDB URI
  - OpenAI API Key
  - Flask settings

### Flujo de Procesamiento de Mensaje

```
1. [Twilio] ──HTTP POST──> [Webhook Controller]
                                │
2. [Webhook Controller] ──extract──> (Body, From)
                                │
3. [Webhook Controller] ──call──> [Database Service].save_message()
                                │
4. [Database Service] ──insert──> [MongoDB]
                                │
5. [Webhook Controller] ──call──> [AI Analysis Service].analizar_sentimiento()
                                │
6. [AI Analysis Service] ──API request──> [OpenAI]
                                │
7. [OpenAI] ──JSON response──> [AI Analysis Service]
                                │
8. [AI Analysis Service] ──validate & parse──> {sentimiento, tema, resumen}
                                │
9. [Webhook Controller] ──call──> [Database Service].update_message_analysis()
                                │
10. [Database Service] ──update──> [MongoDB]
                                │
11. [Webhook Controller] ──return──> 200 OK
```

### Validación y Gobernanza

**Schema de Validación (Pydantic):**
```python
{
  "sentimiento": enum ["positivo", "negativo", "neutro"],
  "tema": enum ["Servicio al Cliente", "Calidad del Producto",
                "Precio", "Limpieza", "Otro"],
  "resumen": string (max 500 chars)
}
```

**Manejo de Errores:**
- Try-catch en cada nivel
- Logging detallado
- Valores por defecto si IA falla
- Retry logic (máx 3 intentos)

---

## 4. Deployment Diagram

### Propósito
Muestra cómo el sistema se despliega en infraestructura real (desarrollo y producción).

---

## Deployment - Desarrollo

### Máquina Local del Desarrollador

**Node 1: Backend Server**
- Sistema Operativo: Windows 10/11
- Runtime: Python 3.10
- Proceso: Flask Dev Server
- Puerto: 5000
- Herramienta: `python app.py`

**Node 2: Frontend Dev Server**
- Sistema Operativo: Windows 10/11
- Runtime: Node.js 18
- Proceso: Vite Dev Server
- Puerto: 3000
- Herramienta: `npm run dev`

**Node 3: ngrok Tunnel**
- Herramienta: ngrok
- Función: Exponer puerto 5000 públicamente
- URL: `https://[random].ngrok.io`
- Protocolo: HTTPS

### Servicios Cloud (Desarrollo)

**MongoDB Atlas**
- Tier: M0 (Free)
- Región: AWS us-east-1
- Replica Set: 3 nodos
- Conexión: TLS/SSL
- IP Whitelist: 0.0.0.0/0 (all IPs)

**Twilio**
- Servicio: WhatsApp Sandbox
- Webhook URL: `https://[ngrok].ngrok.io/webhook/whatsapp`
- Método: POST
- Timeout: 15 segundos

**OpenAI API**
- Endpoint: `https://api.openai.com/v1/chat/completions`
- Modelo: gpt-3.5-turbo
- Rate Limit: 3 RPM (tier free)

---

## Deployment - Producción (Recomendado)

### Frontend

**Vercel**
- Tipo: Static Site Hosting
- Build Command: `npm run build`
- Output Directory: `dist`
- Framework Preset: Vite
- Dominio: `https://cafe-feedback.vercel.app`
- CDN: Edge Network global
- SSL: Automático (Let's Encrypt)

**Variables de Entorno:**
```
VITE_API_BASE_URL=https://cafe-backend.railway.app/api
```

### Backend

**Railway / Render**
- Tipo: Container-based deployment
- Runtime: Python 3.10
- Comando: `python app.py`
- Puerto: 5000 (auto-asignado)
- Dominio: `https://cafe-backend.railway.app`
- Auto-scaling: Horizontal
- Health Check: `GET /health`

**Variables de Entorno:**
```env
TWILIO_ACCOUNT_SID=***
TWILIO_AUTH_TOKEN=***
TWILIO_PHONE_NUMBER=***
MONGODB_URI=***
OPENAI_API_KEY=***
PORT=5000
FLASK_ENV=production
```

### Base de Datos

**MongoDB Atlas**
- Tier: M10 (Producción)
- Región: Multi-región
- Replica Set: 3 nodos
- Backup: Automático (snapshot diario)
- Monitoring: Atlas Charts
- IP Whitelist: Railway IP ranges

### Configuración Twilio (Producción)

**WhatsApp Business Account**
- Tipo: Approved sender
- Webhook URL: `https://cafe-backend.railway.app/webhook/whatsapp`
- Método: POST
- Failover: Retry 3 veces
- Status Callback: Habilitado

---

## Diagrama de Red (Producción)

```
Internet
   │
   ├──> [Vercel CDN] ──> React Frontend (Static Files)
   │         │
   │         └──> HTTPS ──> [Railway] Backend API
   │                              │
   │                              ├──> [MongoDB Atlas] (TLS)
   │                              │
   │                              └──> [OpenAI API] (HTTPS)
   │
   └──> [Twilio] ──HTTPS Webhook──> [Railway] Backend API
```

---

## Consideraciones de Seguridad

### Desarrollo
- ⚠️ Variables de entorno en `.env` (no commitear)
- ⚠️ ngrok expone localhost públicamente
- ⚠️ CORS habilitado para `*` (desarrollo)

### Producción
- ✅ Variables de entorno en Railway/Vercel
- ✅ HTTPS obligatorio (TLS 1.2+)
- ✅ CORS restringido a dominios específicos
- ✅ Validación de firma de Twilio
- ✅ Rate limiting en API
- ✅ Secrets en servicios manejados (no en código)
- ✅ MongoDB con autenticación SCRAM-SHA-256
- ✅ IP Whitelist en MongoDB Atlas

---

## Monitoreo y Logging

### Desarrollo
- Console logs en terminal
- MongoDB Atlas Charts (básico)

### Producción
- **Logs:** Railway Logs / Render Logs
- **Métricas:**
  - Request latency
  - Error rate
  - OpenAI API usage
  - MongoDB query performance
- **Alertas:**
  - Error rate > 5%
  - API latency > 2 segundos
  - OpenAI quota exceeded
- **Herramientas sugeridas:**
  - Sentry (error tracking)
  - DataDog (APM)
  - MongoDB Atlas Monitoring

---

## Escalabilidad

### Horizontal Scaling
- **Frontend:** Auto-scaling vía CDN (Vercel)
- **Backend:** Múltiples instancias en Railway/Render
- **Database:** MongoDB sharding (si >100GB datos)

### Vertical Scaling
- **Backend:** Aumentar RAM/CPU en Railway
- **Database:** Upgrade tier en MongoDB Atlas

### Caching (Futuro)
- Redis para caché de agregaciones
- TTL: 60 segundos

---

## Costos Estimados (Producción)

| Servicio | Tier | Costo Mensual |
|----------|------|---------------|
| Vercel | Hobby | $0 |
| Railway | Starter | $5 |
| MongoDB Atlas | M10 | $57 |
| OpenAI API | Pay-as-go | ~$10-30 |
| Twilio WhatsApp | Pay-as-go | ~$0.005/msg |
| **Total** | | **~$75-95/mes** |

---

## Instrucciones para Crear los Diagramas

### Usando draw.io

1. Ir a https://app.diagrams.net/
2. Crear nuevo diagrama
3. Para cada diagrama:
   - Usar formas "Cloud" para sistemas externos
   - Usar rectángulos para contenedores/componentes
   - Usar íconos de personas para actores
   - Usar flechas con etiquetas para relaciones
4. Exportar como PNG o SVG

### Colores Sugeridos
- **Actores:** Azul claro (#3B82F6)
- **Sistema principal:** Verde (#10B981)
- **Sistemas externos:** Gris (#6B7280)
- **Base de datos:** Naranja (#F59E0B)
- **Frontend:** Púrpura (#8B5CF6)
- **Backend:** Verde oscuro (#059669)

---

**Fin de especificaciones de Diagramas C4**
