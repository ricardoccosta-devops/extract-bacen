"""
Módulo LLM - Integração com modelos de linguagem
Classe base abstrata para provedores de LLM
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict
import logging


class LLMProvider(ABC):
    """Classe base abstrata para provedores de LLM"""
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Inicializa o provedor LLM
        
        Args:
            api_key: Chave da API
            **kwargs: Parâmetros adicionais específicos do provedor
        """
        self.api_key = api_key
        self.logger = logging.getLogger(self.__class__.__name__)
        self.setup_provider(**kwargs)
    
    @abstractmethod
    def setup_provider(self, **kwargs):
        """Configura o provedor específico"""
        pass
    
    @abstractmethod
    def summarize_text(self, texto: str, titulo: str, max_lines: int = 5) -> str:
        """
        Gera resumo do texto usando LLM
        
        Args:
            texto: Texto completo para resumir
            titulo: Título do documento
            max_lines: Número máximo de linhas do resumo
            
        Returns:
            Resumo formatado com título em negrito, resumo e link
        """
        pass
    
    def format_summary(self, titulo: str, resumo: str, link: str) -> str:
        """
        Formata o resumo no padrão esperado
        
        Args:
            titulo: Título do documento
            resumo: Texto do resumo
            link: Link original
            
        Returns:
            Texto formatado
        """
        return f"**{titulo}**\n\n{resumo}\n\n🔗 Leia na íntegra: {link}"


class FallbackSummarizer:
    """Sumarizador de fallback quando LLM não está disponível"""
    
    @staticmethod
    def summarize_text(texto: str, titulo: str, max_lines: int = 5) -> str:
        """
        Resumo simples baseado em palavras-chave
        
        Args:
            texto: Texto completo
            titulo: Título do documento
            max_lines: Número máximo de linhas
            
        Returns:
            Resumo simples
        """
        import re
        
        # Limpa o texto
        texto_limpo = re.sub(r'\s+', ' ', texto)
        texto_limpo = texto_limpo.strip()
        
        # Divide em sentenças
        sentencas = re.split(r'[.!?]+', texto_limpo)
        sentencas = [s.strip() for s in sentencas if s.strip()]
        
        # Palavras-chave relevantes
        palavras_chave = [
            'banco central', 'bacen', 'resolução', 'circular', 'comunicado',
            'normativo', 'regulamentação', 'instituição', 'financeiro',
            'sistema', 'pagamento', 'cartão', 'crédito', 'débito',
            'transação', 'operador', 'adquirente', 'emissor'
        ]
        
        # Filtra sentenças relevantes
        sentencas_relevantes = []
        for sentenca in sentencas:
            if any(palavra.lower() in sentenca.lower() for palavra in palavras_chave):
                sentencas_relevantes.append(sentenca)
        
        # Se não encontrou, usa as primeiras
        if not sentencas_relevantes:
            sentencas_relevantes = sentencas[:max_lines * 2]
        
        # Limita ao número de linhas
        resumo_sentencas = sentencas_relevantes[:max_lines]
        
        # Completa se necessário
        if len(resumo_sentencas) < max_lines:
            for sentenca in sentencas:
                if sentenca not in resumo_sentencas:
                    resumo_sentencas.append(sentenca)
                    if len(resumo_sentencas) >= max_lines:
                        break
        
        return '. '.join(resumo_sentencas[:max_lines]) + '.'

