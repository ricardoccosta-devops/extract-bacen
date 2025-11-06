"""
Sistema Principal Refatorado - Plataforma de Monitoramento BACEN
Integra todos os módulos em um pipeline completo
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from modulo_scraper import BACENScraper
from modulo_llm import LLMManager
from modulo_report import PDFGenerator
from modulo_email import EmailSender
from modulo_scheduler import TaskScheduler
from config.config import Config


class SistemaMonitoramentoBACEN:
    """Sistema principal de monitoramento BACEN"""
    
    def __init__(self, config: Config = None):
        """
        Inicializa o sistema
        
        Args:
            config: Objeto de configuração
        """
        self.config = config or Config()
        self.setup_logging()
        
        # Inicializa componentes
        self.scraper = BACENScraper(self.config)
        self.llm_manager = LLMManager(
            provider_name=self.config.LLM_PROVIDER,
            api_key=self.config.get_llm_api_key(),
            model=getattr(self.config, f"{self.config.LLM_PROVIDER.upper()}_MODEL", None)
        )
        self.pdf_generator = PDFGenerator(str(self.config.RELATORIOS_DIR))
        self.email_sender = EmailSender(self.config)
        
        self.logger.info("Sistema de Monitoramento BACEN inicializado")
    
    def setup_logging(self):
        """Configura o sistema de logging principal"""
        os.makedirs(self.config.LOGS_DIR, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config.LOGS_DIR / 'sistema_monitoramento.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def executar_processo_completo(self):
        """
        Executa o processo completo de monitoramento:
        1. Coleta de dados
        2. Processamento com LLM
        3. Geração de PDF
        4. Envio de email
        """
        try:
            self.logger.info("=" * 60)
            self.logger.info("INICIANDO PROCESSO DE MONITORAMENTO BACEN")
            self.logger.info("=" * 60)
            
            # Etapa 1: Coleta de dados
            self.logger.info("ETAPA 1: Coletando dados do BACEN...")
            dados_coletados = self.scraper.executar_coleta()
            
            if not dados_coletados:
                self.logger.warning("Nenhum dado foi coletado. Enviando notificação...")
                self.enviar_notificacao_sem_dados()
                return
            
            self.logger.info(f"Coleta concluída: {len(dados_coletados)} itens encontrados")
            
            # Etapa 2: Processamento com LLM
            self.logger.info("ETAPA 2: Processando com LLM...")
            informacoes_processadas = []
            
            for idx, item in enumerate(dados_coletados):
                try:
                    self.logger.info(f"Processando {idx+1}/{len(dados_coletados)}: {item['titulo'][:50]}...")
                    
                    texto = item.get('conteudo_completo', '')
                    titulo = item.get('titulo', '')
                    link = item.get('link', '')
                    
                    if texto:
                        resumo = self.llm_manager.summarize(
                            texto=texto,
                            titulo=titulo,
                            link=link,
                            max_lines=5
                        )
                        item['resumo'] = resumo
                    else:
                        item['resumo'] = "Conteúdo não disponível."
                    
                    informacoes_processadas.append(item)
                    
                except Exception as e:
                    self.logger.error(f"Erro ao processar item {item.get('titulo', 'desconhecido')}: {str(e)}")
                    # Adiciona item mesmo com erro
                    item['resumo'] = "Erro ao processar conteúdo."
                    informacoes_processadas.append(item)
            
            self.logger.info(f"Processamento concluído: {len(informacoes_processadas)} itens processados")
            
            # Etapa 3: Geração de PDF
            self.logger.info("ETAPA 3: Gerando relatório PDF...")
            try:
                caminho_pdf = self.pdf_generator.generate_pdf(informacoes_processadas)
                self.logger.info(f"PDF gerado: {caminho_pdf}")
            except Exception as e:
                self.logger.error(f"Erro ao gerar PDF: {str(e)}")
                caminho_pdf = None
            
            # Etapa 4: Envio de email
            self.logger.info("ETAPA 4: Enviando relatório por email...")
            try:
                assunto = f"Relatório BACEN - {datetime.now().strftime('%d/%m/%Y')}"
                corpo_html = self.email_sender.criar_corpo_email_html(informacoes_processadas)
                
                resultado = self.email_sender.enviar_email_com_anexo(
                    assunto=assunto,
                    corpo_html=corpo_html,
                    caminho_pdf=caminho_pdf
                )
                
                if resultado['sucesso']:
                    self.logger.info(f"Email enviado para {resultado['total_enviados']} destinatário(s)")
                else:
                    self.logger.error(f"Falha no envio do email: {resultado.get('erro', 'Erro desconhecido')}")
                    
            except Exception as e:
                self.logger.error(f"Erro ao enviar email: {str(e)}")
            
            self.logger.info("PROCESSO CONCLUÍDO COM SUCESSO!")
            self.logger.info("=" * 60)
            
        except Exception as e:
            self.logger.error(f"Erro durante o processo de monitoramento: {str(e)}")
            self.enviar_notificacao_erro(str(e))
            raise
    
    def enviar_notificacao_sem_dados(self):
        """Envia notificação quando não há dados"""
        try:
            assunto = f"Monitoramento BACEN - {datetime.now().strftime('%d/%m/%Y')} - Sem dados"
            corpo = f"""
            Relatório de Monitoramento BACEN - {datetime.now().strftime('%d/%m/%Y')}
            
            Nenhum comunicado, resolução ou circular foi encontrado para o dia de hoje.
            
            O sistema continuará monitorando normalmente.
            
            Sistema de Monitoramento BACEN - Cielo
            """
            
            resultado = self.email_sender.enviar_email_com_anexo(
                assunto=assunto,
                corpo_html=f"<p>{corpo.replace(chr(10), '<br>')}</p>"
            )
            
            if resultado['sucesso']:
                self.logger.info("Notificação de 'sem dados' enviada")
            else:
                self.logger.error("Falha ao enviar notificação de 'sem dados'")
                
        except Exception as e:
            self.logger.error(f"Erro ao enviar notificação de 'sem dados': {str(e)}")
    
    def enviar_notificacao_erro(self, erro: str):
        """Envia notificação de erro"""
        try:
            assunto = f"ERRO - Monitoramento BACEN - {datetime.now().strftime('%d/%m/%Y')}"
            corpo = f"""
            ERRO NO SISTEMA DE MONITORAMENTO BACEN
            
            Data/Hora: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
            
            Erro: {erro}
            
            Por favor, verifique os logs do sistema e entre em contato com a equipe de TI.
            
            Sistema de Monitoramento BACEN - Cielo
            """
            
            resultado = self.email_sender.enviar_email_com_anexo(
                assunto=assunto,
                corpo_html=f"<p>{corpo.replace(chr(10), '<br>')}</p>"
            )
            
            if resultado['sucesso']:
                self.logger.info("Notificação de erro enviada")
            else:
                self.logger.error("Falha ao enviar notificação de erro")
                
        except Exception as e:
            self.logger.error(f"Erro ao enviar notificação de erro: {str(e)}")
    
    def executar_teste(self):
        """Executa um teste do sistema"""
        self.logger.info("Executando teste do sistema...")
        self.executar_processo_completo()
    
    def executar_com_agendamento(self):
        """Executa o sistema com agendamento automático"""
        try:
            self.logger.info("Iniciando sistema de agendamento...")
            
            scheduler = TaskScheduler(self.config)
            scheduler.agendar_tarefa_diaria(
                self.executar_processo_completo,
                hora=self.config.HORA_EXECUCAO
            )
            
            # Envia notificação de inicialização
            self.enviar_notificacao_inicializacao()
            
            # Inicia o agendador
            scheduler.executar()
            
        except KeyboardInterrupt:
            self.logger.info("Sistema interrompido pelo usuário")
        except Exception as e:
            self.logger.error(f"Erro no agendador: {str(e)}")
            raise
    
    def enviar_notificacao_inicializacao(self):
        """Envia notificação de inicialização"""
        try:
            assunto = "Sistema de Monitoramento BACEN - Inicializado"
            corpo = f"""
            Sistema de Monitoramento BACEN inicializado com sucesso!
            
            Data/Hora: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
            
            O sistema está configurado para executar diariamente às {self.config.HORA_EXECUCAO}.
            
            Sistema de Monitoramento BACEN - Cielo
            """
            
            resultado = self.email_sender.enviar_email_com_anexo(
                assunto=assunto,
                corpo_html=f"<p>{corpo.replace(chr(10), '<br>')}</p>"
            )
            
            if resultado['sucesso']:
                self.logger.info("Notificação de inicialização enviada")
            else:
                self.logger.warning("Falha ao enviar notificação de inicialização")
                
        except Exception as e:
            self.logger.error(f"Erro ao enviar notificação de inicialização: {str(e)}")


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Sistema de Monitoramento BACEN")
    parser.add_argument(
        '--teste',
        action='store_true',
        help='Executa um teste do sistema'
    )
    parser.add_argument(
        '--agendador',
        action='store_true',
        help='Inicia o agendador para execução diária'
    )
    parser.add_argument(
        '--streamlit',
        action='store_true',
        help='Inicia a interface web Streamlit'
    )
    
    args = parser.parse_args()
    
    # Valida configurações
    config = Config()
    errors = config.validate()
    
    if errors:
        print("⚠️ Erros de configuração encontrados:")
        for error in errors:
            print(f"  - {error}")
        print("\nConfigure o arquivo .env antes de continuar.")
        return
    
    sistema = SistemaMonitoramentoBACEN(config)
    
    if args.teste:
        sistema.executar_teste()
    elif args.agendador:
        sistema.executar_com_agendamento()
    elif args.streamlit:
        print("Iniciando interface Streamlit...")
        os.system("streamlit run frontend/app.py")
    else:
        print("Sistema de Monitoramento BACEN - Cielo")
        print("\nUso:")
        print("  python main.py --teste      : Executa um teste do sistema")
        print("  python main.py --agendador  : Inicia o agendador para execução diária")
        print("  python main.py --streamlit  : Inicia a interface web Streamlit")


if __name__ == "__main__":
    main()

