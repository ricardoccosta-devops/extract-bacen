"""
Selenium-based web scraper for Bacen website
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from typing import Optional, Dict, List
import logging

from .config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BacenScraper:
    """Web scraper for Banco Central do Brasil website"""
    
    def __init__(self, headless: bool = None):
        """
        Initialize the Bacen scraper
        
        Args:
            headless: Run browser in headless mode (default: from config)
        """
        self.headless = headless if headless is not None else Config.HEADLESS_MODE
        self.driver: Optional[webdriver.Chrome] = None
        self.timeout = Config.TIMEOUT_SECONDS
        
    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()
        
    def start(self):
        """Initialize and start the browser"""
        logger.info("Starting Chrome browser...")
        
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Additional options for stability
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        logger.info("Browser started successfully")
        
    def stop(self):
        """Stop the browser and cleanup"""
        if self.driver:
            logger.info("Stopping browser...")
            self.driver.quit()
            self.driver = None
            
    def navigate_to(self, url: str):
        """
        Navigate to a specific URL
        
        Args:
            url: URL to navigate to
        """
        if not self.driver:
            raise RuntimeError("Browser not started. Call start() first.")
        
        logger.info(f"Navigating to {url}")
        self.driver.get(url)
        
    def extract_page_text(self) -> str:
        """
        Extract all text content from the current page
        
        Returns:
            Text content of the page
        """
        if not self.driver:
            raise RuntimeError("Browser not started. Call start() first.")
        
        return self.driver.find_element(By.TAG_NAME, 'body').text
    
    def extract_page_html(self) -> str:
        """
        Extract HTML content from the current page
        
        Returns:
            HTML content of the page
        """
        if not self.driver:
            raise RuntimeError("Browser not started. Call start() first.")
        
        return self.driver.page_source
    
    def wait_for_element(self, by: By, value: str, timeout: int = None) -> bool:
        """
        Wait for an element to be present on the page
        
        Args:
            by: Selenium By locator type
            value: Locator value
            timeout: Timeout in seconds (default: from config)
            
        Returns:
            True if element found, False otherwise
        """
        if not self.driver:
            raise RuntimeError("Browser not started. Call start() first.")
        
        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except Exception as e:
            logger.warning(f"Element not found: {value}. Error: {e}")
            return False
    
    def get_elements_by_selector(self, selector: str) -> List[Dict[str, str]]:
        """
        Get elements by CSS selector
        
        Args:
            selector: CSS selector
            
        Returns:
            List of elements with text and attributes
        """
        if not self.driver:
            raise RuntimeError("Browser not started. Call start() first.")
        
        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
        results = []
        
        for elem in elements:
            results.append({
                'text': elem.text,
                'tag': elem.tag_name,
                'html': elem.get_attribute('outerHTML')
            })
        
        return results
    
    def scrape_bacen_home(self) -> Dict[str, any]:
        """
        Scrape information from Bacen home page
        
        Returns:
            Dictionary with scraped information
        """
        self.navigate_to(Config.BACEN_URL)
        
        # Wait for page to load
        self.wait_for_element(By.TAG_NAME, 'body')
        
        return {
            'url': self.driver.current_url,
            'title': self.driver.title,
            'text': self.extract_page_text(),
            'html': self.extract_page_html()
        }
