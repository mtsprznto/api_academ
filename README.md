# API Académica - Transcripción y Análisis de Videos

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Supabase](https://img.shields.io/badge/Supabase-181818?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)

API desarrollada en FastAPI que permite transcribir y analizar contenido de videos, con integración a Supabase para el almacenamiento de transcripciones y respuestas generadas por IA.

## Características Principales

- 🎥 Transcripción automática de videos de YouTube
- 💬 Chat con IA para realizar consultas sobre el contenido de los videos
- 🗄️ Almacenamiento seguro de transcripciones en Supabase
- 🔍 Búsqueda de información específica dentro de los videos
- 🚀 API RESTful con documentación automática

## Tecnologías Utilizadas

- **Backend**: FastAPI
- **Base de Datos**: Supabase (PostgreSQL)
- **Procesamiento de Lenguaje**: Groq
- **Variables de Entorno**: python-dotenv
- **Hosting**: Vercel (configuración incluida)

## Requisitos Previos

- Python 3.8 o superior
- Cuenta en [Supabase](https://supabase.com/)
- Cuenta en [Groq](https://groq.com/)
- Git

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/mtsprznto/api_academ.git
   cd api_academ
   ```

2. Crea y activa un entorno virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: .\venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Configuración del Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```
SUPABASE_URL=key
SUPABASE_KEY=key
GROQ_API_KEY=key
GROK_API_KEY_RESPONSE=key
NEON_DATABASE_URL=key
```

## Estructura del Proyecto

```
api_academ/
├── api/
│   ├── audio_temp/          # Archivos de audio temporales
│   ├── data_url/            # URLs de videos a procesar
│   ├── main.py              # Aplicación principal FastAPI
│   ├── guardar_db.py        # Funciones para guardar en Supabase
│   └── extraer_text_update.py # Procesamiento de transcripciones
├── requirements.txt         # Dependencias del proyecto
└── vercel.json             # Configuración de despliegue en Vercel
```

## Uso

### Iniciar el servidor de desarrollo:

```bash
fastapi dev .\api\main.py
```

La documentación interactiva de la API estará disponible en:
- Documentación Swagger: http://localhost:8000/docs
- Documentación ReDoc: http://localhost:8000/redoc

### Endpoints Principales

#### 1. Chat con Video
```
POST /api/chat/video
```
Envía un mensaje sobre el contenido de un video específico.

**Cuerpo de la petición:**
```json
{
  "userId": "id_del_usuario",
  "courseSlug": "slug_del_curso",
  "chapterId": "id_del_capitulo",
  "videoUrl": "url_del_video",
  "userMessage": "Tu pregunta sobre el video"
}
```

#### 2. Obtener información de un video
```
GET /video/{video_id}
```
Obtiene la información de un video específico por su ID.

## Despliegue

El proyecto incluye configuración para Vercel. Para desplegar:

1. Instala Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Inicia sesión en Vercel:
   ```bash
   vercel login
   ```

3. Configura las variables de entorno en el dashboard de Vercel

4. Despliega:
   ```bash
   vercel --prod
   ```

## Contribución

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Haz un fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Haz commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Haz push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Distribuido bajo la licencia MIT. Ver `LICENSE` para más información.

## Contacto

Tu Nombre - [@tu_twitter](https://twitter.com/tu_twitter)

Enlace del Proyecto: [https://github.com/tu-usuario/api_academ](https://github.com/tu-usuario/api_academ)
