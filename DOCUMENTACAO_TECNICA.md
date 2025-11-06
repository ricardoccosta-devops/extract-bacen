# 📚 DOCUMENTAÇÃO TÉCNICA - Sistema de Monitoramento BACEN

## 📋 Índice

1. [Visão Geral do Sistema](#visão-geral-do-sistema)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Componentes e Módulos](#componentes-e-módulos)
4. [Fluxo de Dados](#fluxo-de-dados)
5. [Configuração e Ambiente](#configuração-e-ambiente)
6. [Instalação e Setup](#instalação-e-setup)
7. [Estrutura de Código](#estrutura-de-código)
8. [Dependências e Bibliotecas](#dependências-e-bibliotecas)
9. [Sistema de Logging](#sistema-de-logging)
10. [Tratamento de Erros](#tratamento-de-erros)
11. [Agendamento e Execução](#agendamento-e-execução)
12. [Integração com Serviços Externos](#integração-com-serviços-externos)
13. [Segurança](#segurança)
14. [Manutenção e Troubleshooting](#manutenção-e-troubleshooting)
15. [Extensibilidade](#extensibilidade)

---

## 🎯 Visão Geral do Sistema

### Objetivo
Sistema automatizado de monitoramento que coleta, processa e distribui informações sobre comunicados, resoluções e circulares publicados pelo Banco Central do Brasil (BACEN).

### Tecnologias Principais
- **Python 3.8+**: Linguagem de programação
- **Selenium**: Automação de navegador para web scraping
- **BeautifulSoup4**: Parsing de HTML
- **SMTP**: Envio de emails
- **Schedule**: Agendamento de tarefas

### Características Técnicas
- Execução em modo headless (sem interface gráfica)
- Suporte a múltiplos provedores de email (Gmail, Outlook)
- Sistema modular e extensível
- Logging detalhado para auditoria
- Tratamento robusto de erros

---

## 🏗️ Arquitetura do Sistema

### Padrão Arquitetural
O sistema segue um padrão **modular monolítico**, onde cada módulo possui responsabilidade única e comunica-se através de interfaces bem definidas.

```
┌─────────────────────────────────────────────────────────┐
│                  Sistema Monitoramento BACEN            │
│                       (main.py)                         │
└────────────┬────────────────────────────────────────────┘
             │
     ┌───────┴────────┐
     │                │
┌────▼─────┐    ┌─────▼────────┐    ┌───────────▼──────┐
│Webcrawler│───▶│ Sumarizador  │───▶│ Enviador Email  │
│          │    │              │    │                 │
└──────────┘    └──────────────┘    └─────────────────┘
     │                 │                      │
     ▼                 ▼                      ▼
┌──────────┐    ┌──────────┐         ┌──────────────┐
│   BACEN  │    │ Relatório│         │     SMTP     │
│  Website │    │   HTML   │         │   Servers    │
└──────────┘    └──────────┘         └──────────────┘
```

### Componentes Principais

1. **Orquestrador Principal** (`main.py`)
   - Gerencia o fluxo de execução
   - Controla agendamento
   - Trata erros globais

2. **Coletor de Dados** (`webcrawler.py`)
   - Automação de navegador
   - Extração de dados do BACEN

3. **Processador** (`sumarizador.py`)
   - Análise de conteúdo
   - Geração de resumos
   - Criação de relatórios HTML

4. **Comunicação** (`enviador_email.py`)
   - Envio de emails
   - Formatação de mensagens
   - Notificações do sistema

5. **Configuração** (`config.py`)
   - Carregamento de variáveis de ambiente
   - Configurações centralizadas

---

## 📦 Componentes e Módulos

### 1. SistemaPrincipal (main.py)

#### Classe: `SistemaMonitoramentoBACEN`

**Responsabilidades:**
- Orquestração do processo completo
- Configuração de agendamento
- Tratamento centralizado de erros
- Gerenciamento de logs

**Métodos Principais:**

##### `__init__(self)`
Inicializa o sistema, configura logging e instancia os módulos.

```python
def __init__(self):
    self.setup_logging()
    self.webcrawler = WebcrawlerBACEN()
    self.sumarizador = SumarizadorBACEN()
    self.enviador = EnviadorEmail()
```

##### `executar_processo_completo(self)`
Executa o fluxo completo de monitoramento em 4 etapas:

1. **Coleta**: Busca documentos no BACEN
2. **Processamento**: Sumariza informações
3. **Envio**: Distribui relatório por email
4. **Persistência**: Salva relatório localmente

**Fluxo de Execução:**
```python
dados_coletados = self.webcrawler.executar_coleta()
informacoes_processadas = self.sumarizador.processar_informacoes(dados_coletados)
resultado_envio = self.enviador.enviar_email(informacoes_processadas)
self.salvar_relatorio_local(informacoes_processadas)
```

##### `configurar_agendamento(self)`
Configura execução diária usando a biblioteca `schedule`.

**Configuração padrão:**
- Horário: 07:00 (configurável via `.env`)
- Fuso horário: America/Sao_Paulo

##### `executar_agendador(self)`
Mantém o sistema em execução contínua, verificando agendamentos a cada minuto.

**Características:**
- Loop infinito com verificação periódica
- Envio de notificação de inicialização
- Tratamento de interrupções (Ctrl+C)

---

### 2. Webcrawler (webcrawler.py)

#### Classe: `WebcrawlerBACEN`

**Responsabilidades:**
- Automação de navegador web
- Extração de dados do site do BACEN
- Identificação de documentos por tipo
- Tratamento de elementos dinâmicos

**Métodos Principais:**

##### `setup_driver(self)`
Configura o driver Selenium com Chrome.

**Configurações Aplicadas:**
- Modo headless (opcional via config)
- Desabilita GPU para ambientes sem display
- Timeout configurável
- Tamanho de janela padrão

**Dependências:**
- ChromeDriver (gerenciado pelo `webdriver-manager`)
- Google Chrome instalado no sistema

##### `get_system_date(self)`
Retorna a data atual do sistema operacional no formato DD/MM/YYYY.

**Características:**
- Converte para fuso horário do Brasil quando possível
- Fallback para data local se conversão falhar
- Usado para filtrar documentos do dia

##### `buscar_comunicados(self)`
Extrai comunicados da página do BACEN.

**Processo:**
1. Acessa URL configurada
2. Aguarda carregamento (WebDriverWait)
3. Localiza elementos com seletor CSS
4. Extrai título e link de cada item
5. Filtra por data do sistema
6. Retorna lista estruturada

**Estrutura de Dados Retornada:**
```python
{
    'titulo': str,      # Título do comunicado
    'link': str,        # URL completa
    'data': str,        # Data no formato DD/MM/YYYY
    'tipo': str         # "Comunicado"
}
```

##### `buscar_resolucoes(self)` e `buscar_circulares(self)`
Seguem o mesmo padrão de `buscar_comunicados()`, apenas variando:
- URL de destino
- Seletor CSS para identificar elementos
- Tipo de documento no retorno

##### `executar_coleta(self)`
Orquestra a coleta completa de todos os tipos de documentos.

**Fluxo:**
1. Inicializa driver Selenium
2. Executa busca de comunicados
3. Executa busca de resoluções
4. Executa busca de circulares
5. Combina todos os resultados
6. Encerra driver
7. Retorna lista consolidada

**Tratamento de Erros:**
- Usa blocos `try/finally` para garantir fechamento do driver
- Continua processamento mesmo se um tipo falhar
- Registra erros em log para diagnóstico

---

### 3. Sumarizador (sumarizador.py)

#### Classe: `SumarizadorBACEN`

**Responsabilidades:**
- Download de conteúdo completo de documentos
- Extração e limpeza de texto
- Geração de resumos inteligentes
- Criação de relatórios HTML

**Métodos Principais:**

##### `obter_conteudo_completo(self, url)`
Faz download do conteúdo HTML de uma URL.

**Características:**
- Usa biblioteca `requests` (mais leve que Selenium)
- Remove scripts e estilos
- Extrai apenas texto relevante
- Timeout de 30 segundos
- User-Agent customizado para evitar bloqueios

##### `extrair_resumo(self, texto_completo, titulo)`
Gera resumo inteligente de até 10 sentenças.

**Algoritmo:**
1. Limpa texto (remove espaços extras)
2. Divide em sentenças
3. Filtra por palavras-chave relevantes:
   - Termos financeiros: banco central, bacen, normativo
   - Termos regulatórios: resolução, circular, comunicado
   - Termos de pagamento: cartão, crédito, débito, transação
4. Prioriza sentenças relevantes
5. Completa com sentenças gerais se necessário
6. Limita a 10 sentenças

**Fallback:**
Se não encontrar sentenças relevantes, usa primeiras 15 sentenças ou primeiros 500 caracteres.

##### `processar_informacoes(self, dados_coletados)`
Processa lista de documentos coletados.

**Processo:**
1. Itera sobre cada documento
2. Baixa conteúdo completo
3. Gera resumo
4. Cria estrutura de dados processada
5. Adiciona metadados (data de processamento)

**Estrutura de Dados Processada:**
```python
{
    'titulo': str,
    'tipo': str,
    'data': str,
    'link': str,
    'resumo': str,              # Resumo de 10 linhas
    'data_processamento': str   # Timestamp
}
```

##### `gerar_relatorio_html(self, informacoes_processadas)`
Gera relatório HTML completo e formatado.

**Características:**
- HTML5 responsivo
- CSS inline para compatibilidade
- Organizado por tipo de documento
- Inclui links clicáveis
- Estilo profissional

**Estrutura do Relatório:**
- Cabeçalho com data
- Seção de Comunicados
- Seção de Resoluções
- Seção de Circulares
- Rodapé com informações do sistema

---

### 4. Enviador de Email (enviador_email.py)

#### Classe: `EnviadorEmail`

**Responsabilidades:**
- Configuração de servidor SMTP
- Criação de emails HTML
- Envio para múltiplos destinatários
- Notificações do sistema

**Métodos Principais:**

##### `configurar_servidor_smtp(self)`
Configura conexão SMTP baseada no provedor.

**Suporte a Provedores:**

**Gmail:**
- Servidor: `smtp.gmail.com`
- Porta: `587`
- Autenticação: TLS
- Requisito: Senha de aplicativo

**Outlook:**
- Servidor: `smtp-mail.outlook.com`
- Porta: `587`
- Autenticação: TLS
- Requisito: Senha normal da conta

**Processo:**
1. Identifica provedor via `EMAIL_PROVIDER`
2. Configura servidor e porta
3. Estabelece conexão TLS
4. Autentica com credenciais
5. Retorna objeto server configurado

##### `criar_corpo_email(self, informacoes_processadas)`
Gera HTML completo para corpo do email.

**Conteúdo:**
- Cabeçalho profissional
- Resumo executivo com estatísticas
- Seções organizadas por tipo
- Estilo inline compatível com clientes de email

##### `enviar_email(self, informacoes_processadas)`
Envia email para todos os destinatários configurados.

**Processo:**
1. Configura servidor SMTP
2. Cria mensagem multipart
3. Adiciona conteúdo HTML
4. Envia para cada destinatário individualmente
5. Registra sucessos e falhas
6. Retorna relatório detalhado

**Retorno:**
```python
{
    'sucesso': bool,
    'destinatarios_sucesso': list,
    'destinatarios_falharam': list,
    'total_enviados': int,
    'total_falharam': int
}
```

##### `enviar_email_simples(self, assunto, corpo_texto)`
Envia email de texto simples (usado para notificações).

**Uso:**
- Notificações de erro
- Notificações de "sem dados"
- Notificações de inicialização

---

### 5. Configuração (config.py)

#### Responsabilidades
- Carregamento de variáveis de ambiente
- Configurações centralizadas
- Validação de parâmetros

**Variáveis de Ambiente Carregadas:**

**Email:**
- `EMAIL_PROVIDER`: gmail ou outlook
- `SMTP_SERVER`: servidor SMTP
- `SMTP_PORT`: porta SMTP
- `EMAIL_USER`: email remetente
- `EMAIL_PASSWORD`: senha
- `DESTINATARIOS`: lista separada por vírgula

**Webcrawler:**
- `BACEN_BASE_URL`: URL base do BACEN
- `BACEN_COMUNICADOS_URL`: URL de comunicados
- `BACEN_RESOLUCOES_URL`: URL de resoluções
- `BACEN_CIRCULARES_URL`: URL de circulares

**Agendamento:**
- `HORA_EXECUCAO`: hora no formato HH:MM
- `FUSO_HORARIO`: timezone (padrão: America/Sao_Paulo)

**Selenium:**
- `HEADLESS_MODE`: true/false
- `TIMEOUT_PAGINA`: segundos (padrão: 30)
- `DELAY_ENTRE_REQUISICOES`: segundos (padrão: 2)

**Carregamento:**
Usa `python-dotenv` para carregar arquivo `.env` automaticamente.

---

## 🔄 Fluxo de Dados

### Fluxo Completo

```
1. AGENDAMENTO/TRIGGER
   │
   ▼
2. SistemaMonitoramentoBACEN.executar_processo_completo()
   │
   ▼
3. WebcrawlerBACEN.executar_coleta()
   │
   ├─▶ buscar_comunicados()
   │   └─▶ Retorna: Lista de dicts
   │
   ├─▶ buscar_resolucoes()
   │   └─▶ Retorna: Lista de dicts
   │
   └─▶ buscar_circulares()
       └─▶ Retorna: Lista de dicts
   │
   └─▶ Consolidado: Lista única
   │
   ▼
4. SumarizadorBACEN.processar_informacoes()
   │
   ├─▶ Para cada documento:
   │   ├─▶ obter_conteudo_completo(url)
   │   │   └─▶ Retorna: Texto completo
   │   │
   │   └─▶ extrair_resumo(texto, titulo)
   │       └─▶ Retorna: Resumo de 10 linhas
   │
   └─▶ Consolidado: Lista processada
   │
   ▼
5. EnviadorEmail.enviar_email()
   │
   ├─▶ criar_corpo_email()
   │   └─▶ Retorna: HTML formatado
   │
   ├─▶ configurar_servidor_smtp()
   │   └─▶ Retorna: Server SMTP configurado
   │
   └─▶ Envia para cada destinatário
   │
   ▼
6. salvar_relatorio_local()
   │
   ├─▶ gerar_relatorio_html()
   │   └─▶ Retorna: HTML completo
   │
   └─▶ Salva em: relatorios/relatorio_bacen_YYYYMMDD.html
   │
   ▼
7. LOG E CONCLUSÃO
```

### Estruturas de Dados

#### Dados Coletados (webcrawler)
```python
[
    {
        'titulo': 'Título do Documento',
        'link': 'https://www.bcb.gov.br/...',
        'data': '01/01/2024',
        'tipo': 'Comunicado'  # ou 'Resolução' ou 'Circular'
    },
    ...
]
```

#### Dados Processados (sumarizador)
```python
[
    {
        'titulo': 'Título do Documento',
        'tipo': 'Comunicado',
        'data': '01/01/2024',
        'link': 'https://www.bcb.gov.br/...',
        'resumo': 'Resumo de 10 linhas...',
        'data_processamento': '01/01/2024 07:15:30'
    },
    ...
]
```

---

## ⚙️ Configuração e Ambiente

### Arquivo .env

**Localização:** Raiz do projeto

**Formato:**
```env
# Configurações de Email
EMAIL_PROVIDER=gmail
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_app
DESTINATARIOS=email1@cielo.com.br,email2@cielo.com.br

# Configurações do Webcrawler
BACEN_BASE_URL=https://www.bcb.gov.br
BACEN_COMUNICADOS_URL=https://www.bcb.gov.br/estabilidadefinanceira/comunicados
BACEN_RESOLUCOES_URL=https://www.bcb.gov.br/estabilidadefinanceira/resolucoes
BACEN_CIRCULARES_URL=https://www.bcb.gov.br/estabilidadefinanceira/circular

# Configurações de Agendamento
HORA_EXECUCAO=07:00
FUSO_HORARIO=America/Sao_Paulo

# Configurações do Selenium
HEADLESS_MODE=true
TIMEOUT_PAGINA=30
DELAY_ENTRE_REQUISICOES=2
```

### Variáveis Críticas

**EMAIL_PASSWORD:**
- **Gmail**: Senha de aplicativo (não senha normal)
- **Outlook**: Senha normal da conta
- **Segurança**: Nunca commitar no Git

**HEADLESS_MODE:**
- `true`: Execução sem interface (servidores)
- `false`: Execução com janela do navegador (debug)

**TIMEOUT_PAGINA:**
- Tempo máximo para carregamento de página
- Aumentar se conexão for lenta

---

## 🛠️ Instalação e Setup

### Pré-requisitos Técnicos

**Sistema Operacional:**
- Windows 10+
- Linux (Ubuntu 18.04+)
- macOS 10.14+

**Software:**
- Python 3.8 ou superior
- Google Chrome (versão recente)
- Git (opcional, para versionamento)

**Acesso:**
- Conexão com internet
- Acesso ao site do BACEN (sem bloqueios)
- Porta SMTP (587) liberada

### Instalação Passo a Passo

#### 1. Verificar Python
```bash
python --version
# Deve retornar: Python 3.8.x ou superior
```

#### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

**Dependências Principais:**
- `selenium==4.15.2`: Automação de navegador
- `webdriver-manager==4.0.1`: Gerenciamento de ChromeDriver
- `beautifulsoup4==4.12.2`: Parsing HTML
- `requests==2.31.0`: Requisições HTTP
- `schedule==1.2.0`: Agendamento de tarefas
- `python-dotenv==1.0.0`: Variáveis de ambiente

#### 3. Configurar Ambiente
```bash
# Copiar exemplo
cp config_example.env .env

# Editar configurações
# (use editor de texto)
```

#### 4. Configurar Gmail (Se aplicável)
1. Acesse: https://myaccount.google.com/security
2. Ative "Verificação em duas etapas"
3. Gere "Senha de aplicativo"
4. Use essa senha em `EMAIL_PASSWORD`

#### 5. Testar Instalação
```bash
python main.py --teste
```

### Script de Instalação Automática

O arquivo `instalar.py` automatiza todo o processo:

**Funcionalidades:**
- Verifica versão do Python
- Instala dependências
- Cria diretórios necessários
- Configura arquivo .env
- Cria scripts de execução
- Gera arquivo de tarefa agendada (Windows)

**Execução:**
```bash
python instalar.py
```

---

## 📁 Estrutura de Código

### Estrutura de Diretórios

```
webcrawler_bacen/
│
├── main.py                    # Orquestrador principal
├── webcrawler.py              # Módulo de coleta
├── sumarizador.py             # Módulo de processamento
├── enviador_email.py          # Módulo de envio
├── config.py                  # Configurações
├── instalar.py                # Script de instalação
│
├── requirements.txt           # Dependências Python
├── config_example.env         # Exemplo de configuração
│
├── relatorios/                # Relatórios HTML gerados
│   └── relatorio_bacen_YYYYMMDD.html
│
├── logs/                      # Arquivos de log
│   ├── sistema_monitoramento.log
│   ├── webcrawler.log
│   ├── sumarizador.log
│   └── enviador_email.log
│
└── docs/                      # Documentação (este arquivo)
```

### Padrões de Código

**Nomenclatura:**
- Classes: PascalCase (`WebcrawlerBACEN`)
- Funções: snake_case (`executar_coleta`)
- Variáveis: UPPER_SNAKE_CASE para constantes (`EMAIL_USER`)

**Documentação:**
- Docstrings em todas as classes e métodos
- Comentários explicativos em lógica complexa
- Logs informativos em operações importantes

**Tratamento de Erros:**
- Try/except em todas as operações críticas
- Logs de erro detalhados
- Continuidade quando possível (não falhar completamente)

---

## 📚 Dependências e Bibliotecas

### Dependências Principais

#### selenium (4.15.2)
- **Uso**: Automação de navegador web
- **Módulos utilizados**: `webdriver`, `By`, `WebDriverWait`, `Options`
- **Alternativas**: Scrapy (mais leve, mas menos flexível)

#### webdriver-manager (4.0.1)
- **Uso**: Download automático do ChromeDriver
- **Benefício**: Não requer instalação manual do driver

#### beautifulsoup4 (4.12.2)
- **Uso**: Parsing e extração de dados HTML
- **Parser**: html.parser (padrão Python)

#### requests (2.31.0)
- **Uso**: Download de conteúdo de páginas
- **Vantagem**: Mais rápido que Selenium para downloads simples

#### schedule (1.2.0)
- **Uso**: Agendamento de tarefas recorrentes
- **Funcionalidade**: Execução diária em horário específico

#### python-dotenv (1.0.0)
- **Uso**: Carregamento de variáveis de ambiente do arquivo .env
- **Benefício**: Separação de configuração e código

### Dependências Secundárias

- **lxml (4.9.3)**: Parser XML/HTML (opcional, melhora performance)
- **pandas (2.1.3)**: Manipulação de dados (futuro uso)
- **openpyxl (3.1.2)**: Exportação Excel (futuro uso)

---

## 📝 Sistema de Logging

### Configuração

Cada módulo configura seu próprio logger:

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nome_do_modulo.log'),
        logging.StreamHandler()  # Também imprime no console
    ]
)
```

### Arquivos de Log

**sistema_monitoramento.log:**
- Log principal do sistema
- Execução de processos
- Erros globais

**webcrawler.log:**
- Operações de coleta
- Erros de Selenium
- URLs acessadas

**sumarizador.log:**
- Processamento de documentos
- Erros de download
- Geração de resumos

**enviador_email.log:**
- Tentativas de envio
- Sucessos e falhas
- Configuração SMTP

### Níveis de Log

- **INFO**: Operações normais, progresso
- **WARNING**: Situações não críticas, mas anormais
- **ERROR**: Erros que impedem funcionalidade
- **DEBUG**: Informações detalhadas (não usado atualmente)

### Rotação de Logs

**Recomendação:** Implementar rotação para evitar crescimento excessivo:
- Manter últimos 30 dias
- Compactar logs antigos
- Limpar logs muito antigos

---

## ⚠️ Tratamento de Erros

### Estratégias de Tratamento

#### 1. Falha de Coleta
**Situação:** Webcrawler não consegue coletar dados

**Tratamento:**
- Log de erro detalhado
- Envio de notificação de erro por email
- Sistema continua tentando (não encerra)

#### 2. Falha de Processamento
**Situação:** Sumarizador não consegue processar um documento

**Tratamento:**
- Log do erro específico
- Continua com próximos documentos
- Lista final pode ter menos itens, mas não falha completamente

#### 3. Falha de Envio de Email
**Situação:** Não consegue enviar para um ou mais destinatários

**Tratamento:**
- Tenta enviar para cada destinatário individualmente
- Registra quais falharam e quais sucederam
- Retorna relatório detalhado
- Não interrompe se pelo menos um envio funcionar

#### 4. Falha de Driver Selenium
**Situação:** ChromeDriver não inicializa

**Tratamento:**
- Log de erro com detalhes do sistema
- Tentativa de re-download pelo webdriver-manager
- Se persistir, notificação de erro

#### 5. Timeout de Requisição
**Situação:** Página demora muito para carregar

**Tratamento:**
- Timeout configurável (padrão: 30s)
- Log de timeout
- Retorna lista vazia para aquele tipo de documento

### Pontos de Recuperação

1. **Coleta Parcial**: Se um tipo de documento falhar, outros ainda são coletados
2. **Processamento Parcial**: Se um documento falhar, outros ainda são processados
3. **Envio Parcial**: Se alguns destinatários falharem, outros ainda recebem

---

## ⏰ Agendamento e Execução

### Mecanismo de Agendamento

**Biblioteca:** `schedule`

**Configuração:**
```python
schedule.every().day.at("07:00").do(executar_processo_completo)
```

**Execução:**
```python
while True:
    schedule.run_pending()
    time.sleep(60)  # Verifica a cada minuto
```

### Modos de Execução

#### 1. Execução de Teste
```bash
python main.py --teste
```
- Executa processo completo uma vez
- Útil para validação e debug
- Não agenda execuções futuras

#### 2. Execução com Agendador
```bash
python main.py --agendador
```
- Inicia agendamento automático
- Executa diariamente no horário configurado
- Mantém processo em execução contínua
- Envia notificação de inicialização

#### 3. Execução Manual Única
```bash
python main.py
```
- Executa processo completo uma vez
- Não agenda execuções futuras

### Agendamento no Windows

**Opção 1: Script de Execução**
- Arquivo `executar_sistema.bat`
- Executa `main.py --agendador`
- Pode ser colocado na inicialização do Windows

**Opção 2: Tarefa Agendada do Windows**
- Arquivo `MonitoramentoBACEN.xml` gerado
- Comando para instalar:
```bash
schtasks /create /xml MonitoramentoBACEN.xml /tn MonitoramentoBACEN
```
- Executa automaticamente no horário configurado

### Agendamento no Linux

**Opção 1: systemd Service**
Criar arquivo `/etc/systemd/system/bacen-monitor.service`:

```ini
[Unit]
Description=Sistema de Monitoramento BACEN
After=network.target

[Service]
Type=simple
User=usuario
WorkingDirectory=/caminho/para/projeto
ExecStart=/usr/bin/python3 main.py --agendador
Restart=always

[Install]
WantedBy=multi-user.target
```

**Opção 2: Cron**
```bash
# Editar crontab
crontab -e

# Adicionar linha (executa às 07:00 diariamente)
0 7 * * * cd /caminho/para/projeto && python3 main.py --teste
```

---

## 🔌 Integração com Serviços Externos

### Banco Central do Brasil (BACEN)

**URLs Utilizadas:**
- Comunicados: `/estabilidadefinanceira/comunicados`
- Resoluções: `/estabilidadefinanceira/resolucoes`
- Circulares: `/estabilidadefinanceira/circular`

**Características:**
- Site dinâmico (requer JavaScript)
- Necessita Selenium para renderização completa
- Estrutura pode mudar (requer manutenção)

**Limitações:**
- Rate limiting: Respeitado com `DELAY_ENTRE_REQUISICOES`
- Timeout: Configurável via `TIMEOUT_PAGINA`
- Bloqueio de IP: Não implementado, mas possível

### Servidores SMTP

#### Gmail
- **Servidor**: `smtp.gmail.com`
- **Porta**: `587` (TLS)
- **Autenticação**: Senha de aplicativo obrigatória
- **Limite**: 500 emails/dia (gratuito)

#### Outlook
- **Servidor**: `smtp-mail.outlook.com`
- **Porta**: `587` (TLS)
- **Autenticação**: Senha normal da conta
- **Limite**: 300 emails/dia (gratuito)

### Considerações de Integração

**Resiliência:**
- Timeouts adequados
- Retry não implementado (futuro)
- Fallback entre provedores não implementado

**Segurança:**
- Credenciais em arquivo `.env` (não versionado)
- TLS/STARTTLS para SMTP
- Validação de certificados SSL

---

## 🔒 Segurança

### Gerenciamento de Credenciais

**Arquivo .env:**
- Não versionado no Git (deve estar no .gitignore)
- Permissões restritas (chmod 600 em Linux)
- Não compartilhado publicamente

**Senhas:**
- Gmail: Senha de aplicativo (mais seguro que senha normal)
- Outlook: Senha normal (única opção disponível)

### Segurança de Comunicação

**SMTP:**
- Uso obrigatório de TLS/STARTTLS
- Porta 587 (segura)
- Evita porta 25 (não criptografada)

**HTTP/HTTPS:**
- Todas as URLs do BACEN usam HTTPS
- Validação de certificados SSL habilitada

### Segurança do Código

**Input Validation:**
- URLs do BACEN são fixas (não há input do usuário)
- Destinatários validados como formato de email

**Path Traversal:**
- Nomes de arquivo gerados com data (formato controlado)
- Não há input de caminhos do usuário

### Recomendações de Segurança

1. **Senha de Aplicativo**: Sempre usar para Gmail
2. **Rotação de Senhas**: Periódica (conforme política)
3. **Auditoria**: Revisar logs regularmente
4. **Firewall**: Permitir apenas portas necessárias
5. **Backup**: Manter backup de configurações (criptografado)

---

## 🔧 Manutenção e Troubleshooting

### Problemas Comuns

#### 1. ChromeDriver Desatualizado

**Sintoma:**
```
selenium.common.exceptions.SessionNotCreatedException
```

**Solução:**
```bash
pip install --upgrade webdriver-manager
# O webdriver-manager baixa automaticamente a versão correta
```

#### 2. Email Não Envia (Gmail)

**Sintoma:**
```
smtplib.SMTPAuthenticationError
```

**Soluções:**
1. Verificar se senha de aplicativo está correta
2. Confirmar verificação em duas etapas ativa
3. Verificar se "Acesso a apps menos seguros" não está desabilitado (antigo)

#### 3. Timeout ao Acessar BACEN

**Sintoma:**
```
TimeoutException ou requests timeout
```

**Soluções:**
1. Aumentar `TIMEOUT_PAGINA` no `.env`
2. Verificar conexão com internet
3. Verificar se site do BACEN está acessível
4. Verificar firewall/proxy

#### 4. Nenhum Documento Encontrado

**Sintoma:**
- Sistema executa, mas lista vazia

**Diagnóstico:**
1. Verificar data do sistema (deve estar correta)
2. Verificar se há documentos no BACEN naquela data
3. Verificar se seletores CSS ainda estão corretos (site pode ter mudado)

**Verificação Manual:**
```python
from webcrawler import WebcrawlerBACEN
crawler = WebcrawlerBACEN()
crawler.setup_driver()
comunicados = crawler.buscar_comunicados()
print(comunicados)
```

#### 5. Sistema Não Executa no Agendamento

**Sintoma:**
- Tarefa agendada não executa

**Soluções:**
1. Verificar logs do sistema
2. Verificar permissões do usuário
3. Verificar se Python está no PATH
4. Testar execução manual primeiro

### Monitoramento Proativo

**Checklist Diário (Automatizado):**
- [ ] Verificar execução do dia (via email recebido)
- [ ] Verificar logs para erros
- [ ] Verificar relatórios gerados

**Checklist Semanal:**
- [ ] Revisar tamanho dos logs
- [ ] Verificar espaço em disco
- [ ] Atualizar dependências se necessário

**Checklist Mensal:**
- [ ] Verificar se URLs do BACEN ainda estão corretas
- [ ] Testar execução completa manual
- [ ] Revisar credenciais (expiração)

### Limpeza e Manutenção

**Rotação de Logs:**
```bash
# Script de exemplo (Linux)
find logs/ -name "*.log" -mtime +30 -delete
```

**Limpeza de Relatórios:**
```bash
# Manter últimos 90 dias
find relatorios/ -name "*.html" -mtime +90 -delete
```

**Backup:**
```bash
# Backup mensal
tar -czf backup_bacen_$(date +%Y%m).tar.gz relatorios/ logs/
```

---

## 🔄 Extensibilidade

### Pontos de Extensão

#### 1. Novos Tipos de Documentos

**Onde:** `webcrawler.py`

**Como:**
```python
def buscar_novo_tipo(self):
    # Implementar busca similar às existentes
    # Retornar lista com tipo 'NovoTipo'
    pass
```

**Integração:**
- Adicionar método em `executar_coleta()`
- Não requer mudanças em outros módulos (polimorfismo)

#### 2. Novos Formatos de Saída

**Onde:** `sumarizador.py`

**Como:**
```python
def gerar_relatorio_pdf(self, informacoes_processadas):
    # Usar biblioteca como reportlab
    pass
```

#### 3. Novos Destinos

**Onde:** Criar novo módulo ou estender `enviador_email.py`

**Exemplos:**
- Webhook (Slack, Teams)
- API REST
- Banco de dados
- Sistema de arquivos compartilhado

#### 4. Melhorias no Resumo

**Onde:** `sumarizador.py -> extrair_resumo()`

**Possibilidades:**
- Integração com API de NLP (OpenAI, etc.)
- Machine Learning para relevância
- Análise de sentimento
- Extração de entidades nomeadas

#### 5. Notificações Adicionais

**Onde:** `main.py`

**Como:**
```python
def enviar_notificacao_customizada(self, tipo, dados):
    # Integrar com Slack, Teams, SMS, etc.
    pass
```

### Arquitetura para Extensibilidade

**Princípios:**
1. **Módulos independentes**: Cada módulo pode ser modificado sem afetar outros
2. **Interfaces claras**: Estruturas de dados bem definidas
3. **Configuração externa**: Mudanças via `.env` quando possível
4. **Logging extensivo**: Facilita debug de novas funcionalidades

### Exemplo de Extensão: Webhook

```python
# novo_arquivo: notificador_webhook.py

import requests
from config import WEBHOOK_URL

class NotificadorWebhook:
    def enviar_webhook(self, informacoes_processadas):
        payload = {
            'data': datetime.now().isoformat(),
            'documentos': informacoes_processadas
        }
        requests.post(WEBHOOK_URL, json=payload)
```

**Integração:**
```python
# Em main.py
from notificador_webhook import NotificadorWebhook

class SistemaMonitoramentoBACEN:
    def __init__(self):
        # ... código existente ...
        self.notificador_webhook = NotificadorWebhook()
    
    def executar_processo_completo(self):
        # ... código existente ...
        self.notificador_webhook.enviar_webhook(informacoes_processadas)
```

---

## 📊 Métricas e Monitoramento

### Métricas Sugeridas (Não Implementadas)

**Performance:**
- Tempo de execução total
- Tempo por módulo
- Número de requisições HTTP

**Qualidade:**
- Taxa de sucesso de coleta
- Taxa de sucesso de processamento
- Taxa de sucesso de envio

**Negócio:**
- Número de documentos por tipo
- Tendência ao longo do tempo
- Alertas quando número de documentos muda drasticamente

### Implementação Futura

**Sugestão:** Adicionar métricas em arquivo JSON:

```python
{
    "data_execucao": "2024-01-01 07:00:00",
    "tempo_total_segundos": 125.5,
    "documentos_coletados": 5,
    "documentos_processados": 5,
    "emails_enviados": 3,
    "emails_falharam": 0,
    "status": "sucesso"
}
```

---

## 📞 Suporte Técnico

### Informações para Troubleshooting

Quando reportar problemas, incluir:

1. **Versão do Python:**
   ```bash
   python --version
   ```

2. **Sistema Operacional:**
   ```bash
   # Linux/Mac
   uname -a
   
   # Windows
   systeminfo
   ```

3. **Logs Relevantes:**
   - Últimas 50 linhas de cada log

4. **Configuração (sem senhas):**
   - Valores de `.env` (com senhas mascaradas)

5. **Comando Executado:**
   - Exatamente o que foi executado
   - Argumentos passados

### Canais de Suporte

- **Email**: Equipe de TI
- **Logs**: Sempre verificar primeiro
- **Documentação**: Este arquivo e README.md

---

**Documentação Técnica - Sistema de Monitoramento BACEN**  
Versão 1.0  
Última atualização: 2024


