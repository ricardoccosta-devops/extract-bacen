"""
Módulo de Envio de Email Refatorado
"""

import os
import smtplib
import logging
from datetime import datetime
from typing import List, Optional
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import sys

# Adiciona o diretório raiz ao path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

try:
    from config.config import Config
except ImportError:
    # Fallback para configuração básica
    class Config:
        EMAIL_PROVIDER = "gmail"
        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT = 587
        EMAIL_USER = ""
        EMAIL_PASSWORD = ""
        DESTINATARIOS = []


class EmailSender:
    """Enviador de emails com suporte a anexos PDF"""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Inicializa o enviador de email
        
        Args:
            config: Objeto de configuração
        """
        self.config = config or Config()
        self.setup_logging()
    
    def setup_logging(self):
        """Configura logging"""
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(log_dir, 'email_sender.log')),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def configurar_servidor_smtp(self):
        """
        Configura o servidor SMTP baseado no provedor
        
        Returns:
            Servidor SMTP configurado
        """
        try:
            self.logger.info(f"Configurando servidor SMTP para {self.config.EMAIL_PROVIDER}")
            self.logger.info(f"Servidor: {self.config.SMTP_SERVER}:{self.config.SMTP_PORT}")
            
            server = smtplib.SMTP(self.config.SMTP_SERVER, self.config.SMTP_PORT)
            server.starttls()
            server.login(self.config.EMAIL_USER, self.config.EMAIL_PASSWORD)
            
            self.logger.info("Conexão SMTP estabelecida com sucesso")
            return server
            
        except Exception as e:
            self.logger.error(f"Erro ao configurar servidor SMTP: {str(e)}")
            raise e
    
    def enviar_email_com_anexo(
        self,
        assunto: str,
        corpo_html: str,
        caminho_pdf: Optional[str] = None,
        destinatarios: Optional[List[str]] = None
    ) -> dict:
        """
        Envia email com anexo PDF
        
        Args:
            assunto: Assunto do email
            corpo_html: Corpo do email em HTML
            caminho_pdf: Caminho do arquivo PDF para anexar
            destinatarios: Lista de destinatários (usa config se None)
            
        Returns:
            Dicionário com resultado do envio
        """
        try:
            server = self.configurar_servidor_smtp()
            
            destinatarios = destinatarios or self.config.DESTINATARIOS
            destinatarios_sucesso = []
            destinatarios_falharam = []
            
            for destinatario in destinatarios:
                try:
                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = assunto
                    msg['From'] = self.config.EMAIL_USER
                    msg['To'] = destinatario
                    
                    # Adiciona corpo HTML
                    html_part = MIMEText(corpo_html, 'html', 'utf-8')
                    msg.attach(html_part)
                    
                    # Adiciona anexo PDF se fornecido
                    if caminho_pdf and os.path.exists(caminho_pdf):
                        with open(caminho_pdf, 'rb') as f:
                            anexo = MIMEBase('application', 'pdf')
                            anexo.set_payload(f.read())
                            encoders.encode_base64(anexo)
                            anexo.add_header(
                                'Content-Disposition',
                                f'attachment; filename= {os.path.basename(caminho_pdf)}'
                            )
                            msg.attach(anexo)
                    
                    server.send_message(msg)
                    destinatarios_sucesso.append(destinatario)
                    self.logger.info(f"Email enviado com sucesso para: {destinatario}")
                    
                except Exception as e:
                    destinatarios_falharam.append(destinatario)
                    self.logger.error(f"Erro ao enviar email para {destinatario}: {str(e)}")
            
            server.quit()
            
            return {
                'sucesso': len(destinatarios_sucesso) > 0,
                'destinatarios_sucesso': destinatarios_sucesso,
                'destinatarios_falharam': destinatarios_falharam,
                'total_enviados': len(destinatarios_sucesso),
                'total_falharam': len(destinatarios_falharam)
            }
            
        except Exception as e:
            self.logger.error(f"Erro geral ao enviar email: {str(e)}")
            return {
                'sucesso': False,
                'erro': str(e),
                'destinatarios_sucesso': [],
                'destinatarios_falharam': destinatarios or self.config.DESTINATARIOS,
                'total_enviados': 0,
                'total_falharam': len(destinatarios or self.config.DESTINATARIOS)
            }
    
    def criar_corpo_email_html(self, informacoes_processadas: List[dict], data_referencia: str = None) -> str:
        """
        Cria o corpo do email em HTML
        
        Args:
            informacoes_processadas: Lista de documentos processados
            data_referencia: Data de referência
            
        Returns:
            HTML do corpo do email
        """
        if data_referencia is None:
            data_referencia = datetime.now().strftime("%d/%m/%Y")
        
        comunicados = [item for item in informacoes_processadas if item.get('tipo') == 'Comunicado']
        resolucoes = [item for item in informacoes_processadas if item.get('tipo') == 'Resolução']
        circulares = [item for item in informacoes_processadas if item.get('tipo') == 'Circular']
        
        html = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Relatório BACEN - {data_referencia}</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background-color: #f4f4f4; }}
                .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
                .header {{ text-align: center; border-bottom: 3px solid #0066cc; padding-bottom: 20px; margin-bottom: 30px; }}
                .header h1 {{ color: #0066cc; margin: 0; }}
                .resumo-executivo {{ background-color: #e8f4fd; padding: 20px; border-radius: 8px; margin-bottom: 30px; }}
                .item {{ margin-bottom: 30px; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background-color: #fafafa; }}
                .titulo {{ font-size: 18px; font-weight: bold; color: #333; }}
                .resumo {{ margin: 15px 0; text-align: justify; }}
                .footer {{ text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Relatório Diário - Banco Central do Brasil</h1>
                    <p>Data: {data_referencia}</p>
                </div>
                <div class="resumo-executivo">
                    <h3>Resumo Executivo</h3>
                    <p><strong>Total:</strong> {len(informacoes_processadas)} | 
                       <strong>Comunicados:</strong> {len(comunicados)} | 
                       <strong>Resoluções:</strong> {len(resolucoes)} | 
                       <strong>Circulares:</strong> {len(circulares)}</p>
                </div>
        """
        
        # Adiciona documentos por tipo
        for tipo, documentos in [('COMUNICADOS', comunicados), ('RESOLUÇÕES', resolucoes), ('CIRCULARES', circulares)]:
            if documentos:
                html += f"<h2 style='color: #0066cc;'>{tipo}</h2>"
                for item in documentos:
                    titulo = item.get('titulo', 'Sem título')
                    resumo = item.get('resumo', '').replace('**', '<strong>').replace('**', '</strong>')
                    link = item.get('link', '')
                    
                    html += f"""
                    <div class="item">
                        <div class="titulo">{titulo}</div>
                        <div class="resumo">{resumo}</div>
                        {f'<p><a href="{link}">🔗 Leia na íntegra</a></p>' if link else ''}
                    </div>
                    """
        
        html += """
                <div class="footer">
                    <p>Relatório gerado automaticamente pelo Sistema de Monitoramento BACEN</p>
                    <p>Ver anexo PDF para versão completa.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html

