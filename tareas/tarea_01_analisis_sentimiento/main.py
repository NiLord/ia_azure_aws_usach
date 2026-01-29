#!/usr/bin/env python3
"""
Ejemplos de uso del cliente de Azure Cognitive Services Language usando el SDK oficial
"""

from azure_foundry_client import AzureSentimentClient
import yaml
import os

def cargar_frases_desde_yaml(archivo='sentiment_examples.yml'):
    """
    Carga las frases de ejemplo desde un archivo YAML
    """
    ruta_archivo = os.path.join(os.path.dirname(__file__), archivo)
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def ejemplo_analisis_sentimiento():
    """
    Ejemplo de análisis de sentimiento usando frases del archivo YAML
    """
    client = AzureSentimentClient()
    
    try:
        frases = cargar_frases_desde_yaml()
        
        documents = []
        doc_id = 1
        
        for categoria, textos in frases.items():
            print(f"\n{'='*60}")
            print(f"Cargando frases de la categoría: {categoria.upper()}")
            print('='*60)
            
            for item in textos:
                if isinstance(item, dict):
                    texto = item.get('text', '')
                    idioma = item.get('language', 'en')
                else:
                    texto = item
                    idioma = 'en'
                
                documents.append({
                    "id": str(doc_id),
                    "text": texto,
                    "language": idioma
                })
                doc_id += 1
        
        print("\n" + "="*60)
        print("RESULTADOS DEL ANÁLISIS DE SENTIMIENTO")
        print("="*60 + "\n")
        
        results = client.analyze_sentiment_batch(documents)
        
        for idx, result in enumerate(results):
            if not result.is_error:
                doc = documents[idx]
                
                print(f"ID: {result.id}")
                print(f"Idioma: {doc['language'].upper()}")
                print(f"Texto: {doc['text']}")
                print(f"Sentimiento detectado: {result.sentiment.upper()}")
                print(f"Confianza - Positivo: {result.confidence_scores.positive:.2f}, "
                      f"Neutral: {result.confidence_scores.neutral:.2f}, "
                      f"Negativo: {result.confidence_scores.negative:.2f}")
                
                if result.sentences:
                    print(f"Análisis por oración:")
                    for sentence in result.sentences:
                        print(f"  - '{sentence.text[:50]}...' -> {sentence.sentiment}")
                
                print("-" * 60)
            else:
                print(f"Error en documento {result.id}: {result.error.message}")
                print("-" * 60)
        
        print(f"\nTotal de frases analizadas: {len([r for r in results if not r.is_error])}")
        
    except FileNotFoundError:
        print("Error: No se encontró el archivo sentiment_examples.yml")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ejemplo_analisis_sentimiento()
