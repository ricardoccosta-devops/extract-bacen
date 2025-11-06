"""
Main orchestrator for Bacen data extraction
Combines scraping and LLM processing
"""

import logging
from typing import Dict, List, Optional
from selenium.webdriver.common.by import By

from .scraper import BacenScraper
from .llm_processor import LLMProcessor
from .config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BacenExtractor:
    """Main class for extracting and processing Bacen information"""
    
    def __init__(self, headless: bool = None):
        """
        Initialize Bacen Extractor
        
        Args:
            headless: Run browser in headless mode (default: from config)
        """
        self.headless = headless if headless is not None else Config.HEADLESS_MODE
        self.scraper: Optional[BacenScraper] = None
        self.llm: Optional[LLMProcessor] = None
        
    def __enter__(self):
        """Context manager entry"""
        self.initialize()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()
        
    def initialize(self):
        """Initialize scraper and LLM processor"""
        logger.info("Initializing Bacen Extractor...")
        
        # Validate configuration
        Config.validate()
        
        # Initialize components
        self.scraper = BacenScraper(headless=self.headless)
        self.scraper.start()
        
        self.llm = LLMProcessor()
        
        logger.info("Bacen Extractor initialized successfully")
        
    def cleanup(self):
        """Cleanup resources"""
        if self.scraper:
            self.scraper.stop()
            
    def extract_and_summarize(self, url: str = None) -> Dict[str, str]:
        """
        Extract content from Bacen page and generate a summary
        
        Args:
            url: URL to scrape (default: Bacen home page)
            
        Returns:
            Dictionary with scraped data and summary
        """
        if not self.scraper or not self.llm:
            raise RuntimeError("Extractor not initialized. Call initialize() first.")
        
        # Scrape content
        url = url or Config.BACEN_URL
        logger.info(f"Extracting information from: {url}")
        
        self.scraper.navigate_to(url)
        self.scraper.wait_for_element(By.TAG_NAME, 'body')
        
        page_data = {
            'url': url,
            'title': self.scraper.driver.title,
            'text': self.scraper.extract_page_text()
        }
        
        # Generate summary using LLM
        logger.info("Generating summary with LLM...")
        summary = self.llm.summarize_content(page_data['text'])
        
        return {
            'url': page_data['url'],
            'title': page_data['title'],
            'content_length': len(page_data['text']),
            'summary': summary
        }
    
    def extract_specific_information(self, url: str, extraction_prompt: str) -> Dict[str, str]:
        """
        Extract specific information from a Bacen page using custom prompt
        
        Args:
            url: URL to scrape
            extraction_prompt: Custom prompt for information extraction
            
        Returns:
            Dictionary with extracted information
        """
        if not self.scraper or not self.llm:
            raise RuntimeError("Extractor not initialized. Call initialize() first.")
        
        logger.info(f"Extracting specific information from: {url}")
        
        self.scraper.navigate_to(url)
        self.scraper.wait_for_element(By.TAG_NAME, 'body')
        
        text = self.scraper.extract_page_text()
        
        # Extract information using LLM
        logger.info("Extracting information with LLM...")
        extracted_info = self.llm.extract_information(text, extraction_prompt)
        
        return {
            'url': url,
            'title': self.scraper.driver.title,
            'extracted_information': extracted_info
        }
    
    def extract_structured_fields(self, url: str, fields: List[str]) -> Dict[str, any]:
        """
        Extract structured data fields from a Bacen page
        
        Args:
            url: URL to scrape
            fields: List of fields to extract
            
        Returns:
            Dictionary with URL, title, and extracted fields
        """
        if not self.scraper or not self.llm:
            raise RuntimeError("Extractor not initialized. Call initialize() first.")
        
        logger.info(f"Extracting structured fields from: {url}")
        
        self.scraper.navigate_to(url)
        self.scraper.wait_for_element(By.TAG_NAME, 'body')
        
        text = self.scraper.extract_page_text()
        
        # Extract structured data using LLM
        logger.info(f"Extracting fields: {', '.join(fields)}")
        extracted_data = self.llm.extract_structured_data(text, fields)
        
        return {
            'url': url,
            'title': self.scraper.driver.title,
            'fields': extracted_data
        }
    
    def answer_question_about_page(self, url: str, question: str) -> Dict[str, str]:
        """
        Answer a specific question about a Bacen page
        
        Args:
            url: URL to scrape
            question: Question to answer
            
        Returns:
            Dictionary with URL, question, and answer
        """
        if not self.scraper or not self.llm:
            raise RuntimeError("Extractor not initialized. Call initialize() first.")
        
        logger.info(f"Answering question about: {url}")
        
        self.scraper.navigate_to(url)
        self.scraper.wait_for_element(By.TAG_NAME, 'body')
        
        text = self.scraper.extract_page_text()
        
        # Answer question using LLM
        logger.info(f"Question: {question}")
        answer = self.llm.answer_question(text, question)
        
        return {
            'url': url,
            'title': self.scraper.driver.title,
            'question': question,
            'answer': answer
        }
