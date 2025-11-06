"""
LLM integration for processing scraped content
"""

from openai import OpenAI
from typing import Optional, Dict, List
import logging

from .config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMProcessor:
    """Process scraped content using Large Language Models"""
    
    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize LLM processor
        
        Args:
            api_key: OpenAI API key (default: from config)
            model: Model name (default: from config)
        """
        self.api_key = api_key or Config.OPENAI_API_KEY
        self.model = model or Config.LLM_MODEL
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = OpenAI(api_key=self.api_key)
        logger.info(f"LLM Processor initialized with model: {self.model}")
    
    def extract_information(self, text: str, prompt: str, temperature: float = None) -> str:
        """
        Extract specific information from text using LLM
        
        Args:
            text: Text to process
            prompt: Instruction for what to extract
            temperature: Model temperature (default: from config)
            
        Returns:
            Extracted information
        """
        temperature = temperature if temperature is not None else Config.LLM_TEMPERATURE
        
        logger.info(f"Processing text with LLM (length: {len(text)} chars)")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that extracts and structures information from web content."
                    },
                    {
                        "role": "user",
                        "content": f"{prompt}\n\nContent:\n{text}"
                    }
                ],
                temperature=temperature,
                max_tokens=2000
            )
            
            result = response.choices[0].message.content
            logger.info("LLM processing completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error processing with LLM: {e}")
            raise
    
    def summarize_content(self, text: str, max_length: int = 500) -> str:
        """
        Summarize content using LLM
        
        Args:
            text: Text to summarize
            max_length: Maximum length of summary
            
        Returns:
            Summary
        """
        prompt = f"Please provide a concise summary of the following content in approximately {max_length} characters. Focus on the most important information."
        return self.extract_information(text, prompt)
    
    def extract_structured_data(self, text: str, fields: List[str]) -> Dict[str, str]:
        """
        Extract structured data from text
        
        Args:
            text: Text to process
            fields: List of fields to extract
            
        Returns:
            Dictionary with extracted fields
        """
        fields_str = ", ".join(fields)
        prompt = f"""Extract the following information from the text and return it in a structured format:
        
Fields to extract: {fields_str}

Please return the information in the following JSON format:
{{
    "field1": "value1",
    "field2": "value2",
    ...
}}

If a field is not found, use "N/A" as the value."""
        
        result = self.extract_information(text, prompt)
        
        # Parse the result (basic parsing, could be enhanced)
        import json
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            logger.warning("Could not parse LLM response as JSON, returning raw text")
            return {"raw_response": result}
    
    def classify_content(self, text: str, categories: List[str]) -> str:
        """
        Classify content into predefined categories
        
        Args:
            text: Text to classify
            categories: List of possible categories
            
        Returns:
            Most appropriate category
        """
        categories_str = ", ".join(categories)
        prompt = f"""Classify the following content into one of these categories: {categories_str}

Return only the category name, nothing else."""
        
        return self.extract_information(text, prompt).strip()
    
    def answer_question(self, text: str, question: str) -> str:
        """
        Answer a specific question about the content
        
        Args:
            text: Context text
            question: Question to answer
            
        Returns:
            Answer to the question
        """
        prompt = f"""Based on the following content, please answer this question: {question}

If the answer is not found in the content, say "Information not found in the provided content." """
        
        return self.extract_information(text, prompt)
