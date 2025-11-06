#!/usr/bin/env python3
"""
Script de Limpeza - Remove arquivos antigos após refatoração
Move arquivos antigos para pasta de backup antes de remover
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def criar_backup():
    """Cria pasta de backup e move arquivos antigos"""
    
    # Pasta de backup
    backup_dir = Path("backup_arquivos_antigos")
    backup_dir.mkdir(exist_ok=True)
    
    # Data do backup
    data_backup = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_subdir = backup_dir / data_backup
    backup_subdir.mkdir(exist_ok=True)
    
    # Arquivos antigos a serem movidos
    arquivos_antigos = [
        "webcrawler.py",
        "sumarizador.py",
        "enviador_email.py",
        "main.py",
        "config.py",  # Config antigo na raiz
        "exemplo_uso.py",
        "config_example.env",
        "config_outlook.env",
        "requirements.txt"
    ]
    
    arquivos_movidos = []
    arquivos_nao_encontrados = []
    
    print("🧹 Limpando arquivos antigos após refatoração...")
    print("=" * 60)
    
    for arquivo in arquivos_antigos:
        arquivo_path = Path(arquivo)
        
        if arquivo_path.exists():
            try:
                # Move para backup
                destino = backup_subdir / arquivo_path.name
                shutil.move(str(arquivo_path), str(destino))
                arquivos_movidos.append(arquivo)
                print(f"✅ Movido: {arquivo} → backup/{data_backup}/")
            except Exception as e:
                print(f"❌ Erro ao mover {arquivo}: {str(e)}")
        else:
            arquivos_nao_encontrados.append(arquivo)
    
    print("\n" + "=" * 60)
    print(f"📦 Backup criado em: {backup_subdir}")
    print(f"✅ Arquivos movidos: {len(arquivos_movidos)}")
    
    if arquivos_movidos:
        print("\nArquivos movidos para backup:")
        for arquivo in arquivos_movidos:
            print(f"  - {arquivo}")
    
    if arquivos_nao_encontrados:
        print(f"\n⚠️ Arquivos não encontrados (já removidos ou não existem):")
        for arquivo in arquivos_nao_encontrados:
            print(f"  - {arquivo}")
    
    # Limpar logs antigos (opcional)
    print("\n" + "=" * 60)
    resposta = input("Deseja limpar logs antigos também? (s/n): ").lower()
    
    if resposta in ['s', 'sim', 'y', 'yes']:
        logs_antigos = [
            "webcrawler.log",
            "sumarizador.log",
            "enviador_email.log",
            "sistema_monitoramento.log"
        ]
        
        logs_dir = backup_subdir / "logs_antigos"
        logs_dir.mkdir(exist_ok=True)
        
        for log_file in logs_antigos:
            log_path = Path(log_file)
            if log_path.exists():
                try:
                    shutil.move(str(log_path), str(logs_dir / log_path.name))
                    print(f"✅ Log movido: {log_file}")
                except Exception as e:
                    print(f"❌ Erro ao mover log {log_file}: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ Limpeza concluída!")
    print(f"\n💡 Arquivos antigos estão em: {backup_subdir}")
    print("💡 Você pode removê-los manualmente depois de verificar que tudo funciona.")
    print("\n📋 Próximos passos:")
    print("  1. Teste o sistema refatorado: python main_refatorado.py --teste")
    print("  2. Se tudo funcionar, pode remover a pasta de backup")
    print("  3. Renomeie main_refatorado.py para main.py se desejar")

if __name__ == "__main__":
    try:
        criar_backup()
    except KeyboardInterrupt:
        print("\n\n⚠️ Operação cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante a limpeza: {str(e)}")

