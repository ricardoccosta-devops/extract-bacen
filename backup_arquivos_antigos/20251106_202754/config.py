import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do Webcrawler BACEN
# Configurações de Email
EMAIL_PROVIDER = os.getenv("EMAIL_PROVIDER", "gmail")  # gmail ou outlook

# Configurações específicas por provedor
if EMAIL_PROVIDER.lower() == "outlook":
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp-mail.outlook.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
else:  # Gmail (padrão)
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

EMAIL_USER = os.getenv("EMAIL_USER", "seu_email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "sua_senha_app")

# Lista de destinatários
DESTINATARIOS_STR = os.getenv("DESTINATARIOS", "destinatario1@cielo.com.br,destinatario2@cielo.com.br")
DESTINATARIOS = [email.strip() for email in DESTINATARIOS_STR.split(",") if email.strip()]

# Configurações do Webcrawler
BACEN_BASE_URL = os.getenv("BACEN_BASE_URL", "https://www.bcb.gov.br")
BACEN_COMUNICADOS_URL = os.getenv("BACEN_COMUNICADOS_URL", "https://www.bcb.gov.br/estabilidadefinanceira/comunicados")
BACEN_RESOLUCOES_URL = os.getenv("BACEN_RESOLUCOES_URL", "https://www.bcb.gov.br/estabilidadefinanceira/resolucoes")
BACEN_CIRCULARES_URL = os.getenv("BACEN_CIRCULARES_URL", "https://www.bcb.gov.br/estabilidadefinanceira/circular")

# Configurações de Agendamento
HORA_EXECUCAO = os.getenv("HORA_EXECUCAO", "07:00")
FUSO_HORARIO = os.getenv("FUSO_HORARIO", "America/Sao_Paulo")

# Configurações do Selenium
HEADLESS_MODE = os.getenv("HEADLESS_MODE", "true").lower() == "true"
TIMEOUT_PAGINA = int(os.getenv("TIMEOUT_PAGINA", "30"))
DELAY_ENTRE_REQUISICOES = int(os.getenv("DELAY_ENTRE_REQUISICOES", "2"))

# Informações sobre provedores de email suportados
EMAIL_PROVIDERS_INFO = {
    "gmail": {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "description": "Gmail - Requer senha de aplicativo"
    },
    "outlook": {
        "smtp_server": "smtp-mail.outlook.com", 
        "smtp_port": 587,
        "description": "Outlook/Hotmail - Usa senha normal"
    }
}
