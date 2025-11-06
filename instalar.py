#!/usr/bin/env python3
"""
Script de instalação e configuração do Sistema de Monitoramento BACEN
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def verificar_python():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 ou superior é necessário")
        print(f"Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detectado")
    return True

def instalar_dependencias():
    """Instala as dependências do projeto"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def criar_diretorios():
    """Cria os diretórios necessários"""
    print("📁 Criando diretórios...")
    diretorios = ['relatorios', 'logs']
    
    for diretorio in diretorios:
        os.makedirs(diretorio, exist_ok=True)
        print(f"✅ Diretório '{diretorio}' criado")
    
    return True

def configurar_ambiente():
    """Configura o arquivo de ambiente"""
    print("⚙️ Configurando ambiente...")
    
    if not os.path.exists('.env'):
        if os.path.exists('config_example.env'):
            shutil.copy('config_example.env', '.env')
            print("✅ Arquivo .env criado a partir do exemplo")
            print("⚠️ IMPORTANTE: Configure suas credenciais no arquivo .env")
        else:
            print("❌ Arquivo de exemplo não encontrado")
            return False
    else:
        print("✅ Arquivo .env já existe")
    
    return True

def criar_script_execucao():
    """Cria scripts de execução para Windows e Linux"""
    print("📝 Criando scripts de execução...")
    
    # Script para Windows
    script_windows = """@echo off
cd /d "%~dp0"
python main.py --agendador
pause
"""
    
    with open('executar_sistema.bat', 'w', encoding='utf-8') as f:
        f.write(script_windows)
    
    # Script para Linux/Mac
    script_linux = """#!/bin/bash
cd "$(dirname "$0")"
python3 main.py --agendador
"""
    
    with open('executar_sistema.sh', 'w', encoding='utf-8') as f:
        f.write(script_linux)
    
    # Torna o script Linux executável
    if os.name != 'nt':  # Não é Windows
        os.chmod('executar_sistema.sh', 0o755)
    
    print("✅ Scripts de execução criados")
    return True

def criar_agendamento_windows():
    """Cria um arquivo de tarefa agendada para Windows"""
    print("⏰ Criando agendamento para Windows...")
    
    script_path = os.path.abspath('main.py')
    python_path = sys.executable
    
    task_xml = f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2024-01-01T07:00:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>S-1-5-18</UserId>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>true</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT1H</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{python_path}</Command>
      <Arguments>"{script_path}" --agendador</Arguments>
      <WorkingDirectory>{os.path.dirname(script_path)}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>"""
    
    with open('MonitoramentoBACEN.xml', 'w', encoding='utf-8') as f:
        f.write(task_xml)
    
    print("✅ Arquivo de tarefa agendada criado (MonitoramentoBACEN.xml)")
    print("💡 Para instalar a tarefa, execute como administrador:")
    print("   schtasks /create /xml MonitoramentoBACEN.xml /tn MonitoramentoBACEN")
    
    return True

def executar_teste():
    """Executa um teste do sistema"""
    print("🧪 Executando teste do sistema...")
    try:
        resultado = subprocess.run([sys.executable, "main.py", "--teste"], 
                                 capture_output=True, text=True, timeout=300)
        
        if resultado.returncode == 0:
            print("✅ Teste executado com sucesso")
            return True
        else:
            print(f"❌ Erro no teste: {resultado.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Teste demorou muito para executar (timeout)")
        return False
    except Exception as e:
        print(f"❌ Erro ao executar teste: {e}")
        return False

def main():
    """Função principal de instalação"""
    print("🚀 Sistema de Monitoramento BACEN - Instalação")
    print("=" * 50)
    
    # Verificações iniciais
    if not verificar_python():
        return False
    
    # Instalação
    if not instalar_dependencias():
        return False
    
    if not criar_diretorios():
        return False
    
    if not configurar_ambiente():
        return False
    
    if not criar_script_execucao():
        return False
    
    if os.name == 'nt':  # Windows
        criar_agendamento_windows()
    
    print("\n" + "=" * 50)
    print("✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 50)
    
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Configure suas credenciais no arquivo .env")
    print("2. Execute um teste: python main.py --teste")
    print("3. Para executar o sistema:")
    if os.name == 'nt':
        print("   - Windows: execute executar_sistema.bat")
        print("   - Ou instale a tarefa agendada como administrador")
    else:
        print("   - Linux/Mac: ./executar_sistema.sh")
    
    print("\n⚠️ IMPORTANTE:")
    print("- Configure o arquivo .env com suas credenciais de email")
    print("- Para Gmail: use senha de aplicativo (não a senha normal)")
    print("- Para Outlook: use sua senha normal da conta")
    print("- Teste o sistema antes de colocar em produção")
    print("- Monitore os logs para verificar o funcionamento")
    
    # Pergunta se quer executar teste
    resposta = input("\n🧪 Deseja executar um teste agora? (s/n): ").lower()
    if resposta in ['s', 'sim', 'y', 'yes']:
        executar_teste()

if __name__ == "__main__":
    main()
