"""
Provedor OpenAI para LLM
"""

from typing import Optional
import logging
from .base import LLMProvider, FallbackSummarizer

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class OpenAIProvider(LLMProvider):
    """Provedor OpenAI (GPT-3.5, GPT-4, etc.)"""
    
    def setup_provider(self, model: str = "gpt-3.5-turbo", **kwargs):
        """
        Configura o cliente OpenAI
        
        Args:
            model: Modelo a ser usado (gpt-3.5-turbo, gpt-4, etc.)
            **kwargs: Parâmetros adicionais
        """
        if not OPENAI_AVAILABLE:
            raise ImportError("Biblioteca openai não está instalada. Execute: pip install openai")
        
        if not self.api_key:
            raise ValueError("API Key do OpenAI não fornecida")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.logger.info(f"OpenAI Provider configurado com modelo: {model}")
    
    def summarize_text(self, texto: str, titulo: str, max_lines: int = 5) -> str:
        """
        Gera resumo usando OpenAI
        
        Args:
            texto: Texto completo
            titulo: Título do documento
            max_lines: Número máximo de linhas
            
        Returns:
            Resumo formatado
        """
        try:
            # Trunca texto se muito longo (limite de tokens)
            max_chars = 12000  # Aproximadamente 3000 tokens
            if len(texto) > max_chars:
                texto = texto[:max_chars] + "..."
            
            prompt = f"""Resuma o seguinte documento do Banco Central do Brasil em no máximo {max_lines} linhas concisas e objetivas. 
Foque nos pontos principais e impactos relevantes.

Título: {titulo}

Conteúdo:
{texto}

Resumo:"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um assistente especializado em resumir documentos regulatórios do Banco Central do Brasil."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            resumo = response.choices[0].message.content.strip()
            return self.format_summary(titulo, resumo, "")
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar resumo com OpenAI: {str(e)}")
            # Fallback para sumarizador simples
            fallback = FallbackSummarizer()
            resumo = fallback.summarize_text(texto, titulo, max_lines)
            return self.format_summary(titulo, resumo, "")

