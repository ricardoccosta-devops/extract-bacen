# 🏦 Plataforma de Monitoramento Diário do Banco Central do Brasil (BACEN)

Sistema automatizado e modular para monitoramento diário de publicações do Banco Central do Brasil, com integração de LLM para sumarização inteligente, geração de relatórios PDF e interface web Streamlit.

## 🎯 Características Principais

- ✅ **Arquitetura Modular**: Separação clara de responsabilidades
- ✅ **Múltiplos Provedores LLM**: OpenAI, Claude, OLLAMA ou fallback
- ✅ **Geração de PDF Profissional**: Relatórios formatados com reportlab
- ✅ **Interface Web Streamlit**: Visualização e controle via navegador
- ✅ **Agendamento Automático**: Execução diária configurável
- ✅ **Envio Automático de Email**: PDF anexado aos relatórios
- ✅ **Logs Detalhados**: Rastreamento completo de operações

## 📁 Estrutura do Projeto

```
webcrawler_bacen/
├── modulo_scraper/          # Módulo de coleta de dados
│   ├── __init__.py
│   └── bacen_scraper.py
├── modulo_llm/              # Módulo de LLM
│   ├── __init__.py
│   ├── base.py
│   ├── openai_provider.py
│   ├── claude_provider.py
│   ├── ollama_provider.py
│   └── factory.py
├── modulo_report/           # Módulo de geração de PDF
│   ├── __init__.py
│   └── pdf_generator.py
├── modulo_email/            # Módulo de envio de email
│   ├── __init__.py
│   └── email_sender.py
├── modulo_scheduler/        # Módulo de agendamento
│   ├── __init__.py
│   └── task_scheduler.py
├── frontend/                # Interface Streamlit
│   └── app.py
├── config/                  # Configurações
│   ├── __init__.py
│   └── config.py
├── relatorios/              # PDFs gerados
├── logs/                    # Arquivos de log
├── main_refatorado.py       # Sistema principal
├── requirements_refatorado.txt
└── config_example_refatorado.env
```

## 🚀 Instalação

### 1. Pré-requisitos

- Python 3.11 ou superior
- Google Chrome instalado
- Conta de email (Gmail ou Outlook)

### 2. Instalar Dependências

```bash
pip install -r requirements_refatorado.txt
```

### 3. Configurar Ambiente

```bash
# Copiar arquivo de exemplo
cp config_example_refatorado.env .env

# Editar .env com suas credenciais
```

### 4. Configurar LLM (Opcional)

**OpenAI:**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sua_chave_aqui
```

**Claude:**
```env
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=sua_chave_aqui
```

**OLLAMA (Local):**
```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
```

**Fallback (Sem LLM):**
```env
LLM_PROVIDER=fallback
```

## 📖 Uso

### Execução Manual (Teste)

```bash
python main_refatorado.py --teste
```

### Execução com Agendamento

```bash
python main_refatorado.py --agendador
```

### Interface Web Streamlit

```bash
python main_refatorado.py --streamlit
```

Ou diretamente:

```bash
streamlit run frontend/app.py
```

## 🔧 Configuração Detalhada

### Email

**Gmail:**
1. Ative verificação em duas etapas
2. Gere senha de aplicativo
3. Use no `EMAIL_PASSWORD`

**Outlook:**
- Use senha normal da conta

### LLM Providers

#### OpenAI
- Requer API Key da OpenAI
- Modelos: gpt-3.5-turbo, gpt-4, etc.
- Custo por uso

#### Claude (Anthropic)
- Requer API Key da Anthropic
- Modelos: claude-3-sonnet, claude-3-opus, etc.
- Custo por uso

#### OLLAMA
- LLM local (gratuito)
- Requer instalação do OLLAMA
- Modelos: llama2, mistral, etc.

#### Fallback
- Sumarização simples baseada em palavras-chave
- Não requer API Key
- Gratuito mas menos preciso

## 📊 Fluxo de Execução

```
[Scheduler] 
    ↓
[Scraper] → Coleta dados do BACEN
    ↓
[LLM Manager] → Sumariza com LLM
    ↓
[PDF Generator] → Gera relatório PDF
    ↓
[Email Sender] → Envia por email
```

## 🎨 Interface Streamlit

A interface web permite:

- ✅ Executar coleta manualmente
- ✅ Processar com LLM selecionado
- ✅ Visualizar relatórios gerados
- ✅ Enviar emails manualmente
- ✅ Visualizar logs do sistema
- ✅ Configurar provedor LLM em tempo real

## 📝 Exemplo de Uso Programático

```python
from config.config import Config
from modulo_scraper import BACENScraper
from modulo_llm import LLMManager
from modulo_report import PDFGenerator

# Configuração
config = Config()

# Coleta
scraper = BACENScraper(config)
dados = scraper.executar_coleta()

# Processamento
llm = LLMManager(provider_name='openai', api_key='sua_key')
for item in dados:
    item['resumo'] = llm.summarize(
        texto=item['conteudo_completo'],
        titulo=item['titulo'],
        link=item['link']
    )

# Geração PDF
generator = PDFGenerator()
pdf_path = generator.generate_pdf(dados)
```

## 🔒 Segurança

- ✅ Credenciais em arquivo `.env` (não versionado)
- ✅ Senhas nunca no código
- ✅ Validação de configurações
- ✅ Logs sem informações sensíveis

## 🐛 Troubleshooting

### Erro de ChromeDriver
```bash
pip install --upgrade webdriver-manager
```

### Erro de LLM
- Verifique API Key
- Confirme provedor configurado
- Use `fallback` para testar sem LLM

### Erro de Email
- Verifique credenciais no `.env`
- Gmail: use senha de aplicativo
- Outlook: use senha normal

## 📚 Documentação Adicional

- `DOCUMENTACAO_TECNICA.md` - Documentação técnica completa
- `MANUAL_USUARIO.md` - Manual do usuário
- `INDICE_DOCUMENTACAO.md` - Índice de documentação

## 🔄 Migração da Versão Anterior

Se você estava usando a versão anterior:

1. Mantenha o arquivo `.env` existente
2. Adicione as novas variáveis de LLM
3. Execute: `pip install -r requirements_refatorado.txt`
4. Use `main_refatorado.py` em vez de `main.py`

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique os logs em `logs/`
2. Consulte a documentação
3. Entre em contato com a equipe de TI

## 📄 Licença

Sistema desenvolvido para uso interno da Cielo.

---

**Versão 2.0** - Refatoração Modular com LLM e Streamlit

