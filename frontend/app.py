"""
Frontend Streamlit - Interface Web para o Sistema de Monitoramento BACEN
"""

import streamlit as st
import os
import sys
from datetime import datetime
import pandas as pd
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from modulo_scraper import BACENScraper
from modulo_llm import LLMManager
from modulo_report import PDFGenerator
from modulo_email import EmailSender
from config.config import Config


# Configuração da página
st.set_page_config(
    page_title="Sistema de Monitoramento BACEN",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🏦 Sistema de Monitoramento BACEN")
st.markdown("---")

# Inicializa configuração
@st.cache_resource
def get_config():
    """Carrega configuração"""
    return Config()

config = get_config()

# Sidebar - Configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Seleção de provedor LLM
    st.subheader("Provedor LLM")
    provider_options = ['openai', 'claude', 'ollama', 'fallback']
    selected_provider = st.selectbox(
        "Escolha o provedor LLM:",
        provider_options,
        index=provider_options.index(config.LLM_PROVIDER) if hasattr(config, 'LLM_PROVIDER') else 0
    )
    
    # API Key (se necessário)
    if selected_provider != 'fallback' and selected_provider != 'ollama':
        api_key = st.text_input(
            f"API Key ({selected_provider.upper()})",
            type="password",
            value=os.getenv(f"{selected_provider.upper()}_API_KEY", "")
        )
    else:
        api_key = None
    
    st.markdown("---")
    
    # Status do sistema
    st.subheader("📊 Status")
    
    # Verifica se há relatórios recentes
    relatorios_dir = Path("relatorios")
    if relatorios_dir.exists():
        pdfs = list(relatorios_dir.glob("*.pdf"))
        if pdfs:
            ultimo_pdf = max(pdfs, key=lambda p: p.stat().st_mtime)
            st.success(f"✅ Último relatório: {ultimo_pdf.name}")
        else:
            st.warning("⚠️ Nenhum relatório encontrado")
    else:
        st.warning("⚠️ Diretório de relatórios não existe")

# Abas principais
tab1, tab2, tab3, tab4 = st.tabs(["📋 Executar Coleta", "📊 Relatórios", "📧 Email", "📝 Logs"])

# Aba 1: Executar Coleta
with tab1:
    st.header("Executar Coleta e Processamento")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Coleta de Dados")
        if st.button("🔄 Executar Coleta", type="primary"):
            with st.spinner("Coletando dados do BACEN..."):
                try:
                    scraper = BACENScraper(config)
                    dados_coletados = scraper.executar_coleta()
                    
                    if dados_coletados:
                        st.success(f"✅ {len(dados_coletados)} documentos coletados!")
                        st.session_state['dados_coletados'] = dados_coletados
                        
                        # Mostra preview
                        st.subheader("Preview dos Dados Coletados")
                        df = pd.DataFrame(dados_coletados)
                        st.dataframe(df[['titulo', 'tipo', 'data']], use_container_width=True)
                    else:
                        st.warning("⚠️ Nenhum documento encontrado")
                        
                except Exception as e:
                    st.error(f"❌ Erro na coleta: {str(e)}")
    
    with col2:
        st.subheader("Processamento com LLM")
        
        if 'dados_coletados' in st.session_state and st.session_state['dados_coletados']:
            if st.button("🤖 Processar com LLM", type="primary"):
                with st.spinner("Processando com LLM..."):
                    try:
                        llm_manager = LLMManager(
                            provider_name=selected_provider,
                            api_key=api_key
                        )
                        
                        informacoes_processadas = []
                        progress_bar = st.progress(0)
                        
                        for idx, item in enumerate(st.session_state['dados_coletados']):
                            texto = item.get('conteudo_completo', '')
                            titulo = item.get('titulo', '')
                            link = item.get('link', '')
                            
                            if texto:
                                resumo = llm_manager.summarize(
                                    texto=texto,
                                    titulo=titulo,
                                    link=link,
                                    max_lines=5
                                )
                                item['resumo'] = resumo
                            
                            informacoes_processadas.append(item)
                            progress_bar.progress((idx + 1) / len(st.session_state['dados_coletados']))
                        
                        st.session_state['informacoes_processadas'] = informacoes_processadas
                        st.success(f"✅ {len(informacoes_processadas)} documentos processados!")
                        
                    except Exception as e:
                        st.error(f"❌ Erro no processamento: {str(e)}")
        else:
            st.info("ℹ️ Execute a coleta primeiro")

# Aba 2: Relatórios
with tab2:
    st.header("Relatórios Gerados")
    
    # Lista de relatórios PDF
    relatorios_dir = Path("relatorios")
    if relatorios_dir.exists():
        pdfs = sorted(relatorios_dir.glob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True)
        
        if pdfs:
            st.subheader("Relatórios Disponíveis")
            
            for pdf in pdfs[:10]:  # Mostra últimos 10
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"📄 {pdf.name}")
                    st.caption(f"Modificado: {datetime.fromtimestamp(pdf.stat().st_mtime).strftime('%d/%m/%Y %H:%M')}")
                
                with col2:
                    with open(pdf, 'rb') as f:
                        st.download_button(
                            "⬇️ Download",
                            f.read(),
                            file_name=pdf.name,
                            mime="application/pdf",
                            key=f"download_{pdf.name}"
                        )
                
                with col3:
                    if st.button("🗑️", key=f"delete_{pdf.name}"):
                        pdf.unlink()
                        st.rerun()
            
            # Gerar novo relatório
            if 'informacoes_processadas' in st.session_state:
                st.markdown("---")
                st.subheader("Gerar Novo Relatório PDF")
                
                if st.button("📄 Gerar PDF", type="primary"):
                    with st.spinner("Gerando PDF..."):
                        try:
                            generator = PDFGenerator()
                            caminho_pdf = generator.generate_pdf(
                                st.session_state['informacoes_processadas']
                            )
                            st.success(f"✅ PDF gerado: {caminho_pdf}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro ao gerar PDF: {str(e)}")
        else:
            st.info("ℹ️ Nenhum relatório encontrado")
    else:
        st.warning("⚠️ Diretório de relatórios não existe")

# Aba 3: Email
with tab3:
    st.header("Envio de Email")
    
    if 'informacoes_processadas' in st.session_state:
        st.subheader("Enviar Relatório por Email")
        
        # Seleção de PDF
        relatorios_dir = Path("relatorios")
        pdfs = sorted(relatorios_dir.glob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True) if relatorios_dir.exists() else []
        
        if pdfs:
            pdf_selecionado = st.selectbox(
                "Selecione o PDF para enviar:",
                [pdf.name for pdf in pdfs]
            )
            
            assunto = st.text_input(
                "Assunto do Email:",
                value=f"Relatório BACEN - {datetime.now().strftime('%d/%m/%Y')}"
            )
            
            if st.button("📧 Enviar Email", type="primary"):
                with st.spinner("Enviando email..."):
                    try:
                        email_sender = EmailSender(config)
                        caminho_pdf = relatorios_dir / pdf_selecionado
                        
                        corpo_html = email_sender.criar_corpo_email_html(
                            st.session_state['informacoes_processadas']
                        )
                        
                        resultado = email_sender.enviar_email_com_anexo(
                            assunto=assunto,
                            corpo_html=corpo_html,
                            caminho_pdf=str(caminho_pdf)
                        )
                        
                        if resultado['sucesso']:
                            st.success(f"✅ Email enviado para {resultado['total_enviados']} destinatário(s)")
                        else:
                            st.error(f"❌ Erro no envio: {resultado.get('erro', 'Erro desconhecido')}")
                            
                    except Exception as e:
                        st.error(f"❌ Erro ao enviar email: {str(e)}")
        else:
            st.warning("⚠️ Nenhum PDF disponível para envio")
    else:
        st.info("ℹ️ Processe os dados primeiro")

# Aba 4: Logs
with tab4:
    st.header("Logs do Sistema")
    
    log_files = {
        "Scraper": "logs/scraper.log",
        "LLM": "logs/llm.log",
        "PDF": "logs/pdf_generator.log",
        "Email": "logs/email_sender.log",
        "Scheduler": "logs/scheduler.log"
    }
    
    log_selecionado = st.selectbox("Selecione o log:", list(log_files.keys()))
    
    log_path = log_files[log_selecionado]
    
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            ultimas_linhas = linhas[-100:] if len(linhas) > 100 else linhas
            
        st.text_area(
            "Últimas 100 linhas:",
            value=''.join(ultimas_linhas),
            height=400
        )
        
        if st.button("🔄 Atualizar"):
            st.rerun()
    else:
        st.warning(f"⚠️ Arquivo de log não encontrado: {log_path}")

# Rodapé
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Sistema de Monitoramento BACEN - Desenvolvido para Cielo<br/>"
    f"Versão 2.0 - {datetime.now().strftime('%Y')}"
    "</div>",
    unsafe_allow_html=True
)

