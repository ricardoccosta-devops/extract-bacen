"""
Configuration module for Bacen Extract
Loads environment variables and provides configuration settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Configuration class for Bacen Extract"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Bacen Website Configuration
    BACEN_URL = os.getenv('BACEN_URL', 'https://www.bcb.gov.br')
    
    # Selenium Configuration
    HEADLESS_MODE = os.getenv('HEADLESS_MODE', 'True').lower() == 'true'
    TIMEOUT_SECONDS = int(os.getenv('TIMEOUT_SECONDS', '30'))
    
    # LLM Configuration
    LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-4o-mini')
    LLM_TEMPERATURE = float(os.getenv('LLM_TEMPERATURE', '0.1'))
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required. Please set it in .env file")
        return True
