# 👤 MANUAL DO USUÁRIO - Sistema de Monitoramento BACEN

## 📋 Índice

1. [Apresentação](#apresentação)
2. [O que é o Sistema](#o-que-é-o-sistema)
3. [Requisitos do Sistema](#requisitos-do-sistema)
4. [Instalação Passo a Passo](#instalação-passo-a-passo)
5. [Configuração Inicial](#configuração-inicial)
6. [Primeira Execução](#primeira-execução)
7. [Uso Diário](#uso-diário)
8. [Interpretando os Resultados](#interpretando-os-resultados)
9. [Problemas Comuns e Soluções](#problemas-comuns-e-soluções)
10. [Manutenção Básica](#manutenção-básica)
11. [Dúvidas Frequentes](#dúvidas-frequentes)
12. [Glossário](#glossário)

---

## 🎯 Apresentação

Bem-vindo ao **Sistema de Monitoramento BACEN**!

Este sistema foi desenvolvido para automatizar o monitoramento diário de comunicados, resoluções e circulares publicados pelo Banco Central do Brasil (BACEN) e enviar relatórios resumidos por email.

### Benefícios

✅ **Automatização Completa**: Não precisa acessar o site do BACEN manualmente  
✅ **Economia de Tempo**: Recebe resumos prontos no email  
✅ **Atualização Diária**: Recebe informações todos os dias automaticamente  
✅ **Resumos Inteligentes**: Cada documento vem com um resumo de 10 linhas  
✅ **Organização**: Documentos organizados por tipo (Comunicados, Resoluções, Circulares)

---

## 📖 O que é o Sistema

### Funcionamento em Resumo

O sistema funciona como um "robô" que:

1. **Acessa o site do BACEN** automaticamente todos os dias
2. **Busca os documentos** publicados na data atual
3. **Lê o conteúdo** de cada documento
4. **Cria resumos** de 10 linhas para cada um
5. **Organiza tudo** em um relatório HTML bonito
6. **Envia por email** para as pessoas cadastradas
7. **Salva localmente** para consulta posterior

### O que o Sistema Monitora

O sistema busca três tipos de documentos no site do BACEN:

1. **Comunicados**: Avisos e informações importantes do Banco Central
2. **Resoluções**: Normas e regras estabelecidas pelo BACEN
3. **Circulares**: Orientações e diretrizes para o setor financeiro

### Quando o Sistema Executa

- **Horário padrão**: Todos os dias às 07:00 (manhã)
- **Horário configurável**: Você pode alterar no arquivo de configuração
- **Execução manual**: Você também pode executar quando quiser para testar

---

## 💻 Requisitos do Sistema

### O que Você Precisa Ter

#### Software Necessário

1. **Python 3.8 ou superior**
   - Como verificar: Abra o terminal/comando e digite `python --version`
   - Se não tiver: Baixe em https://www.python.org/downloads/

2. **Google Chrome**
   - O sistema usa o Chrome para acessar o site do BACEN
   - Baixe em: https://www.google.com/chrome/

3. **Conexão com Internet**
   - O sistema precisa de internet para funcionar

4. **Conta de Email**
   - Gmail (recomendado) OU Outlook/Hotmail
   - Para enviar os relatórios

#### Conhecimentos Necessários

- **Básico**: Saber abrir arquivos de texto, copiar e colar
- **Intermediário**: Saber usar terminal/comando (opcional, mas recomendado)
- **Não precisa**: Conhecimento de programação!

---

## 🚀 Instalação Passo a Passo

### Método 1: Instalação Automática (Recomendado)

Esta é a forma mais fácil de instalar o sistema!

#### Passo 1: Baixar o Sistema

1. Baixe todos os arquivos do sistema
2. Extraia em uma pasta (exemplo: `C:\SistemaBACEN` ou `~/SistemaBACEN`)

#### Passo 2: Abrir o Terminal/Comando

**Windows:**
- Pressione `Win + R`
- Digite `cmd` e pressione Enter
- Navegue até a pasta do sistema: `cd C:\SistemaBACEN`

**Linux/Mac:**
- Abra o Terminal
- Navegue até a pasta: `cd ~/SistemaBACEN`

#### Passo 3: Executar Instalação

Digite o comando:
```bash
python instalar.py
```

O sistema irá:
- ✅ Verificar se o Python está instalado
- ✅ Instalar todas as dependências automaticamente
- ✅ Criar as pastas necessárias
- ✅ Criar arquivo de configuração
- ✅ Criar scripts de execução

**Aguarde** a conclusão da instalação. Pode levar alguns minutos na primeira vez.

#### Passo 4: Verificar Instalação

Se tudo deu certo, você verá uma mensagem:
```
✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!
```

---

### Método 2: Instalação Manual

Se preferir instalar manualmente ou se a instalação automática der erro:

#### Passo 1: Instalar Dependências

```bash
pip install -r requirements.txt
```

#### Passo 2: Criar Pastas

**Windows:**
```bash
mkdir relatorios
mkdir logs
```

**Linux/Mac:**
```bash
mkdir -p relatorios logs
```

#### Passo 3: Configurar Ambiente

```bash
# Copiar arquivo de exemplo
copy config_example.env .env
```

**Linux/Mac:**
```bash
cp config_example.env .env
```

---

## ⚙️ Configuração Inicial

### Configurando o Email

Esta é a parte mais importante! O sistema precisa de um email para enviar os relatórios.

#### Passo 1: Abrir o Arquivo de Configuração

1. Abra a pasta do sistema
2. Procure pelo arquivo chamado `.env`
   - Se não existir, copie o arquivo `config_example.env` e renomeie para `.env`
3. Abra o arquivo `.env` com um editor de texto (Bloco de Notas, VS Code, etc.)

#### Passo 2: Escolher o Provedor de Email

No arquivo `.env`, você verá uma linha assim:
```env
EMAIL_PROVIDER=gmail
```

**Opções:**
- `gmail` - Se você usa Gmail
- `outlook` - Se você usa Outlook ou Hotmail

#### Passo 3: Configurar Gmail

Se escolheu Gmail, você precisa usar uma **senha de aplicativo** (não a senha normal da sua conta).

**Como criar senha de aplicativo no Gmail:**

1. Acesse: https://myaccount.google.com/security
2. Certifique-se de que a **Verificação em duas etapas** está ativada
   - Se não estiver, ative primeiro
3. Role a página até encontrar **Senhas de aplicativo**
4. Clique em **Gerar senha de aplicativo**
5. Escolha um nome (ex: "Sistema BACEN") e clique em **Gerar**
6. **Copie a senha gerada** (ela aparece apenas uma vez!)

**Agora configure no arquivo .env:**

```env
EMAIL_PROVIDER=gmail
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=seu_email@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop  # Cole aqui a senha de aplicativo (sem espaços ou com espaços, ambos funcionam)
```

#### Passo 4: Configurar Outlook

Se escolheu Outlook/Hotmail, use sua senha normal da conta.

```env
EMAIL_PROVIDER=outlook
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
EMAIL_USER=seu_email@outlook.com
EMAIL_PASSWORD=sua_senha_normal  # Sua senha normal da conta Microsoft
```

#### Passo 5: Configurar Destinatários

Esta é a lista de emails que vão receber os relatórios diários.

No arquivo `.env`, encontre a linha:
```env
DESTINATARIOS=email1@cielo.com.br,email2@cielo.com.br,email3@cielo.com.br
```

**Substitua** pelos emails reais, separados por vírgula (sem espaços entre vírgulas).

**Exemplo:**
```env
DESTINATARIOS=joao.silva@cielo.com.br,maria.santos@cielo.com.br,pedro.oliveira@cielo.com.br
```

#### Passo 6: Configurar Horário de Execução (Opcional)

Por padrão, o sistema executa às 07:00 todos os dias.

Para mudar, altere a linha:
```env
HORA_EXECUCAO=07:00
```

**Exemplos:**
- `08:00` - Às 8 da manhã
- `09:30` - Às 9h30
- `18:00` - Às 6 da tarde

#### Passo 7: Salvar o Arquivo

Salve o arquivo `.env` após fazer todas as alterações.

**⚠️ IMPORTANTE:** 
- Nunca compartilhe o arquivo `.env` com outras pessoas
- Ele contém suas senhas!
- Não envie por email ou mensagem

---

## 🧪 Primeira Execução

### Testando o Sistema

Antes de colocar em produção, é muito importante testar!

#### Passo 1: Executar Teste

Abra o terminal/comando na pasta do sistema e execute:

```bash
python main.py --teste
```

O sistema irá:
1. Acessar o site do BACEN
2. Buscar documentos do dia
3. Processar informações
4. Enviar email de teste
5. Salvar relatório local

**Tempo estimado:** 2 a 5 minutos

#### Passo 2: Verificar Resultado

**O que verificar:**

1. **No Terminal:**
   - Procure por mensagens de erro
   - Deve aparecer "✅" para sucessos
   - Se aparecer "❌", há um problema

2. **No Email:**
   - Verifique a caixa de entrada
   - Deve ter recebido um email com o relatório
   - Se não recebeu, verifique a pasta de spam

3. **Na Pasta `relatorios/`:**
   - Deve ter um arquivo HTML com o relatório do dia
   - Abra no navegador para visualizar

#### Passo 3: Verificar Logs (Se Houver Problema)

Se algo não funcionou, verifique os logs:

**Arquivos de log importantes:**
- `sistema_monitoramento.log` - Log geral
- `webcrawler.log` - Problemas de acesso ao site
- `enviador_email.log` - Problemas de envio de email

Abra esses arquivos e veja as últimas linhas para identificar o problema.

---

## 📅 Uso Diário

### Execução Automática (Recomendado)

O sistema foi projetado para funcionar automaticamente, sem intervenção manual.

#### Opção 1: Agendamento com Script

**Windows:**

1. Execute o arquivo `executar_sistema.bat`
   - Pode criar um atalho na área de trabalho
   - O sistema ficará rodando em segundo plano

2. **Para executar automaticamente ao ligar o computador:**
   - Pressione `Win + R`
   - Digite `shell:startup`
   - Copie o atalho do `executar_sistema.bat` para essa pasta

**Linux/Mac:**

1. Execute o script:
```bash
chmod +x executar_sistema.sh
./executar_sistema.sh
```

2. **Para executar automaticamente:**
   - Use o crontab ou systemd (requer conhecimento técnico)
   - Consulte a documentação técnica para detalhes

#### Opção 2: Tarefa Agendada do Windows

**Windows possui uma ferramenta nativa para agendar tarefas:**

1. Abra o **Agendador de Tarefas**
   - Pressione `Win + R`, digite `taskschd.msc`

2. Clique em **Criar Tarefa Básica**

3. Configure:
   - **Nome**: Sistema BACEN
   - **Gatilho**: Diariamente, às 07:00
   - **Ação**: Iniciar programa
   - **Programa**: `python`
   - **Argumentos**: `main.py --teste`
   - **Diretório**: Caminho da pasta do sistema

**OU use o arquivo XML gerado:**

Se você executou `instalar.py`, foi gerado um arquivo `MonitoramentoBACEN.xml`.

Para instalar a tarefa agendada:

1. Abra o **Prompt de Comando como Administrador**
2. Navegue até a pasta do sistema
3. Execute:
```bash
schtasks /create /xml MonitoramentoBACEN.xml /tn MonitoramentoBACEN
```

### Execução Manual

Se precisar executar manualmente:

```bash
python main.py --teste
```

**Use quando:**
- Quiser testar novamente
- Houver problema no agendamento
- Precisar de um relatório imediato

### O que Acontece Diariamente

Todos os dias, no horário configurado:

1. **07:00** - Sistema inicia automaticamente
2. **07:00-07:05** - Acessa o site do BACEN e busca documentos
3. **07:05-07:10** - Processa e cria resumos
4. **07:10** - Envia emails para todos os destinatários
5. **07:10** - Salva relatório local

**Você não precisa fazer nada!** Apenas aguardar o email.

---

## 📧 Interpretando os Resultados

### Entendendo o Email Recebido

Quando você recebe o email do sistema, ele contém:

#### 1. Cabeçalho

```
Relatório Diário - Banco Central do Brasil
Comunicados, Resoluções e Circulares do dia DD/MM/AAAA
```

#### 2. Resumo Executivo

Uma caixa azul com:
- **Total de documentos encontrados**: Quantos documentos foram publicados
- **Comunicados**: Quantos comunicados
- **Resoluções**: Quantas resoluções
- **Circulares**: Quantas circulares
- **Data de processamento**: Quando o relatório foi gerado

#### 3. Seções por Tipo

O email é dividido em três seções:

**COMUNICADOS**
- Lista todos os comunicados do dia
- Cada comunicado tem:
  - Título
  - Data
  - Resumo de 10 linhas
  - Link para documento completo

**RESOLUÇÕES**
- Mesma estrutura dos comunicados

**CIRCULARES**
- Mesma estrutura dos comunicados

#### 4. Quando Não Há Documentos

Se não houver documentos em um tipo, aparecerá:
```
COMUNICADOS
Nenhum comunicado encontrado para o dia de hoje.
```

**Isso é normal!** Nem sempre há documentos publicados todos os dias.

### Relatório Local

Além do email, o sistema salva um relatório HTML na pasta `relatorios/`.

**Nome do arquivo:**
```
relatorio_bacen_20240101.html
```
(Onde `20240101` é a data no formato AAAAMMDD)

**Para visualizar:**
1. Abra a pasta `relatorios/`
2. Clique duas vezes no arquivo HTML
3. Abrirá no navegador com formatação completa

**Vantagem:** 
- Pode ser compartilhado com outras pessoas
- Não depende do email
- Pode ser impresso

---

## 🔧 Problemas Comuns e Soluções

### Problema 1: "Email não enviado"

**Sintomas:**
- Sistema executa, mas ninguém recebe email
- Aparece erro relacionado a SMTP no log

**Soluções:**

**Para Gmail:**
1. Verifique se está usando **senha de aplicativo** (não senha normal)
2. Confirme que a verificação em duas etapas está ativada
3. Verifique se copiou a senha corretamente (sem espaços extras)
4. Tente gerar uma nova senha de aplicativo

**Para Outlook:**
1. Verifique se a senha está correta
2. Tente fazer login manual no site do Outlook para confirmar a senha
3. Verifique se a conta não está bloqueada

**Geral:**
1. Verifique se os destinatários estão corretos no arquivo `.env`
2. Verifique se há vírgulas extras ou faltando
3. Veja o arquivo `enviador_email.log` para detalhes do erro

### Problema 2: "Nenhum documento encontrado"

**Sintomas:**
- Sistema executa, mas lista está vazia
- Email diz "Nenhum documento encontrado"

**Soluções:**

1. **Verificar se realmente há documentos:**
   - Acesse manualmente o site do BACEN
   - Veja se há documentos publicados na data atual

2. **Verificar data do sistema:**
   - Certifique-se de que a data do computador está correta
   - O sistema usa a data do sistema operacional

3. **Site pode ter mudado:**
   - O site do BACEN pode ter mudado sua estrutura
   - Entre em contato com a equipe de TI para atualizar

### Problema 3: "Erro ao acessar site do BACEN"

**Sintomas:**
- Timeout ao carregar página
- Erro de conexão

**Soluções:**

1. **Verificar conexão com internet:**
   - Teste acessar https://www.bcb.gov.br no navegador

2. **Aumentar timeout:**
   - No arquivo `.env`, aumente o valor:
   ```env
   TIMEOUT_PAGINA=60  # Aumentar de 30 para 60 segundos
   ```

3. **Verificar firewall:**
   - Firewall pode estar bloqueando
   - Adicione exceção para Python

4. **Tentar mais tarde:**
   - Site do BACEN pode estar temporariamente indisponível

### Problema 4: "ChromeDriver erro"

**Sintomas:**
- Erro relacionado a ChromeDriver
- Sistema não consegue abrir o navegador

**Soluções:**

1. **Atualizar webdriver-manager:**
```bash
pip install --upgrade webdriver-manager
```

2. **Verificar Chrome instalado:**
   - Certifique-se de que o Google Chrome está instalado
   - Atualize o Chrome para a versão mais recente

3. **Reinstalar dependências:**
```bash
pip install --upgrade -r requirements.txt
```

### Problema 5: "Sistema não executa automaticamente"

**Sintomas:**
- Agendamento configurado, mas não executa
- Tarefa agendada não roda

**Soluções:**

1. **Verificar se Python está no PATH:**
   - Tente executar `python` no terminal
   - Se não funcionar, precisa adicionar ao PATH

2. **Verificar permissões:**
   - Usuário precisa ter permissão para executar Python
   - No Windows, pode precisar executar como administrador

3. **Testar execução manual:**
   - Execute `python main.py --teste` manualmente
   - Se funcionar, o problema é só no agendamento

4. **Verificar logs do Windows:**
   - No Agendador de Tarefas, veja o histórico da tarefa
   - Verifique se há erros registrados

### Problema 6: "Logs muito grandes"

**Sintomas:**
- Pastas de logs ocupando muito espaço
- Sistema ficando lento

**Solução:**

Limpe os logs antigos manualmente ou use script:

**Windows:**
```bash
# Deletar logs com mais de 30 dias
forfiles /p logs /m *.log /d -30 /c "cmd /c del @path"
```

**Linux/Mac:**
```bash
# Deletar logs com mais de 30 dias
find logs/ -name "*.log" -mtime +30 -delete
```

---

## 🛠️ Manutenção Básica

### Verificações Semanais

**O que verificar uma vez por semana:**

1. **Emails estão chegando?**
   - Confirme se os emails diários estão sendo recebidos

2. **Logs não têm muitos erros?**
   - Dê uma olhada rápida nos arquivos de log
   - Procure por "ERROR" ou "❌"

3. **Sistema está executando?**
   - Verifique se o processo está rodando (no gerenciador de tarefas)

### Limpeza Mensal

**Uma vez por mês:**

1. **Limpar logs antigos:**
   - Deletar logs com mais de 30 dias
   - (Veja comando no Problema 6 acima)

2. **Verificar espaço em disco:**
   - Certifique-se de que há espaço suficiente
   - Relatórios HTML ocupam pouco espaço, mas logs podem crescer

3. **Revisar relatórios salvos:**
   - Se quiser, pode fazer backup dos relatórios antigos
   - Ou deletar relatórios muito antigos (mais de 1 ano)

### Atualizações

**Quando atualizar:**

1. **Python:**
   - Se houver atualização importante de segurança
   - Mas cuidado: Pode quebrar compatibilidade

2. **Dependências:**
   - Geralmente não precisa atualizar
   - Apenas se houver problema específico

**Como atualizar dependências:**
```bash
pip install --upgrade -r requirements.txt
```

### Backup

**O que fazer backup:**

1. **Arquivo `.env`:**
   - Faça backup criptografado (contém senhas!)
   - Salve em local seguro

2. **Relatórios importantes:**
   - Se houver relatórios específicos que precisa guardar
   - Faça backup antes de deletar

---

## ❓ Dúvidas Frequentes

### 1. O sistema funciona em feriados?

**Resposta:** Sim! O sistema executa todos os dias, inclusive feriados. Se não houver documentos publicados no BACEN, você receberá um email informando isso.

### 2. Posso mudar o horário de execução?

**Resposta:** Sim! Edite o arquivo `.env` e altere a linha `HORA_EXECUCAO=07:00` para o horário desejado.

### 3. Quantos emails posso enviar por dia?

**Resposta:** 
- **Gmail**: Até 500 emails/dia (gratuito)
- **Outlook**: Até 300 emails/dia (gratuito)

Como o sistema envia apenas 1 email por dia (para múltiplos destinatários), você está bem dentro dos limites.

### 4. E se o computador estiver desligado?

**Resposta:** O sistema não executará. Para garantir execução diária, deixe o computador ligado ou use um servidor que fica sempre ligado.

### 5. Posso adicionar mais destinatários depois?

**Resposta:** Sim! Basta editar o arquivo `.env` e adicionar mais emails separados por vírgula na linha `DESTINATARIOS=`.

### 6. Os relatórios antigos são deletados?

**Resposta:** Não automaticamente. Você precisa deletar manualmente ou configurar uma limpeza automática (requer conhecimento técnico).

### 7. O sistema funciona offline?

**Resposta:** Não. O sistema precisa de internet para:
- Acessar o site do BACEN
- Enviar emails

### 8. Posso usar outro email além de Gmail/Outlook?

**Resposta:** Teoricamente sim, mas requer configuração manual do servidor SMTP. Consulte a documentação técnica ou entre em contato com a equipe de TI.

### 9. Quanto tempo leva cada execução?

**Resposta:** Normalmente entre 2 a 5 minutos, dependendo de:
- Velocidade da internet
- Quantidade de documentos
- Velocidade do computador

### 10. Posso executar mais de uma vez por dia?

**Resposta:** Sim! Você pode executar manualmente quantas vezes quiser usando:
```bash
python main.py --teste
```

Mas o agendamento automático é apenas uma vez por dia.

---

## 📖 Glossário

**BACEN**: Banco Central do Brasil - Autoridade monetária brasileira

**ChromeDriver**: Programa que permite ao Python controlar o navegador Chrome

**Comunicado**: Aviso ou informação oficial do BACEN

**Circular**: Documento com orientações do BACEN para instituições financeiras

**Headless**: Modo de execução sem interface gráfica (sem abrir janela do navegador)

**HTML**: Formato de arquivo usado para criar páginas web e relatórios

**Log**: Arquivo que registra todas as operações e erros do sistema

**Resolução**: Norma ou regra estabelecida pelo BACEN

**SMTP**: Protocolo usado para enviar emails

**Webcrawler**: Programa que navega automaticamente em sites para coletar informações

**Senha de Aplicativo**: Senha especial gerada pelo Gmail para uso em aplicativos (mais segura que senha normal)

---

## 📞 Precisa de Ajuda?

### Antes de Pedir Ajuda

1. ✅ Verifique os logs do sistema
2. ✅ Tente executar manualmente: `python main.py --teste`
3. ✅ Revise este manual
4. ✅ Verifique a documentação técnica (se tiver conhecimento)

### Informações para Pedir Ajuda

Quando pedir ajuda, forneça:

1. **Mensagem de erro completa** (se houver)
2. **Últimas linhas dos logs** relevantes
3. **O que você estava tentando fazer**
4. **Sistema operacional** (Windows/Linux/Mac)
5. **Versão do Python** (`python --version`)

### Contatos

- **Equipe de TI**: Para problemas técnicos
- **Este manual**: Para dúvidas de uso
- **Documentação Técnica**: Para detalhes avançados

---

**Manual do Usuário - Sistema de Monitoramento BACEN**  
Versão 1.0  
Última atualização: 2024

---

## 📎 Anexos

### Exemplo de Arquivo .env Completo

```env
# Configurações de Email
EMAIL_PROVIDER=gmail
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_de_aplicativo_aqui

# Lista de destinatários (separados por vírgula, sem espaços)
DESTINATARIOS=email1@cielo.com.br,email2@cielo.com.br,email3@cielo.com.br

# Configurações de Agendamento
HORA_EXECUCAO=07:00
FUSO_HORARIO=America/Sao_Paulo

# Configurações do Selenium (geralmente não precisa mudar)
HEADLESS_MODE=true
TIMEOUT_PAGINA=30
DELAY_ENTRE_REQUISICOES=2
```

### Comandos Úteis

```bash
# Testar sistema
python main.py --teste

# Executar com agendamento
python main.py --agendador

# Ver versão do Python
python --version

# Instalar/atualizar dependências
pip install -r requirements.txt

# Verificar logs em tempo real (Linux/Mac)
tail -f sistema_monitoramento.log
```

---

**Boa sorte com o sistema! 🚀**


