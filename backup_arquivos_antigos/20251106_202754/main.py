import schedule
import time
import logging
from datetime import datetime
import pytz
import os
import sys

# Importa os módulos do sistema
from webcrawler import WebcrawlerBACEN
from sumarizador import SumarizadorBACEN
from enviador_email import EnviadorEmail
from config import *

class SistemaMonitoramentoBACEN:
    def __init__(self):
        self.setup_logging()
        self.webcrawler = WebcrawlerBACEN()
        self.sumarizador = SumarizadorBACEN()
        self.enviador = EnviadorEmail()
        
    def setup_logging(self):
        """Configura o sistema de logging principal"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('sistema_monitoramento.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def executar_processo_completo(self):
        """Executa o processo completo de monitoramento"""
        try:
            self.logger.info("=" * 60)
            self.logger.info("INICIANDO PROCESSO DE MONITORAMENTO BACEN")
            self.logger.info("=" * 60)
            
            # Etapa 1: Coleta de dados
            self.logger.info("ETAPA 1: Coletando dados do BACEN...")
            dados_coletados = self.webcrawler.executar_coleta()
            
            if not dados_coletados:
                self.logger.warning("Nenhum dado foi coletado. Enviando email de notificação...")
                self.enviar_notificacao_sem_dados()
                return
            
            self.logger.info(f"Coleta concluída: {len(dados_coletados)} itens encontrados")
            
            # Etapa 2: Processamento e sumarização
            self.logger.info("ETAPA 2: Processando e sumarizando informações...")
            informacoes_processadas = self.sumarizador.processar_informacoes(dados_coletados)
            
            if not informacoes_processadas:
                self.logger.error("Erro no processamento das informações")
                return
            
            self.logger.info(f"Processamento concluído: {len(informacoes_processadas)} itens processados")
            
            # Etapa 3: Envio de email
            self.logger.info("ETAPA 3: Enviando relatório por email...")
            resultado_envio = self.enviador.enviar_email(informacoes_processadas)
            
            if resultado_envio['sucesso']:
                self.logger.info(f"Email enviado com sucesso para {resultado_envio['total_enviados']} destinatários")
            else:
                self.logger.error(f"Falha no envio do email: {resultado_envio.get('erro', 'Erro desconhecido')}")
            
            # Etapa 4: Salvar relatório local
            self.logger.info("ETAPA 4: Salvando relatório local...")
            self.salvar_relatorio_local(informacoes_processadas)
            
            self.logger.info("PROCESSO CONCLUÍDO COM SUCESSO!")
            self.logger.info("=" * 60)
            
        except Exception as e:
            self.logger.error(f"Erro durante o processo de monitoramento: {str(e)}")
            self.enviar_notificacao_erro(str(e))
    
    def enviar_notificacao_sem_dados(self):
        """Envia notificação quando não há dados para o dia"""
        try:
            assunto = f"Monitoramento BACEN - {datetime.now().strftime('%d/%m/%Y')} - Sem dados"
            corpo = f"""
            Relatório de Monitoramento BACEN - {datetime.now().strftime('%d/%m/%Y')}
            
            Nenhum comunicado, resolução ou circular foi encontrado para o dia de hoje.
            
            O sistema continuará monitorando normalmente.
            
            Sistema de Monitoramento BACEN - Cielo
            """
            
            resultado = self.enviador.enviar_email_simples(assunto, corpo)
            if resultado['sucesso']:
                self.logger.info("Notificação de 'sem dados' enviada com sucesso")
            else:
                self.logger.error("Falha ao enviar notificação de 'sem dados'")
                
        except Exception as e:
            self.logger.error(f"Erro ao enviar notificação de 'sem dados': {str(e)}")
    
    def enviar_notificacao_erro(self, erro):
        """Envia notificação quando ocorre erro no sistema"""
        try:
            assunto = f"ERRO - Monitoramento BACEN - {datetime.now().strftime('%d/%m/%Y')}"
            corpo = f"""
            ERRO NO SISTEMA DE MONITORAMENTO BACEN
            
            Data/Hora: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
            
            Erro: {erro}
            
            Por favor, verifique os logs do sistema e entre em contato com a equipe de TI.
            
            Sistema de Monitoramento BACEN - Cielo
            """
            
            resultado = self.enviador.enviar_email_simples(assunto, corpo)
            if resultado['sucesso']:
                self.logger.info("Notificação de erro enviada com sucesso")
            else:
                self.logger.error("Falha ao enviar notificação de erro")
                
        except Exception as e:
            self.logger.error(f"Erro ao enviar notificação de erro: {str(e)}")
    
    def salvar_relatorio_local(self, informacoes_processadas):
        """Salva o relatório localmente"""
        try:
            # Cria diretório de relatórios se não existir
            os.makedirs('relatorios', exist_ok=True)
            
            # Gera o relatório HTML
            relatorio_html = self.sumarizador.gerar_relatorio_html(informacoes_processadas)
            
            # Salva o arquivo
            data_atual = datetime.now().strftime("%Y%m%d")
            nome_arquivo = f"relatorios/relatorio_bacen_{data_atual}.html"
            
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write(relatorio_html)
            
            self.logger.info(f"Relatório salvo localmente: {nome_arquivo}")
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar relatório local: {str(e)}")
    
    def configurar_agendamento(self):
        """Configura o agendamento diário"""
        try:
            # Agenda a execução diária às 07:00
            schedule.every().day.at(HORA_EXECUCAO).do(self.executar_processo_completo)
            
            self.logger.info(f"Agendamento configurado para execução diária às {HORA_EXECUCAO}")
            
        except Exception as e:
            self.logger.error(f"Erro ao configurar agendamento: {str(e)}")
    
    def executar_agendador(self):
        """Executa o agendador principal"""
        try:
            self.logger.info("Iniciando sistema de agendamento...")
            self.configurar_agendamento()
            
            # Envia notificação de inicialização
            self.enviar_notificacao_inicializacao()
            
            while True:
                schedule.run_pending()
                time.sleep(60)  # Verifica a cada minuto
                
        except KeyboardInterrupt:
            self.logger.info("Sistema interrompido pelo usuário")
        except Exception as e:
            self.logger.error(f"Erro no agendador: {str(e)}")
    
    def enviar_notificacao_inicializacao(self):
        """Envia notificação de que o sistema foi inicializado"""
        try:
            assunto = "Sistema de Monitoramento BACEN - Inicializado"
            corpo = f"""
            Sistema de Monitoramento BACEN inicializado com sucesso!
            
            Data/Hora: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
            
            O sistema está configurado para executar diariamente às {HORA_EXECUCAO}.
            
            Sistema de Monitoramento BACEN - Cielo
            """
            
            resultado = self.enviador.enviar_email_simples(assunto, corpo)
            if resultado['sucesso']:
                self.logger.info("Notificação de inicialização enviada")
            else:
                self.logger.warning("Falha ao enviar notificação de inicialização")
                
        except Exception as e:
            self.logger.error(f"Erro ao enviar notificação de inicialização: {str(e)}")
    
    def executar_teste(self):
        """Executa um teste do sistema"""
        self.logger.info("Executando teste do sistema...")
        self.executar_processo_completo()

def main():
    """Função principal"""
    sistema = SistemaMonitoramentoBACEN()
    
    # Verifica argumentos da linha de comando
    if len(sys.argv) > 1:
        if sys.argv[1] == '--teste':
            sistema.executar_teste()
        elif sys.argv[1] == '--agendador':
            sistema.executar_agendador()
        else:
            print("Uso: python main.py [--teste|--agendador]")
            print("  --teste: Executa um teste do sistema")
            print("  --agendador: Inicia o agendador para execução diária")
    else:
        print("Sistema de Monitoramento BACEN - Cielo")
        print("Uso: python main.py [--teste|--agendador]")
        print("  --teste: Executa um teste do sistema")
        print("  --agendador: Inicia o agendador para execução diária")

if __name__ == "__main__":
    main()

