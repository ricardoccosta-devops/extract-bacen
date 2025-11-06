import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import logging
from config import *

class WebcrawlerBACEN:
    def __init__(self):
        self.driver = None
        self.setup_logging()
        
    def setup_logging(self):
        """Configura o sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('webcrawler.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_driver(self):
        """Configura o driver do Selenium"""
        try:
            chrome_options = Options()
            if HEADLESS_MODE:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(TIMEOUT_PAGINA)
            
            self.logger.info("Driver do Selenium configurado com sucesso")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao configurar driver: {str(e)}")
            return False
    
    def get_system_date(self):
        """Retorna a data atual do sistema operacional no formato usado pelo BACEN"""
        from datetime import datetime
        import pytz
        
        # Obtém a data atual do sistema operacional
        system_date = datetime.now()
        
        # Converte para o fuso horário do Brasil se necessário
        try:
            brazil_tz = pytz.timezone('America/Sao_Paulo')
            system_date = system_date.astimezone(brazil_tz)
        except:
            # Se não conseguir converter, usa a data local
            pass
        
        return system_date.strftime("%d/%m/%Y")
    
    def buscar_comunicados(self):
        """Busca comunicados da data atual do sistema"""
        self.logger.info("Iniciando busca de comunicados...")
        
        try:
            self.driver.get(BACEN_COMUNICADOS_URL)
            time.sleep(DELAY_ENTRE_REQUISICOES)
            
            # Aguarda a página carregar
            WebDriverWait(self.driver, TIMEOUT_PAGINA).until(
                EC.presence_of_element_located((By.CLASS_NAME, "lista"))
            )
            
            # Busca por elementos que contenham a data do sistema
            system_date = self.get_system_date()
            comunicados = []
            
            # Procura por links e títulos de comunicados
            elementos = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='comunicado']")
            
            for elemento in elementos:
                try:
                    texto = elemento.text.strip()
                    link = elemento.get_attribute('href')
                    
                    if texto and link:
                        comunicados.append({
                            'titulo': texto,
                            'link': link,
                            'data': system_date,
                            'tipo': 'Comunicado'
                        })
                        
                except Exception as e:
                    self.logger.warning(f"Erro ao processar elemento: {str(e)}")
                    continue
            
            self.logger.info(f"Encontrados {len(comunicados)} comunicados")
            return comunicados
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar comunicados: {str(e)}")
            return []
    
    def buscar_resolucoes(self):
        """Busca resoluções da data atual do sistema"""
        self.logger.info("Iniciando busca de resoluções...")
        
        try:
            self.driver.get(BACEN_RESOLUCOES_URL)
            time.sleep(DELAY_ENTRE_REQUISICOES)
            
            WebDriverWait(self.driver, TIMEOUT_PAGINA).until(
                EC.presence_of_element_located((By.CLASS_NAME, "lista"))
            )
            
            system_date = self.get_system_date()
            resolucoes = []
            
            elementos = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='resolucao']")
            
            for elemento in elementos:
                try:
                    texto = elemento.text.strip()
                    link = elemento.get_attribute('href')
                    
                    if texto and link:
                        resolucoes.append({
                            'titulo': texto,
                            'link': link,
                            'data': system_date,
                            'tipo': 'Resolução'
                        })
                        
                except Exception as e:
                    self.logger.warning(f"Erro ao processar elemento: {str(e)}")
                    continue
            
            self.logger.info(f"Encontradas {len(resolucoes)} resoluções")
            return resolucoes
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar resoluções: {str(e)}")
            return []
    
    def buscar_circulares(self):
        """Busca circulares da data atual do sistema"""
        self.logger.info("Iniciando busca de circulares...")
        
        try:
            self.driver.get(BACEN_CIRCULARES_URL)
            time.sleep(DELAY_ENTRE_REQUISICOES)
            
            WebDriverWait(self.driver, TIMEOUT_PAGINA).until(
                EC.presence_of_element_located((By.CLASS_NAME, "lista"))
            )
            
            system_date = self.get_system_date()
            circulares = []
            
            elementos = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='circular']")
            
            for elemento in elementos:
                try:
                    texto = elemento.text.strip()
                    link = elemento.get_attribute('href')
                    
                    if texto and link:
                        circulares.append({
                            'titulo': texto,
                            'link': link,
                            'data': system_date,
                            'tipo': 'Circular'
                        })
                        
                except Exception as e:
                    self.logger.warning(f"Erro ao processar elemento: {str(e)}")
                    continue
            
            self.logger.info(f"Encontradas {len(circulares)} circulares")
            return circulares
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar circulares: {str(e)}")
            return []
    
    def executar_coleta(self):
        """Executa a coleta completa de todas as informações"""
        if not self.setup_driver():
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
            
            self.logger.info(f"Coleta concluída. Total de itens: {len(todas_informacoes)}")
            return todas_informacoes
            
        finally:
            if self.driver:
                self.driver.quit()
                self.logger.info("Driver encerrado")

if __name__ == "__main__":
    crawler = WebcrawlerBACEN()
    resultados = crawler.executar_coleta()
    print(f"Resultados encontrados: {len(resultados)}")
