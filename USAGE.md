# Guia de Uso - Extract Bacen

Este guia fornece exemplos práticos de como usar o Extract Bacen para extrair e processar informações do site do Banco Central do Brasil.

## Configuração Inicial

1. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

2. **Configure a chave de API:**
```bash
cp .env.example .env
# Edite .env e adicione sua chave OpenAI
```

## Exemplos de Uso

### 1. Resumo Automático de Páginas

```python
from src.extractor import BacenExtractor

with BacenExtractor() as extractor:
    result = extractor.extract_and_summarize()
    print(result['summary'])
```

### 2. Extração com Prompt Personalizado

```python
from src.extractor import BacenExtractor

prompt = """
Extraia as seguintes informações da página:
1. Taxa Selic atual
2. Próxima reunião do COPOM
3. Principais indicadores econômicos
"""

with BacenExtractor() as extractor:
    result = extractor.extract_specific_information(
        url="https://www.bcb.gov.br",
        extraction_prompt=prompt
    )
    print(result['extracted_information'])
```

### 3. Extração de Dados Estruturados

```python
from src.extractor import BacenExtractor

fields = [
    "taxa_selic",
    "inflacao_meta",
    "reservas_internacionais",
    "taxa_cambio"
]

with BacenExtractor() as extractor:
    result = extractor.extract_structured_fields(
        url="https://www.bcb.gov.br",
        fields=fields
    )
    print(result['fields'])
```

### 4. Sistema de Perguntas e Respostas

```python
from src.extractor import BacenExtractor

with BacenExtractor() as extractor:
    result = extractor.answer_question_about_page(
        url="https://www.bcb.gov.br",
        question="Qual é a taxa Selic atual e quando foi definida?"
    )
    print(result['answer'])
```

### 5. Usando o Scraper Diretamente

```python
from src.scraper import BacenScraper
from selenium.webdriver.common.by import By

with BacenScraper(headless=True) as scraper:
    scraper.navigate_to("https://www.bcb.gov.br")
    scraper.wait_for_element(By.TAG_NAME, 'body')
    
    # Extrair texto
    text = scraper.extract_page_text()
    
    # Extrair HTML
    html = scraper.extract_page_html()
    
    # Buscar elementos específicos
    elements = scraper.get_elements_by_selector('.main-content')
```

### 6. Usando o Processador LLM Diretamente

```python
from src.llm_processor import LLMProcessor

processor = LLMProcessor()

# Resumir texto
summary = processor.summarize_content(texto_longo)

# Extrair informações específicas
info = processor.extract_information(
    text=texto,
    prompt="Extraia as taxas de juros mencionadas no texto"
)

# Classificar conteúdo
category = processor.classify_content(
    text=texto,
    categories=["Política Monetária", "Câmbio", "Regulação", "Relatório"]
)

# Responder perguntas
answer = processor.answer_question(
    text=texto,
    question="Qual foi a decisão do COPOM?"
)
```

## Modo de Desenvolvimento

Para ver o navegador durante a execução (útil para debug):

```python
from src.extractor import BacenExtractor

# Executar com browser visível
with BacenExtractor(headless=False) as extractor:
    result = extractor.extract_and_summarize()
```

## Configurações Avançadas

Você pode personalizar as configurações no arquivo `.env`:

```env
# Modelo LLM (mais rápido/barato ou mais poderoso)
LLM_MODEL=gpt-4o-mini  # ou gpt-4o para melhor qualidade

# Temperatura do LLM (0.0-1.0, menor = mais determinístico)
LLM_TEMPERATURE=0.1

# Timeout para elementos da página
TIMEOUT_SECONDS=30

# Modo headless
HEADLESS_MODE=True
```

## Tratamento de Erros

```python
from src.extractor import BacenExtractor

try:
    with BacenExtractor() as extractor:
        result = extractor.extract_and_summarize()
except ValueError as e:
    print(f"Erro de configuração: {e}")
except RuntimeError as e:
    print(f"Erro de execução: {e}")
except Exception as e:
    print(f"Erro inesperado: {e}")
```

## Executando os Exemplos

Execute o arquivo de exemplos incluído:

```bash
python example.py
```

## Logs

O sistema registra logs informativos. Para ver logs detalhados:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Dicas

1. **Performance**: Use `headless=True` em produção
2. **Custos**: Use `gpt-4o-mini` para reduzir custos
3. **Precisão**: Use `gpt-4o` para melhor qualidade
4. **Timeout**: Aumente `TIMEOUT_SECONDS` para páginas lentas
5. **Rate Limits**: Implemente delays entre requisições se necessário
