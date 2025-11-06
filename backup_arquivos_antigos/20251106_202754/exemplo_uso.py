#!/usr/bin/env python3
"""
Exemplo de uso do Sistema de Monitoramento BACEN
Este arquivo demonstra como usar cada módulo individualmente
"""

from webcrawler import WebcrawlerBACEN
from sumarizador import SumarizadorBACEN
from enviador_email import EnviadorEmail
from main import SistemaMonitoramentoBACEN
import logging

def exemplo_webcrawler():
    """Exemplo de uso do webcrawler"""
    print("🔍 Exemplo: Webcrawler BACEN")
    print("-" * 40)
    
    crawler = WebcrawlerBACEN()
    dados = crawler.executar_coleta()
    
    print(f"Documentos encontrados: {len(dados)}")
    for item in dados[:3]:  # Mostra apenas os primeiros 3
        print(f"- {item['tipo']}: {item['titulo'][:50]}...")
    
    return dados

def exemplo_sumarizador(dados):
    """Exemplo de uso do sumarizador"""
    print("\n📝 Exemplo: Sumarizador")
    print("-" * 40)
    
    sumarizador = SumarizadorBACEN()
    informacoes_processadas = sumarizador.processar_informacoes(dados)
    
    print(f"Informações processadas: {len(informacoes_processadas)}")
    for item in informacoes_processadas[:2]:  # Mostra apenas os primeiros 2
        print(f"- {item['tipo']}: {item['titulo'][:50]}...")
        print(f"  Resumo: {item['resumo'][:100]}...")
    
    return informacoes_processadas

def exemplo_enviador_email(informacoes_processadas):
    """Exemplo de uso do enviador de email"""
    print("\n📧 Exemplo: Enviador de Email")
    print("-" * 40)
    
    enviador = EnviadorEmail()
    
    # Exemplo de email simples
    resultado = enviador.enviar_email_simples(
        "Teste do Sistema BACEN",
        "Este é um email de teste do sistema de monitoramento BACEN."
    )
    
    print(f"Resultado do envio: {resultado['sucesso']}")
    if resultado['sucesso']:
        print(f"Enviado para: {len(resultado['destinatarios_sucesso'])} destinatários")
    
    # Exemplo de email completo (comentado para não enviar)
    # resultado_completo = enviador.enviar_email(informacoes_processadas)
    # print(f"Email completo: {resultado_completo['sucesso']}")

def exemplo_sistema_completo():
    """Exemplo de uso do sistema completo"""
    print("\n🚀 Exemplo: Sistema Completo")
    print("-" * 40)
    
    sistema = SistemaMonitoramentoBACEN()
    
    # Executa apenas um teste (não o agendador)
    print("Executando teste do sistema...")
    sistema.executar_processo_completo()
    print("Teste concluído!")

def main():
    """Função principal de exemplo"""
    print("📚 EXEMPLOS DE USO - Sistema de Monitoramento BACEN")
    print("=" * 60)
    
    # Configura logging para os exemplos
    logging.basicConfig(level=logging.INFO)
    
    try:
        # Exemplo 1: Webcrawler
        dados = exemplo_webcrawler()
        
        if dados:
            # Exemplo 2: Sumarizador
            informacoes_processadas = exemplo_sumarizador(dados)
            
            if informacoes_processadas:
                # Exemplo 3: Enviador de Email
                exemplo_enviador_email(informacoes_processadas)
        
        # Exemplo 4: Sistema Completo
        exemplo_sistema_completo()
        
    except Exception as e:
        print(f"❌ Erro durante os exemplos: {str(e)}")
        print("Verifique se todas as dependências estão instaladas e configuradas.")
    
    print("\n" + "=" * 60)
    print("✅ Exemplos concluídos!")
    print("\n💡 Para usar o sistema em produção:")
    print("   python main.py --agendador")
    print("\n💡 Para executar um teste:")
    print("   python main.py --teste")

if __name__ == "__main__":
    main()

