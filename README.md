# Chatbot Balanzas

Chatbot de WhatsApp para una fábrica argentina de balanzas e instrumentos de pesaje industrial.  
Captura consultas de clientes (ventas, servicio técnico, calibración/ISO) y las clasifica con IA para derivarlas al área correspondiente.

## Stack

- **Backend:** FastAPI + Python 3.11
- **IA:** Google Gemini 2.0 Flash (Structured Outputs)
- **Base de datos:** SQLite (SQLAlchemy 2.x)
- **Canal:** WhatsApp vía Twilio Sandbox
- **Despliegue local:** Uvicorn + Ngrok

## Instalación

```bash
# 1. Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
copy .env.example .env
# Editá .env y poné tu GEMINI_API_KEY

# 4. Iniciar servidor
uvicorn main:app --reload --port 8000
```

## Variables de entorno

Copiá `.env.example` como `.env` y completá:

| Variable | Descripción |
|---|---|
| `GEMINI_API_KEY` | Clave de Google AI Studio ([obtener aquí](https://aistudio.google.com/app/apikey)) |
| `APP_SECRET_KEY` | Clave secreta de la app (cambiala en producción) |

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/chat` | API REST para pruebas |
| `POST` | `/whatsapp` | Webhook de Twilio (WhatsApp) |

## Prueba rápida (local + WhatsApp)

```powershell
# Terminal 1 — servidor
uvicorn main:app --reload --port 8000

# Terminal 2 — túnel público
& "ruta\a\ngrok.exe" http 8000
```

Configurá la URL HTTPS de Ngrok en el **Sandbox de Twilio** como webhook del `/whatsapp`.

## Subir cambios a GitHub

```powershell
# Windows
.\subir-cambios-windows.ps1 "descripcion de los cambios"
```

```bash
# Mac / Linux
./subir-cambios-mac.sh "descripcion de los cambios"
```
