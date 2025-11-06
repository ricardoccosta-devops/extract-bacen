"""
Módulo de Geração de Relatórios PDF
"""

import os
import logging
from datetime import datetime
from typing import List, Dict
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class PDFGenerator:
    """Gerador de relatórios PDF profissionais"""
    
    def __init__(self, output_dir: str = "relatorios"):
        """
        Inicializa o gerador PDF
        
        Args:
            output_dir: Diretório para salvar os PDFs
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.setup_logging()
        self.setup_fonts()
        self.setup_styles()
    
    def setup_logging(self):
        """Configura logging"""
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(log_dir, 'pdf_generator.log')),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_fonts(self):
        """Configura fontes (tenta carregar fontes customizadas)"""
        try:
            # Tenta registrar fonte Arial (comum no Windows)
            try:
                pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
                pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))
            except:
                # Se não encontrar, usa fontes padrão
                pass
        except Exception as e:
            self.logger.warning(f"Não foi possível carregar fontes customizadas: {str(e)}")
    
    def setup_styles(self):
        """Configura estilos do PDF"""
        styles = getSampleStyleSheet()
        
        # Estilo para título principal
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=HexColor('#0066CC'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Estilo para subtítulo
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=HexColor('#333333'),
            spaceAfter=20,
            spaceBefore=20,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        )
        
        # Estilo para título de documento
        self.doc_title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=HexColor('#000000'),
            spaceAfter=10,
            spaceBefore=15,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        )
        
        # Estilo para corpo do texto
        self.body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontSize=10,
            textColor=HexColor('#333333'),
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            leading=14
        )
        
        # Estilo para link
        self.link_style = ParagraphStyle(
            'Link',
            parent=styles['Normal'],
            fontSize=9,
            textColor=HexColor('#0066CC'),
            spaceAfter=15,
            alignment=TA_LEFT
        )
        
        # Estilo para rodapé
        self.footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=HexColor('#666666'),
            spaceAfter=0,
            alignment=TA_CENTER
        )
    
    def generate_pdf(self, informacoes_processadas: List[Dict], data_referencia: str = None) -> str:
        """
        Gera relatório PDF completo
        
        Args:
            informacoes_processadas: Lista de documentos processados
            data_referencia: Data de referência (formato DD/MM/YYYY)
            
        Returns:
            Caminho do arquivo PDF gerado
        """
        try:
            if data_referencia is None:
                data_referencia = datetime.now().strftime("%d/%m/%Y")
            
            # Nome do arquivo
            data_arquivo = datetime.now().strftime("%Y%m%d")
            nome_arquivo = f"relatorio_bacen_{data_arquivo}.pdf"
            caminho_completo = os.path.join(self.output_dir, nome_arquivo)
            
            # Cria o documento PDF
            doc = SimpleDocTemplate(
                caminho_completo,
                pagesize=A4,
                rightMargin=2*cm,
                leftMargin=2*cm,
                topMargin=2*cm,
                bottomMargin=2*cm
            )
            
            # Constrói o conteúdo
            story = []
            
            # Cabeçalho
            story.append(Paragraph("Banco Central do Brasil", self.title_style))
            story.append(Paragraph("Relatório Diário de Publicações", self.subtitle_style))
            story.append(Paragraph(f"Data: {data_referencia}", self.body_style))
            story.append(Spacer(1, 0.5*cm))
            
            # Resumo executivo
            comunicados = [item for item in informacoes_processadas if item.get('tipo') == 'Comunicado']
            resolucoes = [item for item in informacoes_processadas if item.get('tipo') == 'Resolução']
            circulares = [item for item in informacoes_processadas if item.get('tipo') == 'Circular']
            
            resumo_texto = (
                f"<b>Resumo Executivo</b><br/>"
                f"Total de documentos: {len(informacoes_processadas)}<br/>"
                f"Comunicados: {len(comunicados)} | "
                f"Resoluções: {len(resolucoes)} | "
                f"Circulares: {len(circulares)}"
            )
            story.append(Paragraph(resumo_texto, self.body_style))
            story.append(Spacer(1, 0.5*cm))
            
            # Agrupa por tipo
            tipos_ordem = ['Comunicado', 'Resolução', 'Circular']
            
            for tipo in tipos_ordem:
                documentos_tipo = [item for item in informacoes_processadas if item.get('tipo') == tipo]
                
                if documentos_tipo:
                    story.append(Paragraph(f"<b>{tipo.upper()}S</b>", self.subtitle_style))
                    
                    for item in documentos_tipo:
                        # Título do documento
                        titulo = item.get('titulo', 'Sem título')
                        story.append(Paragraph(f"<b>{titulo}</b>", self.doc_title_style))
                        
                        # Data
                        data = item.get('data', '')
                        if data:
                            story.append(Paragraph(f"Data: {data}", self.body_style))
                        
                        # Resumo
                        resumo = item.get('resumo', '')
                        if resumo:
                            # Remove formatação markdown básica
                            resumo_limpo = resumo.replace('**', '').replace('🔗', '')
                            story.append(Paragraph(resumo_limpo, self.body_style))
                        
                        # Link
                        link = item.get('link', '')
                        if link:
                            link_texto = f"🔗 Leia na íntegra: {link}"
                            story.append(Paragraph(link_texto, self.link_style))
                        
                        story.append(Spacer(1, 0.3*cm))
                    
                    story.append(Spacer(1, 0.5*cm))
            
            # Rodapé
            story.append(Spacer(1, 1*cm))
            rodape_texto = (
                f"Relatório gerado automaticamente pelo Sistema de Monitoramento BACEN<br/>"
                f"Data de processamento: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}"
            )
            story.append(Paragraph(rodape_texto, self.footer_style))
            
            # Gera o PDF
            doc.build(story)
            
            self.logger.info(f"PDF gerado com sucesso: {caminho_completo}")
            return caminho_completo
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar PDF: {str(e)}")
            raise


if __name__ == "__main__":
    # Teste do módulo
    generator = PDFGenerator()
    
    dados_teste = [
        {
            'titulo': 'Comunicado de Teste',
            'tipo': 'Comunicado',
            'data': '01/01/2024',
            'link': 'https://www.bcb.gov.br/exemplo',
            'resumo': 'Este é um resumo de teste do comunicado.'
        }
    ]
    
    caminho = generator.generate_pdf(dados_teste)
    print(f"PDF gerado em: {caminho}")

