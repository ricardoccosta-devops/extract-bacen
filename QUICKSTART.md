# Quick Start - Extract Bacen

## Installation rapide (Quick Setup)

```bash
# 1. Clone o repositório
git clone https://github.com/ricardoccosta-devops/extract-bacen.git
cd extract-bacen

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Configure a API Key
cp .env.example .env
# Edite .env e adicione: OPENAI_API_KEY=sua_chave_aqui

# 4. Execute o exemplo
python example.py
```

## Uso Básico (Basic Usage)

```python
from src.extractor import BacenExtractor

# Resumir página do Bacen
with BacenExtractor() as extractor:
    result = extractor.extract_and_summarize()
    print(result['summary'])
```

## Principais Funcionalidades (Main Features)

| Funcionalidade | Método |
|---------------|---------|
| Resumir página | `extract_and_summarize()` |
| Extração customizada | `extract_specific_information(url, prompt)` |
| Dados estruturados | `extract_structured_fields(url, fields)` |
| Perguntas & Respostas | `answer_question_about_page(url, question)` |

## Exemplos Rápidos (Quick Examples)

### 1. Extrair taxas e indicadores
```python
with BacenExtractor() as extractor:
    result = extractor.extract_specific_information(
        url="https://www.bcb.gov.br",
        extraction_prompt="Extraia taxa Selic e inflação"
    )
```

### 2. Responder perguntas
```python
with BacenExtractor() as extractor:
    result = extractor.answer_question_about_page(
        url="https://www.bcb.gov.br",
        question="Qual a taxa Selic atual?"
    )
```

### 3. Dados estruturados
```python
with BacenExtractor() as extractor:
    result = extractor.extract_structured_fields(
        url="https://www.bcb.gov.br",
        fields=["taxa_selic", "meta_inflacao"]
    )
```

## Configuração (Configuration)

Arquivo `.env`:
```env
OPENAI_API_KEY=sk-your-key-here
LLM_MODEL=gpt-4o-mini          # ou gpt-4o
HEADLESS_MODE=True              # False para debug
TIMEOUT_SECONDS=30
```

## Testes (Tests)

```bash
python tests/test_basic.py
```

## Documentação Completa

- 📖 [README.md](README.md) - Visão geral completa
- 📚 [USAGE.md](USAGE.md) - Guia detalhado de uso
- 🧪 [tests/README.md](tests/README.md) - Informações sobre testes

## Estrutura do Projeto

```
extract-bacen/
├── src/
│   ├── scraper.py         # Selenium scraping
│   ├── llm_processor.py   # Processamento LLM
│   ├── extractor.py       # Orquestrador principal
│   └── config.py          # Configurações
├── tests/                 # Testes
├── example.py            # Exemplos de uso
└── requirements.txt      # Dependências
```

## Suporte

Para mais informações, consulte a [documentação completa](README.md) ou abra uma issue no GitHub.
