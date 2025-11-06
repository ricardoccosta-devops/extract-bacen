"""
Módulo Scraper - Coleta de dados do BACEN
Responsável por navegar no site do BACEN e extrair publicações do dia anterior
"""

import os
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import sys

# Adiciona o diretório raiz ao path para importar config
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

try:
    from config.config import Config
except ImportError:
    # Fallback para configuração básica se config não estiver disponível
    class Config:
        HEADLESS_MODE = True
        TIMEOUT_PAGINA = 30
        DELAY_ENTRE_REQUISICOES = 2
        FUSO_HORARIO = "America/Sao_Paulo"
        BACEN_BASE_URL = "https://www.bcb.gov.br"
        BACEN_COMUNICADOS_URL = "https://www.bcb.gov.br/estabilidadefinanceira/comunicados"
        BACEN_RESOLUCOES_URL = "https://www.bcb.gov.br/estabilidadefinanceira/resolucoes"
        BACEN_CIRCULARES_URL = "https://www.bcb.gov.br/estabilidadefinanceira/circular"


class BACENScraper:
    """Scraper para coletar publicações do Banco Central do Brasil"""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Inicializa o scraper
        
        Args:
            config: Objeto de configuração (opcional)
        """
        self.config = config or Config()
        self.driver: Optional[webdriver.Chrome] = None
        self.setup_logging()
        
    def setup_logging(self):
        """Configura o sistema de logging"""
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(log_dir, 'scraper.log')),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_driver(self) -> bool:
        """
        Configura o driver do Selenium
        
        Returns:
            True se configurado com sucesso, False caso contrário
        """
        try:
            chrome_options = Options()
            
            if self.config.HEADLESS_MODE:
                chrome_options.add_argument("--headless")
            
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(self.config.TIMEOUT_PAGINA)
            
            self.logger.info("Driver do Selenium configurado com sucesso")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao configurar driver: {str(e)}")
            return False
    
    def get_yesterday_date(self) -> str:
        """
        Retorna a data do dia anterior no formato usado pelo BACEN
        
        Returns:
            Data no formato DD/MM/YYYY
        """
        try:
            from datetime import datetime, timedelta
            import pytz
            
            # Obtém a data atual no fuso horário do Brasil
            brazil_tz = pytz.timezone(self.config.FUSO_HORARIO)
            hoje = datetime.now(brazil_tz)
            
            # Calcula o dia anterior
            ontem = hoje - timedelta(days=1)
            
            return ontem.strftime("%d/%m/%Y")
            
        except Exception as e:
            self.logger.warning(f"Erro ao calcular data anterior: {str(e)}")
            # Fallback para data local
            ontem = datetime.now() - timedelta(days=1)
            return ontem.strftime("%d/%m/%Y")
    
    def buscar_comunicados(self) -> List[Dict]:
        """
        Busca comunicados do dia anterior
        
        Returns:
            Lista de dicionários com informações dos comunicados
        """
        self.logger.info("Iniciando busca de comunicados...")
        
        try:
            self.driver.get(self.config.BACEN_COMUNICADOS_URL)
            time.sleep(self.config.DELAY_ENTRE_REQUISICOES)
            
            # Aguarda a página carregar
            WebDriverWait(self.driver, self.config.TIMEOUT_PAGINA).until(
                EC.presence_of_element_located((By.CLASS_NAME, "lista"))
            )
            
            data_anterior = self.get_yesterday_date()
            comunicados = []
            
            # Procura por links e títulos de comunicados
            elementos = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='comunicado']")
            
            for elemento in elementos:
                try:
                    texto = elemento.text.strip()
                    link = elemento.get_attribute('href')
                    
                    if texto and link:
                        # Verifica se o link é completo
                        if not link.startswith('http'):
                            link = f"{self.config.BACEN_BASE_URL}{link}"
                        
                        comunicados.append({
                            'titulo': texto,
                            'link': link,
                            'data': data_anterior,
                            'tipo': 'Comunicado',
                            'categoria': 'comunicado'
                        })
                        
                except Exception as e:
                    self.logger.warning(f"Erro ao processar elemento: {str(e)}")
                    continue
            
            self.logger.info(f"Encontrados {len(comunicados)} comunicados")
            return comunicados
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar comunicados: {str(e)}")
            return []
    
    def buscar_resolucoes(self) -> List[Dict]:
        """
        Busca resoluções do dia anterior
        
        Returns:
            Lista de dicionários com informações das resoluções
        """
        self.logger.info("Iniciando busca de resoluções...")
        
        try:
            self.driver.get(self.config.BACEN_RESOLUCOES_URL)
            time.sleep(self.config.DELAY_ENTRE_REQUISICOES)
            
            WebDriverWait(self.driver, self.config.TIMEOUT_PAGINA).until(
                EC.presence_of_element_located((By.CLASS_NAME, "lista"))
            )
            
            data_anterior = self.get_yesterday_date()
            resolucoes = []
            
            elementos = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='resolucao']")
            
            for elemento in elementos:
                try:
                    texto = elemento.text.strip()
                    link = elemento.get_attribute('href')
                    
                    if texto and link:
                        if not link.startswith('http'):
                            link = f"{self.config.BACEN_BASE_URL}{link}"
                        
                        resolucoes.append({
                            'titulo': texto,
                            'link': link,
                            'data': data_anterior,
                            'tipo': 'Resolução',
                            'categoria': 'resolucao'
                        })
                        
                except Exception as e:
                    self.logger.warning(f"Erro ao processar elemento: {str(e)}")
                    continue
            
            self.logger.info(f"Encontradas {len(resolucoes)} resoluções")
            return resolucoes
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar resoluções: {str(e)}")
            return []
    
    def buscar_circulares(self) -> List[Dict]:
        """
        Busca circulares do dia anterior
        
        Returns:
            Lista de dicionários com informações das circulares
        """
        self.logger.info("Iniciando busca de circulares...")
        
        try:
            self.driver.get(self.config.BACEN_CIRCULARES_URL)
            time.sleep(self.config.DELAY_ENTRE_REQUISICOES)
            
            WebDriverWait(self.driver, self.config.TIMEOUT_PAGINA).until(
                EC.presence_of_element_located((By.CLASS_NAME, "lista"))
            )
            
            data_anterior = self.get_yesterday_date()
            circulares = []
            
            elementos = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='circular']")
            
            for elemento in elementos:
                try:
                    texto = elemento.text.strip()
                    link = elemento.get_attribute('href')
                    
                    if texto and link:
                        if not link.startswith('http'):
                            link = f"{self.config.BACEN_BASE_URL}{link}"
                        
                        circulares.append({
                            'titulo': texto,
                            'link': link,
                            'data': data_anterior,
                            'tipo': 'Circular',
                            'categoria': 'circular'
                        })
                        
                except Exception as e:
                    self.logger.warning(f"Erro ao processar elemento: {str(e)}")
                    continue
            
            self.logger.info(f"Encontradas {len(circulares)} circulares")
            return circulares
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar circulares: {str(e)}")
            return []
    
    def obter_conteudo_completo(self, url: str) -> str:
        """
        Obtém o conteúdo completo de uma página
        
        Args:
            url: URL da página
            
        Returns:
            Texto completo da página
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove scripts e estilos
            for script in soup(["script", "style", "nav", "header", "footer"]):
                script.decompose()
            
            # Extrai texto principal
            texto = soup.get_text(separator=' ', strip=True)
            
            return texto
            
        except Exception as e:
            self.logger.error(f"Erro ao obter conteúdo da URL {url}: {str(e)}")
            return ""
    
    def executar_coleta(self) -> List[Dict]:
        """
        Executa a coleta completa de todas as informações
        
        Returns:
            Lista consolidada de todas as publicações encontradas
        """
        if not self.setup_driver():
            self.logger.error("Não foi possível configurar o driver")
            return []
        
        try:
            todas_informacoes = []
            
            # Coleta comunicados
            comunicados = self.buscar_comunicados()
            todas_informacoes.extend(comunicados)
            
            # Coleta resoluções
            resolucoes = self.buscar_resolucoes()
            todas_informacoes.extend(resolucoes)
            
            # Coleta circulares
            circulares = self.buscar_circulares()
            todas_informacoes.extend(circulares)
            
            # Obtém conteúdo completo para cada item
            for item in todas_informacoes:
                if 'conteudo_completo' not in item:
                    item['conteudo_completo'] = self.obter_conteudo_completo(item['link'])
            
            self.logger.info(f"Coleta concluída. Total de itens: {len(todas_informacoes)}")
            return todas_informacoes
            
        except Exception as e:
            self.logger.error(f"Erro durante a coleta: {str(e)}")
            return []
            
        finally:
            if self.driver:
                self.driver.quit()
                self.logger.info("Driver encerrado")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    # Teste do módulo
    scraper = BACENScraper()
    resultados = scraper.executar_coleta()
    print(f"Resultados encontrados: {len(resultados)}")
    for item in resultados[:3]:  # Mostra apenas os 3 primeiros
        print(f"- {item['tipo']}: {item['titulo'][:50]}...")

