import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import re
from config import *

class SumarizadorBACEN:
    def __init__(self):
        self.setup_logging()
        
    def setup_logging(self):
        """Configura o sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('sumarizador.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def obter_conteudo_completo(self, url):
        """Obtém o conteúdo completo de uma página"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove scripts e estilos
            for script in soup(["script", "style"]):
                script.decompose()
            
            return soup.get_text()
            
        except Exception as e:
            self.logger.error(f"Erro ao obter conteúdo da URL {url}: {str(e)}")
            return ""
    
    def extrair_resumo(self, texto_completo, titulo):
        """Extrai um resumo de 10 linhas do texto"""
        try:
            # Limpa o texto
            texto_limpo = re.sub(r'\s+', ' ', texto_completo)
            texto_limpo = texto_limpo.strip()
            
            # Divide em sentenças
            sentencas = re.split(r'[.!?]+', texto_completo)
            sentencas = [s.strip() for s in sentencas if s.strip()]
            
            # Filtra sentenças relevantes baseado em palavras-chave
            palavras_chave = [
                'banco central', 'bacen', 'resolução', 'circular', 'comunicado',
                'normativo', 'regulamentação', 'instituição', 'financeiro',
                'sistema', 'pagamento', 'cartão', 'crédito', 'débito',
                'transação', 'operador', 'adquirente', 'emissor'
            ]
            
            sentencas_relevantes = []
            for sentenca in sentencas:
                if any(palavra.lower() in sentenca.lower() for palavra in palavras_chave):
                    sentencas_relevantes.append(sentenca)
            
            # Se não encontrou sentenças relevantes, usa as primeiras
            if not sentencas_relevantes:
                sentencas_relevantes = sentencas[:15]
            
            # Limita a 10 linhas (aproximadamente 10 sentenças)
            resumo_sentencas = sentencas_relevantes[:10]
            
            # Se ainda não tem 10, completa com outras sentenças
            if len(resumo_sentencas) < 10:
                for sentenca in sentencas:
                    if sentenca not in resumo_sentencas:
                        resumo_sentencas.append(sentenca)
                        if len(resumo_sentencas) >= 10:
                            break
            
            return '. '.join(resumo_sentencas[:10]) + '.'
            
        except Exception as e:
            self.logger.error(f"Erro ao extrair resumo: {str(e)}")
            return texto_completo[:500] + "..." if len(texto_completo) > 500 else texto_completo
    
    def processar_informacoes(self, dados_coletados):
        """Processa todas as informações coletadas e gera resumos"""
        self.logger.info("Iniciando processamento e sumarização das informações...")
        
        informacoes_processadas = []
        
        for item in dados_coletados:
            try:
                self.logger.info(f"Processando: {item['titulo']}")
                
                # Obtém o conteúdo completo
                conteudo_completo = self.obter_conteudo_completo(item['link'])
                
                # Gera o resumo
                resumo = self.extrair_resumo(conteudo_completo, item['titulo'])
                
                # Cria o item processado
                item_processado = {
                    'titulo': item['titulo'],
                    'tipo': item['tipo'],
                    'data': item['data'],
                    'link': item['link'],
                    'resumo': resumo,
                    'data_processamento': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                }
                
                informacoes_processadas.append(item_processado)
                
                self.logger.info(f"Processado com sucesso: {item['titulo']}")
                
            except Exception as e:
                self.logger.error(f"Erro ao processar item {item['titulo']}: {str(e)}")
                continue
        
        self.logger.info(f"Processamento concluído. {len(informacoes_processadas)} itens processados")
        return informacoes_processadas
    
    def gerar_relatorio_html(self, informacoes_processadas):
        """Gera um relatório HTML com as informações processadas"""
        try:
            data_atual = datetime.now().strftime("%d/%m/%Y")
            
            html = f"""
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
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Relatório Diário - Banco Central do Brasil</h1>
                        <p>Comunicados, Resoluções e Circulares do dia {data_atual}</p>
                    </div>
            """
            
            # Agrupa por tipo
            comunicados = [item for item in informacoes_processadas if item['tipo'] == 'Comunicado']
            resolucoes = [item for item in informacoes_processadas if item['tipo'] == 'Resolução']
            circulares = [item for item in informacoes_processadas if item['tipo'] == 'Circular']
            
            # Adiciona comunicados
            if comunicados:
                html += "<h2 style='color: #0066cc; border-bottom: 2px solid #0066cc; padding-bottom: 10px;'>COMUNICADOS</h2>"
                for item in comunicados:
                    html += self._gerar_item_html(item)
            
            # Adiciona resoluções
            if resolucoes:
                html += "<h2 style='color: #0066cc; border-bottom: 2px solid #0066cc; padding-bottom: 10px; margin-top: 40px;'>RESOLUÇÕES</h2>"
                for item in resolucoes:
                    html += self._gerar_item_html(item)
            
            # Adiciona circulares
            if circulares:
                html += "<h2 style='color: #0066cc; border-bottom: 2px solid #0066cc; padding-bottom: 10px; margin-top: 40px;'>CIRCULARES</h2>"
                for item in circulares:
                    html += self._gerar_item_html(item)
            
            html += """
                    <div class="footer">
                        <p>Relatório gerado automaticamente pelo Sistema de Monitoramento BACEN - Cielo</p>
                        <p>Data de processamento: """ + datetime.now().strftime("%d/%m/%Y às %H:%M:%S") + """</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            return html
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar relatório HTML: {str(e)}")
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

if __name__ == "__main__":
    # Exemplo de uso
    sumarizador = SumarizadorBACEN()
    
    # Dados de exemplo
    dados_exemplo = [
        {
            'titulo': 'Comunicado Exemplo',
            'tipo': 'Comunicado',
            'data': '01/01/2024',
            'link': 'https://www.bcb.gov.br/exemplo'
        }
    ]
    
    informacoes_processadas = sumarizador.processar_informacoes(dados_exemplo)
    relatorio_html = sumarizador.gerar_relatorio_html(informacoes_processadas)
    
    # Salva o relatório
    with open('relatorio_bacen.html', 'w', encoding='utf-8') as f:
        f.write(relatorio_html)
    
    print("Relatório gerado com sucesso!")

