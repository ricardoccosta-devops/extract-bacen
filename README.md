# Sistema de Monitoramento BACEN - Cielo

Sistema automatizado para monitoramento diário de comunicados, resoluções e circulares do Banco Central do Brasil (BACEN), com envio automático de relatórios por email.

## 🚀 Características

- **Webcrawler automatizado** usando Selenium para buscar informações do BACEN
- **Busca baseada na data do sistema operacional** do servidor
- **Sumarização inteligente** com resumos de 10 linhas por tópico
- **Envio automático de emails** para lista de destinatários configurável
- **Suporte a múltiplos provedores** (Gmail e Outlook)
- **Agendamento diário** para execução às 07:00 (horário Brasil)
- **Relatórios HTML** formatados e profissionais
- **Sistema modular** com componentes independentes
- **Logs detalhados** para monitoramento e troubleshooting

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Google Chrome instalado
- Conta de email Gmail com senha de aplicativo configurada
- Conexão com internet

## 🛠️ Instalação

### Instalação Automática

Execute o script de instalação:

```bash
python instalar.py
```

O script irá:
- Verificar a versão do Python
- Instalar todas as dependências
- Criar diretórios necessários
- Configurar arquivos de ambiente
- Criar scripts de execução
- Configurar agendamento (Windows)

### Instalação Manual

1. **Clone ou baixe o projeto**

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure o ambiente:**
```bash
# Copie o arquivo de exemplo
cp config_example.env .env

# Edite o arquivo .env com suas credenciais
```

4. **Crie os diretórios necessários:**
```bash
mkdir relatorios logs
```

## ⚙️ Configuração

### Arquivo .env

Configure suas credenciais no arquivo `.env`:

```env
# Configurações de Email
EMAIL_PROVIDER=gmail
# Opções: gmail ou outlook

# Para Gmail (padrão)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_app

# Para Outlook (descomente e configure)
# SMTP_SERVER=smtp-mail.outlook.com
# SMTP_PORT=587
# EMAIL_USER=seu_email@outlook.com
# EMAIL_PASSWORD=sua_senha_normal

# Lista de destinatários (separados por vírgula)
DESTINATARIOS=destinatario1@cielo.com.br,destinatario2@cielo.com.br

# Configurações de Agendamento
HORA_EXECUCAO=07:00
FUSO_HORARIO=America/Sao_Paulo

# Configurações do Selenium
HEADLESS_MODE=true
TIMEOUT_PAGINA=30
DELAY_ENTRE_REQUISICOES=2
```

### Configuração do Gmail

Para usar o Gmail como servidor SMTP:

1. Ative a verificação em duas etapas na sua conta Google
2. Gere uma senha de aplicativo específica
3. Use essa senha no campo `EMAIL_PASSWORD`
4. Configure `EMAIL_PROVIDER=gmail`

### Configuração do Outlook

Para usar o Outlook/Hotmail como servidor SMTP:

1. Use sua senha normal da conta Microsoft
2. Configure `EMAIL_PROVIDER=outlook`
3. Use `SMTP_SERVER=smtp-mail.outlook.com`
4. Porta padrão: `587`

## 🚀 Uso

### Execução de Teste

Para testar o sistema:

```bash
python main.py --teste
```

### Execução Manual

Para executar uma vez:

```bash
python main.py
```

### Execução com Agendamento

Para executar com agendamento automático:

```bash
python main.py --agendador
```

### Scripts de Execução

- **Windows:** `executar_sistema.bat`
- **Linux/Mac:** `./executar_sistema.sh`

## 📁 Estrutura do Projeto

```
webcrawler_bacen/
├── main.py                 # Arquivo principal e agendador
├── webcrawler.py           # Módulo de webcrawling
├── sumarizador.py          # Módulo de sumarização
├── enviador_email.py       # Módulo de envio de emails
├── config.py               # Configurações do sistema
├── requirements.txt        # Dependências Python
├── instalar.py            # Script de instalação
├── config_example.env     # Exemplo de configuração
├── relatorios/            # Relatórios HTML gerados
├── logs/                  # Arquivos de log
└── README.md              # Este arquivo
```

## 🔧 Módulos do Sistema

### 1. Webcrawler (`webcrawler.py`)

- Busca comunicados, resoluções e circulares do BACEN
- Usa Selenium com Chrome headless
- Filtra documentos do dia anterior
- Retorna lista estruturada de informações

### 2. Sumarizador (`sumarizador.py`)

- Processa o conteúdo completo de cada documento
- Extrai resumos relevantes de 10 linhas
- Usa palavras-chave para identificar conteúdo importante
- Gera relatórios HTML formatados

### 3. Enviador de Email (`enviador_email.py`)

- Envia relatórios por email em formato HTML
- Suporte a múltiplos destinatários
- Tratamento de erros de envio
- Notificações de sistema (erros, sem dados)

### 4. Sistema Principal (`main.py`)

- Orquestra todos os módulos
- Gerencia agendamento diário
- Tratamento de erros e logs
- Notificações de status

## 📊 Funcionamento

1. **07:00** - Sistema executa automaticamente
2. **Coleta** - Busca documentos da data atual do sistema operacional no BACEN
3. **Processamento** - Analisa e sumariza cada documento
4. **Relatório** - Gera relatório HTML formatado
5. **Envio** - Envia email para lista de destinatários
6. **Logs** - Registra todas as operações

## 📧 Formato do Email

O email enviado contém:

- **Cabeçalho** com data e informações do sistema
- **Resumo executivo** com contadores por tipo
- **Seções organizadas** por tipo de documento
- **Resumos de 10 linhas** para cada documento
- **Links diretos** para documentos completos
- **Rodapé** com informações do sistema

## 🔍 Monitoramento

### Logs

O sistema gera logs detalhados em:

- `sistema_monitoramento.log` - Log principal
- `webcrawler.log` - Log do webcrawler
- `sumarizador.log` - Log do sumarizador
- `enviador_email.log` - Log do envio de emails

### Relatórios Locais

Relatórios HTML são salvos em `relatorios/` com nome:
`relatorio_bacen_YYYYMMDD.html`

## ⚠️ Solução de Problemas

### Erro de Driver do Chrome

```bash
# Reinstale o ChromeDriver
pip install --upgrade webdriver-manager
```

### Erro de Email

1. Verifique as credenciais no `.env`
2. Confirme se a senha de aplicativo está correta
3. Verifique se a verificação em duas etapas está ativa

### Erro de Conexão

1. Verifique a conexão com internet
2. Confirme se os URLs do BACEN estão corretos
3. Verifique se não há firewall bloqueando

### Sistema não executa

1. Verifique os logs para erros
2. Execute um teste manual: `python main.py --teste`
3. Verifique se todas as dependências estão instaladas

## 🔄 Manutenção

### Atualização de Dependências

```bash
pip install --upgrade -r requirements.txt
```

### Limpeza de Logs

```bash
# Limpe logs antigos (opcional)
find logs/ -name "*.log" -mtime +30 -delete
```

### Backup de Relatórios

```bash
# Faça backup dos relatórios (opcional)
tar -czf relatorios_backup_$(date +%Y%m%d).tar.gz relatorios/
```

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique os logs do sistema
2. Execute testes manuais
3. Consulte este README
4. Entre em contato com a equipe de TI

## 📄 Licença

Sistema desenvolvido para uso interno da Cielo.

---

**Sistema de Monitoramento BACEN - Cielo**  
Desenvolvido para automatizar o monitoramento de regulamentações do Banco Central do Brasil.
