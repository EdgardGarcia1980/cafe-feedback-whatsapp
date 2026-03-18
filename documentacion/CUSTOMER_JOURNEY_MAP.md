# Customer Journey Map - Dashboard de Sentimiento del Cliente

## Overview

Este mapa documenta el recorrido completo del cliente desde que visita el café hasta que su feedback se refleja en el dashboard del gerente.

---

## Journey End-to-End

```
Cliente visita → Experiencia → Invitación → Envía feedback → Sistema procesa →
→ IA analiza → Datos almacenados → Dashboard actualiza → Gerente visualiza → Acción
```

---

## Fases Detalladas

### FASE 1: Experiencia en el Café
**Duración:** 15-45 minutos

**Actor:** Cliente

**Actividades:**
- Cliente llega al café
- Realiza pedido
- Consume productos
- Recibe servicio
- Experimenta el ambiente

**Touchpoints:**
- Personal de servicio
- Calidad del producto
- Limpieza del establecimiento
- Precio pagado
- Ambiente general

**Emociones:**
- 😊 Satisfecho si la experiencia es positiva
- 😐 Neutral si es promedio
- 😞 Insatisfecho si hay problemas

**Pain Points Potenciales:**
- Tiempo de espera largo
- Producto no cumple expectativas
- Servicio descortés
- Limpieza deficiente
- Precio elevado

---

### FASE 2: Invitación a Dar Feedback
**Duración:** 30 segundos - 1 minuto

**Actor:** Cliente + Personal del Café

**Actividades:**
- Cliente recibe ticket/factura con QR o número de WhatsApp
- O mesero invita verbalmente a enviar feedback
- Cliente ve mensaje: "Comparte tu experiencia vía WhatsApp al +1234567890"

**Touchpoints:**
- Ticket impreso con QR
- Cartel en mesa
- Invitación verbal
- Post en redes sociales

**Canales:**
- QR code → WhatsApp
- Número directo
- Link en redes sociales

**Emociones:**
- 🤔 Considera si vale la pena compartir
- 💭 Recuerda su experiencia

**Barreras:**
- Falta de tiempo
- Pereza de escribir
- No ve beneficio inmediato
- Preocupación por privacidad

**Motivadores:**
- Experiencia muy buena (quiere elogiar)
- Experiencia muy mala (quiere quejarse)
- Incentivo (descuento en próxima visita)
- Facilidad del proceso (solo WhatsApp)

---

### FASE 3: Cliente Envía Mensaje por WhatsApp
**Duración:** 1-3 minutos

**Actor:** Cliente

**Actividades:**
1. Cliente abre WhatsApp
2. Escanea QR o guarda número
3. Redacta mensaje de feedback
4. Envía mensaje

**Ejemplo de Mensajes:**

**Positivo:**
```
"Excelente café! El servicio fue rápido y la
atención muy amable. Definitivamente regresaré 👍"
```

**Negativo:**
```
"El café estaba frío y tardaron mucho en
atenderme. Además el baño estaba sucio."
```

**Neutro:**
```
"Buen café pero un poco caro para el tamaño
de la taza. El lugar es bonito."
```

**Dispositivo:** Smartphone (WhatsApp)

**Emociones:**
- 😊 Satisfecho de compartir opinión positiva
- 😤 Frustrado al reportar experiencia negativa
- 😐 Neutral, solo informa

**Expectativas:**
- Que su mensaje sea leído
- Que se tome en cuenta
- (Ideal) Que haya respuesta o agradecimiento

---

### FASE 4: Sistema Recibe el Mensaje
**Duración:** < 1 segundo

**Sistema:** WhatsApp → Twilio

**Actividades:**
1. WhatsApp recibe el mensaje
2. WhatsApp reenvía a Twilio API
3. Twilio procesa el mensaje
4. Twilio prepara webhook

**Tecnología:**
- WhatsApp Business API
- Twilio Messaging Service
- HTTPS protocol

**Datos Capturados:**
- Texto del mensaje (`Body`)
- Número del remitente (`From`)
- Timestamp
- Message SID (identificador único)

**Emociones del Cliente:**
- ✅ Mensaje enviado, espera confirmación

---

### FASE 5: Backend Procesa el Mensaje
**Duración:** 1-3 segundos

**Sistema:** Twilio → Backend Flask

**Actividades:**
1. Twilio envía POST request al webhook
2. Backend recibe request en `/webhook/whatsapp`
3. Webhook Controller extrae datos
4. Database Service guarda mensaje en MongoDB

**Endpoint:** `POST /webhook/whatsapp`

**Datos Guardados en MongoDB:**
```json
{
  "texto_mensaje": "Excelente café!...",
  "numero_remitente": "whatsapp:+503XXXXXXXX",
  "timestamp": "2024-03-18T14:30:00Z",
  "sentimiento": null,
  "tema": null,
  "resumen": null,
  "metadatos": {}
}
```

**Logging:**
```
📩 Mensaje recibido:
   De: whatsapp:+503XXXXXXXX
   Texto: Excelente café! El servicio...
💾 Mensaje guardado con ID: 65f8a2b4c3d1e2f3a4b5c6d7
```

---

### FASE 6: IA Analiza el Sentimiento
**Duración:** 2-5 segundos

**Sistema:** Backend → OpenAI API

**Actividades:**
1. AI Service construye el prompt con Few-shot examples
2. Envía request a OpenAI API (gpt-3.5-turbo)
3. OpenAI procesa y analiza el texto
4. Retorna JSON con análisis
5. Backend valida el formato JSON
6. Backend extrae: sentimiento, tema, resumen

**Prompt Enviado:**
```
Eres un analista de sentimientos para un café...

Ejemplos:
[4 ejemplos de mensajes con sus análisis]

Mensaje a analizar: "Excelente café! El servicio..."
```

**Respuesta de OpenAI:**
```json
{
  "sentimiento": "positivo",
  "tema": "Servicio al Cliente",
  "resumen": "Cliente muy satisfecho con calidad del café y rapidez del servicio"
}
```

**Metadatos Generados:**
```json
{
  "modelo_id": "gpt-3.5-turbo",
  "latencia_ms": 2340,
  "version_prompt": "1.0",
  "tokens_used": 156
}
```

**Logging:**
```
🤖 Analizando con IA...
✅ Análisis completado:
   Sentimiento: positivo
   Tema: Servicio al Cliente
   Resumen: Cliente muy satisfecho...
   Latencia: 2340ms
```

---

### FASE 7: Actualización de Base de Datos
**Duración:** < 500ms

**Sistema:** Backend → MongoDB

**Actividades:**
1. Database Service actualiza el documento
2. Agrega campos: sentimiento, tema, resumen, metadatos
3. MongoDB confirma actualización

**Documento Actualizado:**
```json
{
  "_id": "65f8a2b4c3d1e2f3a4b5c6d7",
  "texto_mensaje": "Excelente café!...",
  "numero_remitente": "whatsapp:+503XXXXXXXX",
  "timestamp": "2024-03-18T14:30:00Z",
  "sentimiento": "positivo",
  "tema": "Servicio al Cliente",
  "resumen": "Cliente muy satisfecho...",
  "metadatos": {
    "modelo_id": "gpt-3.5-turbo",
    "latencia_ms": 2340,
    "version_prompt": "1.0",
    "tokens_used": 156
  }
}
```

**Estado:** ✅ Mensaje completamente procesado

---

### FASE 8: Dashboard se Actualiza
**Duración:** 0-10 segundos (siguiente ciclo de polling)

**Sistema:** React Frontend

**Actividades:**
1. Frontend hace polling cada 10 segundos
2. Llama a endpoints de la API:
   - `GET /api/sentimientos`
   - `GET /api/temas`
   - `GET /api/mensajes-recientes`
   - `GET /api/stats`
3. Recibe datos actualizados
4. Re-renderiza componentes
5. Gráficos se actualizan
6. Nuevo mensaje aparece en el feed

**Componentes Actualizados:**
- 📊 StatsCard: Total mensajes +1
- 📈 SentimentChart: Positivos +1
- 📊 TopicsChart: Servicio al Cliente +1
- 💬 MessageFeed: Nuevo mensaje en el top

**UI Changes:**
```
Total de Mensajes: 23 → 24
Tasa de Satisfacción: 65.2% → 66.7%
Feed: [NUEVO] "Excelente café! El servicio..."
```

---

### FASE 9: Gerente Visualiza los Datos
**Duración:** Continuo

**Actor:** Gerente del Café

**Actividades:**
1. Gerente abre el dashboard en su navegador
2. Revisa las tarjetas de estadísticas
3. Analiza el gráfico de sentimientos
4. Revisa los temas más mencionados
5. Lee los mensajes recientes
6. Identifica patrones y tendencias

**Dispositivo:**
- Desktop: Oficina del gerente
- Tablet/Mobile: Mientras atiende el café

**Información Visible:**
- **Stats Cards:**
  - Total de mensajes: 24
  - Tasa de satisfacción: 66.7%
  - Tema principal: Servicio al Cliente

- **Gráfico de Pastel:**
  - Positivo: 16 (66.7%) - Verde
  - Neutro: 5 (20.8%) - Gris
  - Negativo: 3 (12.5%) - Rojo

- **Gráfico de Barras:**
  - Servicio al Cliente: 10
  - Calidad del Producto: 8
  - Precio: 3
  - Limpieza: 2
  - Otro: 1

- **Feed de Mensajes:**
  - [NUEVO] "Excelente café! El servicio..."
  - Sentimiento: positivo
  - Tema: Servicio al Cliente
  - Timestamp: Hace 30 segundos

**Emociones:**
- 😊 Satisfecho al ver feedback positivo
- 🤔 Analítico al identificar patrones
- 😟 Preocupado al ver feedback negativo
- 💡 Inspirado para tomar acción

---

### FASE 10: Gerente Toma Decisión
**Duración:** Variable (inmediato a días)

**Actor:** Gerente del Café

**Actividades:**
1. Analiza tendencias
2. Identifica problemas recurrentes
3. Identifica fortalezas
4. Toma decisiones basadas en datos
5. Implementa cambios

**Tipos de Decisiones:**

#### A) Decisiones Inmediatas (Operacionales)
**Trigger:** Múltiples mensajes negativos sobre limpieza en 1 día

**Acción:**
- Inspeccionar baños inmediatamente
- Reforzar limpieza durante el día
- Asignar persona dedicada a limpieza

**Ejemplo:**
```
Dashboard muestra:
- 3 mensajes negativos sobre limpieza hoy
- Tema "Limpieza": Sentimiento 100% negativo

Gerente:
→ Inspecciona baños
→ Encuentra problema (falta jabón)
→ Solución inmediata
→ Refuerza protocolo
```

#### B) Decisiones Tácticas (Semanales)
**Trigger:** Tendencia de quejas sobre precios durante 1 semana

**Acción:**
- Analizar pricing strategy
- Comparar con competencia
- Considerar promociones
- Ajustar tamaños de porciones

**Ejemplo:**
```
Dashboard muestra:
- 15 mensajes mencionan "caro" en 7 días
- Tema "Precio": 60% negativo

Gerente:
→ Revisa costos
→ Crea combo promocional
→ Ofrece descuento en horario bajo
```

#### C) Decisiones Estratégicas (Mensuales)
**Trigger:** Patrones consistentes en 30 días

**Acción:**
- Capacitación del personal
- Cambio de proveedores
- Inversión en infraestructura
- Expansión de menú

**Ejemplo:**
```
Dashboard muestra (30 días):
- "Servicio al Cliente": 70% positivo
- "Calidad del Producto": 85% positivo
- "Limpieza": 40% negativo consistente

Gerente:
→ Reconoce al personal (servicio)
→ Mantiene proveedor de café (calidad)
→ Invierte en mejora de baños (limpieza)
→ Contrata personal de limpieza adicional
```

---

## Touchpoints Resumidos

| Fase | Actor | Touchpoint | Sistema |
|------|-------|-----------|---------|
| 1 | Cliente | Café físico | - |
| 2 | Cliente + Staff | QR / Invitación | - |
| 3 | Cliente | WhatsApp | WhatsApp App |
| 4 | - | - | WhatsApp → Twilio |
| 5 | - | - | Twilio → Backend |
| 6 | - | - | Backend → OpenAI |
| 7 | - | - | Backend → MongoDB |
| 8 | - | - | Backend → Frontend |
| 9 | Gerente | Dashboard Web | Frontend |
| 10 | Gerente | Acción en Café | - |

---

## Métricas Clave del Journey

| Métrica | Objetivo | Actual |
|---------|----------|--------|
| Tiempo total (Fase 3 → Fase 8) | < 15 seg | ~8-12 seg |
| Tasa de conversión (visita → feedback) | > 5% | 3-8% |
| Latencia de IA | < 3 seg | ~2-3 seg |
| Actualización dashboard | < 15 seg | 10 seg |
| Precisión de análisis IA | > 90% | ~85-95% |

---

## Mejoras Futuras

### Corto Plazo
1. **Respuesta automática:**
   - WhatsApp responde: "Gracias por tu feedback!"
   - Aumenta satisfacción del cliente

2. **Notificaciones push:**
   - Gerente recibe alerta de feedback negativo
   - Acción inmediata

### Mediano Plazo
3. **Análisis de tendencias:**
   - Gráficos de evolución temporal
   - Comparación semana/mes

4. **Exportar reportes:**
   - PDF/Excel con estadísticas
   - Para reuniones gerenciales

### Largo Plazo
5. **Machine Learning:**
   - Predicción de satisfacción
   - Detección de anomalías

6. **Integración CRM:**
   - Identificar clientes frecuentes
   - Personalizar respuestas

---

## Pain Points y Oportunidades

### Pain Points Identificados

**Cliente:**
- ❌ No recibe confirmación inmediata de que su mensaje fue leído
- ❌ No ve acción visible basada en su feedback

**Gerente:**
- ❌ Delay de hasta 10 segundos para ver nuevos mensajes
- ❌ No hay alertas proactivas para problemas urgentes
- ❌ No puede responder directamente al cliente

### Oportunidades de Mejora

1. **Auto-respuesta en WhatsApp**
   - Mejora percepción del cliente
   - Cierra el loop de comunicación

2. **Alertas en tiempo real**
   - Push notifications para gerente
   - SMS/Email para problemas críticos

3. **Respuestas personalizadas**
   - Gerente puede responder desde dashboard
   - Muestra que se valora el feedback

4. **Gamificación**
   - Incentivos por dar feedback
   - Descuentos en próxima visita

---

**Fin del Customer Journey Map**
