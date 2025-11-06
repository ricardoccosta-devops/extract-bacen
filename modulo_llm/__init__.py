"""
Arquivo __init__.py para o módulo LLM
"""

from .base import LLMProvider, FallbackSummarizer
from .factory import LLMProviderFactory, LLMManager
from .openai_provider import OpenAIProvider
from .claude_provider import ClaudeProvider
from .ollama_provider import OllamaProvider

__all__ = [
    'LLMProvider',
    'FallbackSummarizer',
    'LLMProviderFactory',
    'LLMManager',
    'OpenAIProvider',
    'ClaudeProvider',
    'OllamaProvider'
]

