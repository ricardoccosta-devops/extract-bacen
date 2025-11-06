"""
Provedor Anthropic (Claude) para LLM
"""

from typing import Optional
import logging
from .base import LLMProvider, FallbackSummarizer

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class ClaudeProvider(LLMProvider):
    """Provedor Anthropic Claude"""
    
    def setup_provider(self, model: str = "claude-3-sonnet-20240229", **kwargs):
        """
        Configura o cliente Anthropic
        
        Args:
            model: Modelo Claude a ser usado
            **kwargs: Parâmetros adicionais
        """
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("Biblioteca anthropic não está instalada. Execute: pip install anthropic")
        
        if not self.api_key:
            raise ValueError("API Key do Anthropic não fornecida")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model
        self.logger.info(f"Anthropic Provider configurado com modelo: {model}")
    
    def summarize_text(self, texto: str, titulo: str, max_lines: int = 5) -> str:
        """
        Gera resumo usando Claude
        
        Args:
            texto: Texto completo
            titulo: Título do documento
            max_lines: Número máximo de linhas
            
        Returns:
            Resumo formatado
        """
        try:
            max_chars = 200000  # Claude aceita textos maiores
            if len(texto) > max_chars:
                texto = texto[:max_chars] + "..."
            
            prompt = f"""Resuma o seguinte documento do Banco Central do Brasil em no máximo {max_lines} linhas concisas e objetivas. 
Foque nos pontos principais e impactos relevantes.

Título: {titulo}

Conteúdo:
{texto}

Resumo:"""
            
            message = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                temperature=0.3,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            resumo = message.content[0].text.strip()
            return self.format_summary(titulo, resumo, "")
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar resumo com Claude: {str(e)}")
            fallback = FallbackSummarizer()
            resumo = fallback.summarize_text(texto, titulo, max_lines)
            return self.format_summary(titulo, resumo, "")

