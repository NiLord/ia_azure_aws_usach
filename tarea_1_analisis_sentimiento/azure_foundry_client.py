import os
from typing import List, Optional
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient, AnalyzeSentimentResult, TextDocumentInput

class AzureSentimentClient:
    """
    Cliente para análisis de sentimiento usando el SDK oficial de Azure Text Analytics
    """
    
    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None):
        """
        Inicializa el cliente de Azure Text Analytics
        
        Args:
            api_key: API key para autenticación
            endpoint: Endpoint de Azure Cognitive Services
        """
        load_dotenv()
        
        self.api_key = api_key or os.getenv('AZURE_FOUNDRY_API_KEY')
        self.endpoint = endpoint or os.getenv('AZURE_FOUNDRY_ENDPOINT')
        
        if not self.api_key or not self.endpoint:
            raise ValueError("Se requiere API key y endpoint. Configúralos en .env o como parámetros")
        
        credential = AzureKeyCredential(self.api_key)
        self.client = TextAnalyticsClient(endpoint=self.endpoint, credential=credential)
    
    def analyze_sentiment(self, documents: List[str], language: str = "en") -> List[AnalyzeSentimentResult]:
        """
        Analiza el sentimiento de una lista de documentos
        
        Args:
            documents: Lista de textos a analizar
            language: Código de idioma (por defecto "en")
            
        Returns:
            Lista de resultados de análisis de sentimiento
        """
        return self.client.analyze_sentiment(documents=documents, language=language)
    
    def analyze_sentiment_batch(self, documents: List[dict]) -> List[AnalyzeSentimentResult]:
        """
        Analiza el sentimiento de documentos con IDs personalizados
        Divide automáticamente en lotes de 10 documentos (límite de Azure)
        
        Args:
            documents: Lista de diccionarios con 'id', 'text' y 'language'
            
        Returns:
            Lista de resultados de análisis de sentimiento
        """
        
        text_documents = [
            TextDocumentInput(id=doc['id'], text=doc['text'], language=doc.get('language', 'en'))
            for doc in documents
        ]
        
        batch_size = 10
        all_results = []
        
        for i in range(0, len(text_documents), batch_size):
            batch = text_documents[i:i + batch_size]
            results = self.client.analyze_sentiment(documents=batch)
            all_results.extend(results)
        
        return all_results
