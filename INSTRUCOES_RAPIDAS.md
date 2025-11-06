# 🚀 INSTRUÇÕES RÁPIDAS - Sistema de Monitoramento BACEN

## ⚡ Instalação Rápida

```bash
# 1. Execute o instalador
python instalar.py

# 2. Configure suas credenciais no arquivo .env
# Edite o arquivo .env com seu email e senha de aplicativo

# 3. Teste o sistema
python main.py --teste
```

## 🎯 Execução

### Teste Manual
```bash
python main.py --teste
```

### Execução com Agendamento
```bash
python main.py --agendador
```

### Scripts de Execução
- **Windows:** `executar_sistema.bat`
- **Linux/Mac:** `./executar_sistema.sh`

## ⚙️ Configuração Essencial

Edite o arquivo `.env`:

```env
EMAIL_PROVIDER=gmail
EMAIL_USER=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_app
DESTINATARIOS=email1@cielo.com.br,email2@cielo.com.br
```

**Provedores suportados:**
- **Gmail**: Use senha de aplicativo
- **Outlook**: Use senha normal da conta

## 📋 Checklist de Instalação

- [ ] Python 3.8+ instalado
- [ ] Google Chrome instalado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Arquivo `.env` configurado
- [ ] Teste executado com sucesso
- [ ] Sistema agendado para execução diária

## 🔧 Solução de Problemas Rápidos

### Erro de ChromeDriver
```bash
pip install --upgrade webdriver-manager
```

### Erro de Email
- Verifique se a senha de aplicativo está correta
- Confirme se a verificação em duas etapas está ativa

### Sistema não executa
```bash
python main.py --teste
# Verifique os logs para detalhes
```

## 📞 Suporte

- Logs: `sistema_monitoramento.log`
- Relatórios: pasta `relatorios/`
- Teste: `python exemplo_uso.py`

---

**Sistema desenvolvido para Cielo**  
Monitoramento automatizado do Banco Central do Brasil
