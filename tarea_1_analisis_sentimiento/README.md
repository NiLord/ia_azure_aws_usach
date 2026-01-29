# Azure Cognitive Services Language - Cliente Python

Cliente en Python para análisis de sentimiento usando el **SDK oficial de Azure Text Analytics**.

## Características

- ✅ Usa el SDK oficial `azure-ai-textanalytics`
- ✅ Autenticación con AzureKeyCredential
- ✅ Manejo automático de errores y reintentos
- ✅ Análisis de sentimiento por documento y por oración
- ✅ Soporte para múltiples idiomas
- ✅ Carga de frases desde archivo YAML

## Instalación

```bash
pip install -r requirements.txt
```

## Configuración

1. Copia el archivo de entorno:
```bash
cp .env.template .env
```

2. Edita el archivo `.env` con tus credenciales:
```env
AZURE_FOUNDRY_API_KEY=tu_subscription_key
AZURE_FOUNDRY_ENDPOINT=https://tu-recurso.cognitiveservices.azure.com
```

## Uso

### Ejemplo Básico

```python
from azure_foundry_client import AzureSentimentClient

# Inicializar el cliente
client = AzureSentimentClient()

# Análisis simple
documents = ["I love this product!", "This is terrible."]
results = client.analyze_sentiment(documents, language="en")

for result in results:
    print(f"Sentimiento: {result.sentiment}")
    print(f"Confianza: Positivo={result.confidence_scores.positive:.2f}")
```

### Ejemplo con IDs Personalizados

```python
documents = [
    {"id": "1", "text": "Great service!", "language": "en"},
    {"id": "2", "text": "Bad experience.", "language": "en"}
]

results = client.analyze_sentiment_batch(documents)

for result in results:
    if not result.is_error:
        print(f"ID: {result.id}, Sentimiento: {result.sentiment}")
```

## Ejemplos Incluidos

El archivo `main.py` analiza 16 frases de sentimiento cargadas desde `sentiment_examples.yml`:

- ✅ **Frases Positivas** - 4 ejemplos
- ✅ **Frases Negativas** - 4 ejemplos
- ✅ **Frases Neutrales** - 4 ejemplos
- ✅ **Frases Mixtas/Complejas** - 4 ejemplos (sarcasmo, conflicto, matices)

### Ejecutar el análisis

1. Crear y activar un entorno virtual:

```bash
# Crear el entorno virtual
python -m venv .venv

# Activar el entorno virtual
# En macOS/Linux:
source .venv/bin/activate

# En Windows:
.venv\Scripts\activate
```

2. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutar el análisis:

```bash
python main.py
```

### Personalizar las frases

Edita el archivo `sentiment_examples.yml` para agregar o modificar las frases a analizar.