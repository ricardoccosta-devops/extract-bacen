import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging
from datetime import datetime
import os
from config import *

class EnviadorEmail:
    def __init__(self):
        self.setup_logging()
        
    def setup_logging(self):
        """Configura o sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('enviador_email.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def configurar_servidor_smtp(self):
        """Configura o servidor SMTP baseado no provedor"""
        try:
            self.logger.info(f"Configurando servidor SMTP para {EMAIL_PROVIDER}")
            self.logger.info(f"Servidor: {SMTP_SERVER}:{SMTP_PORT}")
            
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            
            self.logger.info("Conexão SMTP estabelecida com sucesso")
            return server
            
        except Exception as e:
            self.logger.error(f"Erro ao configurar servidor SMTP: {str(e)}")
            raise e
    
    def criar_corpo_email(self, informacoes_processadas):
        """Cria o corpo do email em HTML"""
        try:
            data_atual = datetime.now().strftime("%d/%m/%Y")
            
            # Conta os tipos de documentos
            comunicados = [item for item in informacoes_processadas if item['tipo'] == 'Comunicado']
            resolucoes = [item for item in informacoes_processadas if item['tipo'] == 'Resolução']
            circulares = [item for item in informacoes_processadas if item['tipo'] == 'Circular']
            
            html_body = f"""
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Relatório BACEN - {data_atual}</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        margin: 0;
                        padding: 20px;
                        background-color: #f4f4f4;
                    }}
                    .container {{
                        max-width: 1200px;
                        margin: 0 auto;
                        background-color: white;
                        padding: 30px;
                        border-radius: 10px;
                        box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    }}
                    .header {{
                        text-align: center;
                        border-bottom: 3px solid #0066cc;
                        padding-bottom: 20px;
                        margin-bottom: 30px;
                    }}
                    .header h1 {{
                        color: #0066cc;
                        margin: 0;
                    }}
                    .header p {{
                        color: #666;
                        margin: 10px 0 0 0;
                    }}
                    .resumo-executivo {{
                        background-color: #e8f4fd;
                        padding: 20px;
                        border-radius: 8px;
                        margin-bottom: 30px;
                        border-left: 5px solid #0066cc;
                    }}
                    .resumo-executivo h3 {{
                        color: #0066cc;
                        margin-top: 0;
                    }}
                    .item {{
                        margin-bottom: 30px;
                        padding: 20px;
                        border: 1px solid #ddd;
                        border-radius: 8px;
                        background-color: #fafafa;
                    }}
                    .item-header {{
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 15px;
                    }}
                    .titulo {{
                        font-size: 18px;
                        font-weight: bold;
                        color: #333;
                        margin: 0;
                    }}
                    .tipo {{
                        background-color: #0066cc;
                        color: white;
                        padding: 5px 10px;
                        border-radius: 15px;
                        font-size: 12px;
                        font-weight: bold;
                    }}
                    .data {{
                        color: #666;
                        font-size: 14px;
                    }}
                    .resumo {{
                        margin: 15px 0;
                        text-align: justify;
                        line-height: 1.8;
                    }}
                    .link {{
                        margin-top: 15px;
                    }}
                    .link a {{
                        color: #0066cc;
                        text-decoration: none;
                        font-weight: bold;
                    }}
                    .link a:hover {{
                        text-decoration: underline;
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 40px;
                        padding-top: 20px;
                        border-top: 1px solid #ddd;
                        color: #666;
                    }}
                    .sem-documentos {{
                        text-align: center;
                        color: #666;
                        font-style: italic;
                        padding: 40px;
                        background-color: #f9f9f9;
                        border-radius: 8px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Relatório Diário - Banco Central do Brasil</h1>
                        <p>Comunicados, Resoluções e Circulares do dia {data_atual}</p>
                    </div>
                    
                    <div class="resumo-executivo">
                        <h3>Resumo Executivo</h3>
                        <p><strong>Total de documentos encontrados:</strong> {len(informacoes_processadas)}</p>
                        <p><strong>Comunicados:</strong> {len(comunicados)} | <strong>Resoluções:</strong> {len(resolucoes)} | <strong>Circulares:</strong> {len(circulares)}</p>
                        <p><strong>Data de processamento:</strong> {datetime.now().strftime("%d/%m/%Y às %H:%M:%S")}</p>
                    </div>
            """
            
            # Adiciona comunicados
            if comunicados:
                html_body += "<h2 style='color: #0066cc; border-bottom: 2px solid #0066cc; padding-bottom: 10px;'>COMUNICADOS</h2>"
                for item in comunicados:
                    html_body += self._gerar_item_html(item)
            else:
                html_body += "<div class='sem-documentos'><h3>COMUNICADOS</h3><p>Nenhum comunicado encontrado para o dia de hoje.</p></div>"
            
            # Adiciona resoluções
            if resolucoes:
                html_body += "<h2 style='color: #0066cc; border-bottom: 2px solid #0066cc; padding-bottom: 10px; margin-top: 40px;'>RESOLUÇÕES</h2>"
                for item in resolucoes:
                    html_body += self._gerar_item_html(item)
            else:
                html_body += "<div class='sem-documentos'><h3>RESOLUÇÕES</h3><p>Nenhuma resolução encontrada para o dia de hoje.</p></div>"
            
            # Adiciona circulares
            if circulares:
                html_body += "<h2 style='color: #0066cc; border-bottom: 2px solid #0066cc; padding-bottom: 10px; margin-top: 40px;'>CIRCULARES</h2>"
                for item in circulares:
                    html_body += self._gerar_item_html(item)
            else:
                html_body += "<div class='sem-documentos'><h3>CIRCULARES</h3><p>Nenhuma circular encontrada para o dia de hoje.</p></div>"
            
            html_body += """
                    <div class="footer">
                        <p>Relatório gerado automaticamente pelo Sistema de Monitoramento BACEN - Cielo</p>
                        <p>Para dúvidas ou sugestões, entre em contato com a equipe de TI.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            return html_body
            
        except Exception as e:
            self.logger.error(f"Erro ao criar corpo do email: {str(e)}")
            return ""
    
    def _gerar_item_html(self, item):
        """Gera o HTML para um item individual"""
        return f"""
        <div class="item">
            <div class="item-header">
                <h3 class="titulo">{item['titulo']}</h3>
                <span class="tipo">{item['tipo']}</span>
            </div>
            <div class="data">Data: {item['data']}</div>
            <div class="resumo">
                <strong>Resumo:</strong><br>
                {item['resumo']}
            </div>
            <div class="link">
                <a href="{item['link']}" target="_blank">Acessar documento completo</a>
            </div>
        </div>
        """
    
    def enviar_email(self, informacoes_processadas, assunto_personalizado=None):
        """Envia o email com as informações processadas"""
        try:
            # Configura o servidor SMTP
            server = self.configurar_servidor_smtp()
            
            # Cria a mensagem
            msg = MIMEMultipart('alternative')
            
            # Assunto do email
            data_atual = datetime.now().strftime("%d/%m/%Y")
            assunto = assunto_personalizado or f"Relatório BACEN - {data_atual}"
            msg['Subject'] = assunto
            msg['From'] = EMAIL_USER
            
            # Cria o corpo do email
            html_body = self.criar_corpo_email(informacoes_processadas)
            
            # Adiciona o corpo HTML
            html_part = MIMEText(html_body, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Envia para todos os destinatários
            destinatarios_falharam = []
            destinatarios_sucesso = []
            
            for destinatario in DESTINATARIOS:
                try:
                    msg['To'] = destinatario
                    server.send_message(msg)
                    destinatarios_sucesso.append(destinatario)
                    self.logger.info(f"Email enviado com sucesso para: {destinatario}")
                    
                except Exception as e:
                    destinatarios_falharam.append(destinatario)
                    self.logger.error(f"Erro ao enviar email para {destinatario}: {str(e)}")
            
            server.quit()
            
            # Log do resultado
            self.logger.info(f"Envio concluído. Sucessos: {len(destinatarios_sucesso)}, Falhas: {len(destinatarios_falharam)}")
            
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
                'destinatarios_falharam': DESTINATARIOS,
                'total_enviados': 0,
                'total_falharam': len(DESTINATARIOS)
            }
    
    def enviar_email_simples(self, assunto, corpo_texto):
        """Envia um email simples com texto"""
        try:
            server = self.configurar_servidor_smtp()
            
            msg = MIMEText(corpo_texto, 'plain', 'utf-8')
            msg['Subject'] = assunto
            msg['From'] = EMAIL_USER
            
            destinatarios_sucesso = []
            destinatarios_falharam = []
            
            for destinatario in DESTINATARIOS:
                try:
                    msg['To'] = destinatario
                    server.send_message(msg)
                    destinatarios_sucesso.append(destinatario)
                    self.logger.info(f"Email simples enviado para: {destinatario}")
                    
                except Exception as e:
                    destinatarios_falharam.append(destinatario)
                    self.logger.error(f"Erro ao enviar email simples para {destinatario}: {str(e)}")
            
            server.quit()
            
            return {
                'sucesso': len(destinatarios_sucesso) > 0,
                'destinatarios_sucesso': destinatarios_sucesso,
                'destinatarios_falharam': destinatarios_falharam
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao enviar email simples: {str(e)}")
            return {'sucesso': False, 'erro': str(e)}

if __name__ == "__main__":
    # Exemplo de uso
    enviador = EnviadorEmail()
    
    # Dados de exemplo
    dados_exemplo = [
        {
            'titulo': 'Comunicado Exemplo',
            'tipo': 'Comunicado',
            'data': '01/01/2024',
            'link': 'https://www.bcb.gov.br/exemplo',
            'resumo': 'Este é um exemplo de resumo do comunicado...'
        }
    ]
    
    resultado = enviador.enviar_email(dados_exemplo)
    print(f"Resultado do envio: {resultado}")
