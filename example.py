"""
Example usage of Bacen Extract
Demonstrates how to use the library to extract information from Bacen website
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.extractor import BacenExtractor
from src.config import Config


def example_1_basic_summary():
    """Example 1: Extract and summarize Bacen home page"""
    print("\n" + "="*80)
    print("Example 1: Basic Summary of Bacen Home Page")
    print("="*80 + "\n")
    
    with BacenExtractor() as extractor:
        result = extractor.extract_and_summarize()
        
        print(f"URL: {result['url']}")
        print(f"Title: {result['title']}")
        print(f"Content Length: {result['content_length']} characters")
        print(f"\nSummary:\n{result['summary']}")


def example_2_specific_information():
    """Example 2: Extract specific information with custom prompt"""
    print("\n" + "="*80)
    print("Example 2: Extract Specific Information")
    print("="*80 + "\n")
    
    custom_prompt = """
    Please extract the following information from this Banco Central do Brasil page:
    1. Main services or sections available
    2. Any important announcements or news
    3. Contact information if available
    
    Provide a clear, structured response.
    """
    
    with BacenExtractor() as extractor:
        result = extractor.extract_specific_information(
            url=Config.BACEN_URL,
            extraction_prompt=custom_prompt
        )
        
        print(f"URL: {result['url']}")
        print(f"Title: {result['title']}")
        print(f"\nExtracted Information:\n{result['extracted_information']}")


def example_3_structured_fields():
    """Example 3: Extract structured data fields"""
    print("\n" + "="*80)
    print("Example 3: Extract Structured Fields")
    print("="*80 + "\n")
    
    fields = [
        "institution_name",
        "main_services",
        "contact_email",
        "last_update_date"
    ]
    
    with BacenExtractor() as extractor:
        result = extractor.extract_structured_fields(
            url=Config.BACEN_URL,
            fields=fields
        )
        
        print(f"URL: {result['url']}")
        print(f"Title: {result['title']}")
        print(f"\nExtracted Fields:")
        print(json.dumps(result['fields'], indent=2, ensure_ascii=False))


def example_4_question_answering():
    """Example 4: Answer specific questions about the page"""
    print("\n" + "="*80)
    print("Example 4: Question Answering")
    print("="*80 + "\n")
    
    questions = [
        "What are the main functions of Banco Central do Brasil?",
        "How can I access economic indicators?",
        "What regulatory information is available?"
    ]
    
    with BacenExtractor() as extractor:
        for question in questions:
            print(f"\nQuestion: {question}")
            result = extractor.answer_question_about_page(
                url=Config.BACEN_URL,
                question=question
            )
            print(f"Answer: {result['answer']}")
            print("-" * 80)


def main():
    """Main function to run examples"""
    print("\n" + "="*80)
    print("BACEN EXTRACT - Example Usage")
    print("="*80)
    
    # Check if API key is configured
    if not Config.OPENAI_API_KEY:
        print("\n⚠️  WARNING: OPENAI_API_KEY is not configured!")
        print("Please set it in .env file or environment variable.")
        print("See .env.example for reference.\n")
        return
    
    print("\nAvailable examples:")
    print("1. Basic summary of Bacen home page")
    print("2. Extract specific information with custom prompt")
    print("3. Extract structured data fields")
    print("4. Question answering about the page")
    print("\nRunning Example 1 (you can modify this script to run other examples)...\n")
    
    try:
        # Run example 1 by default
        example_1_basic_summary()
        
        # Uncomment to run other examples:
        # example_2_specific_information()
        # example_3_structured_fields()
        # example_4_question_answering()
        
        print("\n" + "="*80)
        print("Example completed successfully!")
        print("="*80 + "\n")
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("Please check your .env file configuration.\n")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check the logs for more details.\n")


if __name__ == "__main__":
    main()
