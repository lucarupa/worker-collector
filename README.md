# worker-collector

Microservicio de recolección y normalización de datos. Consume tareas desde Kafka, ejecuta estrategias de recolección (API o scraping), normaliza los resultados según reglas configurables en MongoDB y publica los resultados.

## Tecnologías

- **Python** + **FastAPI** — framework principal y API HTTP
- **Apache Kafka** (aiokafka) — mensajería asíncrona para disparar y reportar ejecuciones
- **MongoDB** (pymongo) — almacenamiento de configuraciones y resultados
- **Pydantic** — validación de modelos y configuración por variables de entorno
- **injector** — inyección de dependencias

## Arquitectura

El sistema implementa tres patrones principales:

- **Strategy** — selección dinámica entre estrategia API y Scrapper según el mensaje recibido
- **Repository** — acceso a configuraciones (API, Scrapper, normalizaciones, operadores) desacoplado de la lógica de negocio
- **Pipeline** — flujo lineal: `Processor → Normalization → Operator`

```
Kafka Consumer
     │
     ▼
CollectorAdapter          ← selecciona estrategia (API | Scrapper)
     │
     ▼
StrategyModel.execute()
  ├── _run_processor()    ← recolección de datos
  ├── _run_normalization() ← transformación
  └── _run_operator()     ← aplicación de expresiones/operadores
     │
     ▼
Kafka Producer            ← publica resultado
```

## Estructura del proyecto

```
app/
├── adapter/
│   ├── __init__.py              # CollectorAdapter — orquestador principal
│   ├── model/                   # StrategyModel — clase base abstracta del pipeline
│   ├── implementations/         # ApiImplementations, ScrapperImplementations
│   └── interface/               # StrategyInterface genérico
├── core/
│   ├── Enum/                    # Tipos de ejecución, reportes y códigos de error
│   ├── interface/               # Modelos Pydantic (configs, normalización, operadores)
│   ├── repositories/            # Repositorios para cada tipo de configuración
│   └── const/                   # Constantes y factories
├── services/
│   ├── kafka/                   # Consumer y Producer
│   ├── implementations/         # Implementación MongoDB
│   ├── model/                   # Interfaz abstracta de base de datos
│   ├── database_injection.py    # Módulo DI para base de datos
│   └── repositories_injection.py # Módulo DI para repositorios
├── routes/                      # Endpoints FastAPI
├── utils/                       # Logger con salida coloreada
└── exections/                   # Excepciones personalizadas
main.py                          # App factory con lifespan (arranque/apagado graceful)
```

## Configuración

El servicio se configura exclusivamente mediante variables de entorno (soporta archivo `.env`).

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `MONGO_CONNECTION_STRING` | URI de conexión a MongoDB | `mongodb://user:pass@host:27017` |
| `MONGO_DATABASE` | Nombre de la base de datos | `collector_db` |
| `KAFKA_BOOTSTRAP_SERVERS` | Brokers de Kafka | `localhost:9092` |
| `KAFKA_TOPIC_CONSUMER` | Topic de entrada (tareas) | `collector_tasks` |
| `KAFKA_TOPIC_PRODUCER` | Topic de salida (resultados) | `collector_results` |
| `KAFKA_GROUP_ID` | Consumer group | `worker-collector` |
| `SENTRY_DSN` | DSN de Sentry para error tracking | *(opcional)* |

### Colecciones requeridas en MongoDB

| Colección | Contenido |
|-----------|-----------|
| `api_config` | Configuraciones de endpoints API |
| `scrapper_config` | Configuraciones de scrapers |
| `normalizations` | Reglas de normalización de datos |
| `operators` | Expresiones y operadores de transformación |

## Instalación y ejecución

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# editar .env con tus valores

# Iniciar el servidor
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/ready` | Health check |
| `POST` | `/start-scrapper` | Dispara una ejecución de forma síncrona |

## Notas de diseño

- El consumer de Kafka filtra mensajes por el header `collector` antes de procesarlos.
- Un `asyncio.Semaphore(1)` garantiza ejecución secuencial: solo una tarea corre a la vez.
- El apagado del servicio cancela gracefully las tareas activas de Kafka.
