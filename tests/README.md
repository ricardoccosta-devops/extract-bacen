# Tests for Extract Bacen

This directory contains tests for the Extract Bacen project.

## Running Tests

### Basic Tests (No API Key Required)

```bash
python tests/test_basic.py
```

These tests verify:
- Module imports
- Configuration loading
- Basic initialization
- Input validation

### Integration Tests (API Key Required)

For full integration tests that actually call the Bacen website and OpenAI API, you need to:

1. Set up your `.env` file with valid credentials
2. Run the example script:

```bash
python example.py
```

## Test Coverage

Currently includes:
- ✓ Import tests
- ✓ Configuration tests  
- ✓ Scraper initialization tests
- ✓ LLM processor validation tests

Future tests could include:
- Integration tests with real API calls
- Mock tests for scraping functionality
- Performance tests
- Error handling tests
