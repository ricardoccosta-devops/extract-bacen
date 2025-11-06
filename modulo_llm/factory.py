"""
Factory e gerenciador de provedores LLM
"""

import os
import logging
from typing import Optional, Dict, Type
from .base import LLMProvider, FallbackSummarizer
from .openai_provider import OpenAIProvider
from .claude_provider import ClaudeProvider
from .ollama_provider import OllamaProvider


class LLMProviderFactory:
    """Factory para criar instâncias de provedores LLM"""
    
    _providers: Dict[str, Type[LLMProvider]] = {
        'openai': OpenAIProvider,
        'claude': ClaudeProvider,
        'anthropic': ClaudeProvider,  # Alias
        'ollama': OllamaProvider,
    }
    
    @classmethod
    def create_provider(
        cls,
        provider_name: str,
        api_key: Optional[str] = None,
        **kwargs
    ) -> LLMProvider:
        """
        Cria uma instância do provedor LLM
        
        Args:
            provider_name: Nome do provedor (openai, claude, ollama)
            api_key: Chave da API
            **kwargs: Parâmetros adicionais específicos do provedor
            
        Returns:
            Instância do provedor LLM
            
        Raises:
            ValueError: Se o provedor não for suportado
        """
        provider_name = provider_name.lower()
        
        if provider_name not in cls._providers:
            raise ValueError(
                f"Provedor '{provider_name}' não suportado. "
                f"Provedores disponíveis: {', '.join(cls._providers.keys())}"
            )
        
        provider_class = cls._providers[provider_name]
        
        try:
            return provider_class(api_key=api_key, **kwargs)
        except Exception as e:
            logging.error(f"Erro ao criar provedor {provider_name}: {str(e)}")
            # Retorna fallback se houver erro
            return FallbackLLMProvider()
    
    @classmethod
    def register_provider(cls, name: str, provider_class: Type[LLMProvider]):
        """
        Registra um novo provedor
        
        Args:
            name: Nome do provedor
            provider_class: Classe do provedor
        """
        cls._providers[name.lower()] = provider_class


class FallbackLLMProvider(LLMProvider):
    """Provedor de fallback que usa sumarização simples"""
    
    def setup_provider(self, **kwargs):
        """Configuração vazia para fallback"""
        self.logger.warning("Usando sumarizador de fallback (sem LLM)")
    
    def summarize_text(self, texto: str, titulo: str, max_lines: int = 5) -> str:
        """
        Gera resumo usando método simples
        
        Args:
            texto: Texto completo
            titulo: Título do documento
            max_lines: Número máximo de linhas
            
        Returns:
            Resumo formatado
        """
        fallback = FallbackSummarizer()
        resumo = fallback.summarize_text(texto, titulo, max_lines)
        return self.format_summary(titulo, resumo, "")


class LLMManager:
    """Gerenciador centralizado de LLM"""
    
    def __init__(self, provider_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Inicializa o gerenciador LLM
        
        Args:
            provider_name: Nome do provedor
            api_key: Chave da API
            **kwargs: Parâmetros adicionais
        """
        self.provider = LLMProviderFactory.create_provider(
            provider_name,
            api_key=api_key,
            **kwargs
        )
        self.logger = logging.getLogger(__name__)
    
    def summarize(self, texto: str, titulo: str, link: str = "", max_lines: int = 5) -> str:
        """
        Gera resumo de um documento
        
        Args:
            texto: Texto completo
            titulo: Título do documento
            link: Link original (será adicionado ao final)
            max_lines: Número máximo de linhas
            
        Returns:
            Resumo formatado completo
        """
        resumo = self.provider.summarize_text(texto, titulo, max_lines)
        
        # Adiciona link se fornecido
        if link and "🔗 Leia na íntegra:" not in resumo:
            resumo += f"\n\n🔗 Leia na íntegra: {link}"
        elif link:
            # Substitui link vazio se já existe o marcador
            resumo = resumo.replace("🔗 Leia na íntegra: ", f"🔗 Leia na íntegra: {link}")
        
        return resumo

