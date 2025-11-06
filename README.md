# Extract Bacen

Extração de informações do Bacen (Banco Central do Brasil) com uso de Selenium e LLM (Large Language Models).

## 📋 Descrição

Este projeto permite extrair e processar informações do site do Banco Central do Brasil usando:
- **Selenium**: Para navegação automatizada e extração de conteúdo web
- **OpenAI GPT**: Para processar e estruturar as informações extraídas usando IA

## 🚀 Funcionalidades

- ✅ Navegação automatizada no site do Bacen
- ✅ Extração de conteúdo de páginas web
- ✅ Resumo automático de conteúdo usando LLM
- ✅ Extração de informações específicas com prompts customizados
- ✅ Extração de dados estruturados
- ✅ Sistema de perguntas e respostas sobre o conteúdo
- ✅ Modo headless para execução em servidores

## 📦 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Google Chrome instalado
- Chave de API da OpenAI

### Passos

1. Clone o repositório:
```bash
git clone https://github.com/ricardoccosta-devops/extract-bacen.git
cd extract-bacen
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env e adicione sua chave de API da OpenAI
```

## ⚙️ Configuração

Edite o arquivo `.env` com suas configurações:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Bacen Website Configuration
BACEN_URL=https://www.bcb.gov.br

# Selenium Configuration
HEADLESS_MODE=True
TIMEOUT_SECONDS=30

# LLM Configuration
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.1
```

## 📖 Uso

### Exemplo Básico

```python
from src.extractor import BacenExtractor

# Usar o extrator com context manager
with BacenExtractor() as extractor:
    # Extrair e resumir página inicial do Bacen
    result = extractor.extract_and_summarize()
    print(f"Resumo: {result['summary']}")
```

### Exemplos Avançados

Execute o arquivo de exemplos:
```bash
python example.py
```

#### 1. Extração com Prompt Customizado

```python
custom_prompt = """
Extraia as seguintes informações:
1. Principais serviços disponíveis
2. Notícias importantes
3. Informações de contato
"""

with BacenExtractor() as extractor:
    result = extractor.extract_specific_information(
        url="https://www.bcb.gov.br",
        extraction_prompt=custom_prompt
    )
    print(result['extracted_information'])
```

#### 2. Extração de Campos Estruturados

```python
fields = ["institution_name", "main_services", "contact_email"]

with BacenExtractor() as extractor:
    result = extractor.extract_structured_fields(
        url="https://www.bcb.gov.br",
        fields=fields
    )
    print(result['fields'])
```

#### 3. Sistema de Perguntas e Respostas

```python
with BacenExtractor() as extractor:
    result = extractor.answer_question_about_page(
        url="https://www.bcb.gov.br",
        question="Quais são as principais funções do Banco Central?"
    )
    print(result['answer'])
```

## 🏗️ Estrutura do Projeto

```
extract-bacen/
├── src/
│   ├── __init__.py
│   ├── config.py          # Configurações e variáveis de ambiente
│   ├── scraper.py         # Scraper usando Selenium
│   ├── llm_processor.py   # Processador LLM (OpenAI)
│   └── extractor.py       # Orquestrador principal
├── example.py             # Exemplos de uso
├── requirements.txt       # Dependências Python
├── .env.example          # Exemplo de configuração
├── .gitignore
└── README.md
```

## 🔧 Componentes

### BacenScraper
Classe responsável pela navegação web e extração de conteúdo usando Selenium.

### LLMProcessor
Classe responsável pelo processamento de texto usando modelos de linguagem da OpenAI.

### BacenExtractor
Classe principal que orquestra o scraper e o processador LLM.

## 🛠️ Desenvolvimento

### Executar em Modo de Desenvolvimento

```python
# Com browser visível (não headless)
with BacenExtractor(headless=False) as extractor:
    result = extractor.extract_and_summarize()
```

## 📝 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## ⚠️ Aviso Legal

Este projeto é para fins educacionais e de pesquisa. Certifique-se de respeitar os termos de uso do site do Banco Central do Brasil ao usar esta ferramenta.
