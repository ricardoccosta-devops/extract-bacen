"""
Arquivo de Configuração Centralizado
"""

import os
from dotenv import load_dotenv
from typing import List
from pathlib import Path

# Carrega variáveis de ambiente
load_dotenv()


class Config:
    """Classe de configuração centralizada"""
    
    def __init__(self):
        """Inicializa configurações a partir de variáveis de ambiente"""
        
        # Configurações de Email
        self.EMAIL_PROVIDER = os.getenv("EMAIL_PROVIDER", "gmail").lower()
        
        if self.EMAIL_PROVIDER == "outlook":
            self.SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp-mail.outlook.com")
            self.SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
        else:  # Gmail (padrão)
            self.SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
            self.SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
        
        self.EMAIL_USER = os.getenv("EMAIL_USER", "")
        self.EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
        
        # Lista de destinatários
        destinatarios_str = os.getenv("DESTINATARIOS", "")
        self.DESTINATARIOS = [
            email.strip() 
            for email in destinatarios_str.split(",") 
            if email.strip()
        ]
        
        # Configurações do Webcrawler
        self.BACEN_BASE_URL = os.getenv("BACEN_BASE_URL", "https://www.bcb.gov.br")
        self.BACEN_COMUNICADOS_URL = os.getenv(
            "BACEN_COMUNICADOS_URL", 
            "https://www.bcb.gov.br/estabilidadefinanceira/comunicados"
        )
        self.BACEN_RESOLUCOES_URL = os.getenv(
            "BACEN_RESOLUCOES_URL",
            "https://www.bcb.gov.br/estabilidadefinanceira/resolucoes"
        )
        self.BACEN_CIRCULARES_URL = os.getenv(
            "BACEN_CIRCULARES_URL",
            "https://www.bcb.gov.br/estabilidadefinanceira/circular"
        )
        
        # Configurações de Agendamento
        self.HORA_EXECUCAO = os.getenv("HORA_EXECUCAO", "07:00")
        self.FUSO_HORARIO = os.getenv("FUSO_HORARIO", "America/Sao_Paulo")
        
        # Configurações do Selenium
        self.HEADLESS_MODE = os.getenv("HEADLESS_MODE", "true").lower() == "true"
        self.TIMEOUT_PAGINA = int(os.getenv("TIMEOUT_PAGINA", "30"))
        self.DELAY_ENTRE_REQUISICOES = int(os.getenv("DELAY_ENTRE_REQUISICOES", "2"))
        
        # Configurações de LLM
        self.LLM_PROVIDER = os.getenv("LLM_PROVIDER", "fallback").lower()
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
        self.OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
        self.OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-sonnet-20240229")
        
        # Diretórios
        self.BASE_DIR = Path(__file__).parent.parent
        self.RELATORIOS_DIR = self.BASE_DIR / "relatorios"
        self.LOGS_DIR = self.BASE_DIR / "logs"
        
        # Cria diretórios se não existirem
        self.RELATORIOS_DIR.mkdir(exist_ok=True)
        self.LOGS_DIR.mkdir(exist_ok=True)
    
    def get_llm_api_key(self) -> str:
        """
        Retorna a API key do provedor LLM configurado
        
        Returns:
            API key ou string vazia
        """
        if self.LLM_PROVIDER == "openai":
            return self.OPENAI_API_KEY
        elif self.LLM_PROVIDER in ["claude", "anthropic"]:
            return self.ANTHROPIC_API_KEY
        else:
            return ""
    
    def validate(self) -> List[str]:
        """
        Valida as configurações
        
        Returns:
            Lista de erros encontrados (vazia se tudo OK)
        """
        errors = []
        
        if not self.EMAIL_USER:
            errors.append("EMAIL_USER não configurado")
        
        if not self.EMAIL_PASSWORD:
            errors.append("EMAIL_PASSWORD não configurado")
        
        if not self.DESTINATARIOS:
            errors.append("DESTINATARIOS não configurado")
        
        if self.LLM_PROVIDER != "fallback" and not self.get_llm_api_key():
            errors.append(f"API Key do {self.LLM_PROVIDER.upper()} não configurada")
        
        return errors


# Instância global de configuração
config = Config()

