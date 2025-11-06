"""
Provedor OLLAMA para LLM local
"""

from typing import Optional
import logging
import requests
from .base import LLMProvider, FallbackSummarizer


class OllamaProvider(LLMProvider):
    """Provedor OLLAMA (LLM local)"""
    
    def setup_provider(self, base_url: str = "http://localhost:11434", model: str = "llama2", **kwargs):
        """
        Configura o cliente OLLAMA
        
        Args:
            base_url: URL base do OLLAMA
            model: Modelo a ser usado
            **kwargs: Parâmetros adicionais
        """
        self.base_url = base_url
        self.model = model
        self.logger.info(f"OLLAMA Provider configurado com modelo: {model} em {base_url}")
    
    def summarize_text(self, texto: str, titulo: str, max_lines: int = 5) -> str:
        """
        Gera resumo usando OLLAMA
        
        Args:
            texto: Texto completo
            titulo: Título do documento
            max_lines: Número máximo de linhas
            
        Returns:
            Resumo formatado
        """
        try:
            max_chars = 8000  # Limite conservador para OLLAMA
            if len(texto) > max_chars:
                texto = texto[:max_chars] + "..."
            
            prompt = f"""Resuma o seguinte documento do Banco Central do Brasil em no máximo {max_lines} linhas concisas e objetivas. 
Foque nos pontos principais e impactos relevantes.

Título: {titulo}

Conteúdo:
{texto}

Resumo:"""
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "num_predict": 500
                    }
                },
                timeout=120
            )
            
            response.raise_for_status()
            result = response.json()
            resumo = result.get('response', '').strip()
            
            if not resumo:
                raise ValueError("Resposta vazia do OLLAMA")
            
            return self.format_summary(titulo, resumo, "")
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar resumo com OLLAMA: {str(e)}")
            fallback = FallbackSummarizer()
            resumo = fallback.summarize_text(texto, titulo, max_lines)
            return self.format_summary(titulo, resumo, "")

