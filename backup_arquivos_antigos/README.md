# 📦 Backup de Arquivos Antigos

Esta pasta contém os arquivos antigos que foram movidos durante a refatoração do sistema.

## 📅 Data do Backup
2025-11-06

## 📁 Arquivos Movidos

### Módulos Antigos (substituídos pela estrutura modular)
- `webcrawler.py` → `modulo_scraper/bacen_scraper.py`
- `sumarizador.py` → `modulo_llm/` (múltiplos arquivos)
- `enviador_email.py` → `modulo_email/email_sender.py`
- `main.py` → `main_refatorado.py`
- `config.py` → `config/config.py`
- `exemplo_uso.py` → Precisa ser atualizado para usar novos módulos

### Arquivos de Configuração Antigos
- `config_example.env` → `config_example_refatorado.env`
- `config_outlook.env` → Integrado em `config_example_refatorado.env`
- `requirements.txt` → `requirements_refatorado.txt`

### Logs Antigos
- `webcrawler.log`
- `sumarizador.log`
- `enviador_email.log`
- `sistema_monitoramento.log`

## ⚠️ Importante

**NÃO DELETE ESTA PASTA** até confirmar que:
1. ✅ O sistema refatorado está funcionando corretamente
2. ✅ Todos os testes passaram
3. ✅ A migração foi concluída com sucesso

## 🔄 Como Restaurar (se necessário)

Se precisar restaurar algum arquivo:

```bash
# Restaurar um arquivo específico
cp backup_arquivos_antigos/20251106_202754/webcrawler.py .

# Restaurar todos os arquivos
cp backup_arquivos_antigos/20251106_202754/*.py .
```

## 🗑️ Quando Pode Remover

Você pode remover esta pasta de backup após:
- ✅ Testar o sistema refatorado: `python main_refatorado.py --teste`
- ✅ Verificar que a interface Streamlit funciona: `python main_refatorado.py --streamlit`
- ✅ Confirmar que o agendamento funciona: `python main_refatorado.py --agendador`
- ✅ Validar que os emails estão sendo enviados corretamente

---

**Sistema Refatorado - Versão 2.0**

