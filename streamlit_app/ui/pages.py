"""
Módulo com funções para renderização das páginas da aplicação.
"""

import os
import streamlit as st
from ..language_utils import IDIOMAS_SUPORTADOS
from ..translator import traduzir_texto
from ..utils.file_utils import validate_file, cleanup_old_files, save_uploaded_file, process_uploaded_pdf, get_output_filename
from ..utils.session_manager import initialize_session_state, update_processed_text, update_translated_text, update_pdf_bytes
from ..utils.pdf_processor import generate_formatted_pdf
from .components import (
    create_file_uploader, create_language_selectors, create_translate_button,
    create_progress_indicators, create_download_buttons, show_error_message,
    show_success_message, show_api_key_error, show_mistral_api_key_error
)
from ..config import get_openai_client

def render_main_page():
    """
    Renderiza a página principal da aplicação.
    """
    # Inicializar variáveis de session_state
    initialize_session_state()
    
    # Verificar se as variáveis de ambiente necessárias estão configuradas
    if not os.getenv('OPENAI_API_KEY'):
        show_api_key_error()
        return
    
    if not os.getenv('MISTRAL_API_KEY'):
        show_mistral_api_key_error()
        return
    
    # Upload de arquivo
    uploaded_file = create_file_uploader()
    
    if uploaded_file is not None:
        # Validar arquivo
        is_valid, error_message = validate_file(uploaded_file)
        if not is_valid:
            show_error_message(error_message)
            return
        
        # Seletores de idioma
        idioma_origem, idioma_destino = create_language_selectors()
        
        # Botão para traduzir
        traduzir_clicked = create_translate_button(idioma_destino)
        
        if traduzir_clicked:
            process_translation(uploaded_file, idioma_origem, idioma_destino)
        
        # Exibir mensagem de sucesso se a tradução foi concluída
        if st.session_state.mensagem_sucesso:
            show_success_message(st.session_state.mensagem_sucesso)
        
        # Exibir botões de download se os dados estiverem disponíveis
        if st.session_state.processed_text and st.session_state.translated_text:
            display_download_options(idioma_origem, idioma_destino)
    
    # Limpar arquivos antigos periodicamente
    cleanup_old_files()

def process_translation(uploaded_file, idioma_origem, idioma_destino):
    """
    Processa a tradução do arquivo carregado.
    
    Args:
        uploaded_file: Arquivo carregado pelo usuário
        idioma_origem: Idioma de origem
        idioma_destino: Idioma de destino
    """
    try:
        client = get_openai_client()
        
        # Criar indicadores de progresso
        progress_container, progress_bar, status_text = create_progress_indicators()
        
        # Criar container para informações de tokens e custos
        token_info_container = st.empty()
        
        # Fase 1: Processamento do PDF
        status_text.markdown("<div class='status-text'>Lendo o PDF... Isso pode levar alguns instantes.</div>", unsafe_allow_html=True)
        progress_bar.progress(0.1)  # Mostrar algum progresso inicial
        
        # Salvar o arquivo temporariamente
        temp_path = save_uploaded_file(uploaded_file)
        
        try:
            # Processar o PDF
            full_text, success = process_uploaded_pdf(str(temp_path))
            
            if not success:
                show_error_message("Erro ao processar o PDF.")
                return
            
            # Armazenar o texto processado na sessão
            update_processed_text(full_text, get_output_filename(uploaded_file.name))
            
            # Atualizar progresso após processamento do PDF
            progress_bar.progress(0.3)
            status_text.markdown("<div class='status-text'>PDF processado com sucesso! Iniciando tradução...</div>", unsafe_allow_html=True)
            
            # Fase 2: Tradução
            def update_progress(current, total):
                # Ajustar a barra de progresso para começar de 30% (processamento do PDF)
                # e ir até 100% (tradução completa)
                progress = 0.3 + (current / total * 0.7)
                progress_bar.progress(progress)
                status_text.markdown(f"<div class='status-text'>Traduzindo... {current}/{total} linhas ({int((current/total) * 100)}%)</div>", unsafe_allow_html=True)
            
            # Função para atualizar informações de tokens e custos
            def update_token_info(input_tokens, output_tokens, input_cost, output_cost, total_cost):
                # Atualizar na sessão
                from ..utils.session_manager import update_token_info as update_session_token_info
                update_session_token_info(input_tokens, output_tokens, input_cost, output_cost, total_cost)
                
                # Exibir na interface (apenas durante o processo de tradução)
                display_token_info(token_info_container, input_tokens, output_tokens, input_cost, output_cost, total_cost)
            
            # Iniciar a tradução com a barra de progresso e informações de tokens
            texto_traduzido = traduzir_texto(
                full_text, 
                client,
                idioma_origem=IDIOMAS_SUPORTADOS[idioma_origem]["code"],
                idioma_destino=IDIOMAS_SUPORTADOS[idioma_destino]["code"],
                progress_callback=update_progress,
                token_callback=update_token_info
            )
            
            # Armazenar o texto traduzido na sessão
            update_translated_text(texto_traduzido)
            
            # Limpar a barra de progresso, status e o container de tokens
            progress_container.empty()
            status_text.empty()
            token_info_container.empty()  # Limpar o container de tokens para evitar duplicação
            
        finally:
            # Garantir que o arquivo temporário seja sempre removido
            if temp_path.exists():
                temp_path.unlink()
                
    except Exception as e:
        show_error_message(f"Ocorreu um erro inesperado: {str(e)}")

def display_token_info(container=None, input_tokens=None, output_tokens=None, input_cost=None, output_cost=None, total_cost=None):
    """
    Exibe as informações de tokens e custos.
    
    Args:
        container: Container para exibir as informações (opcional)
        input_tokens: Número de tokens de entrada (opcional)
        output_tokens: Número de tokens de saída (opcional)
        input_cost: Custo dos tokens de entrada (opcional)
        output_cost: Custo dos tokens de saída (opcional)
        total_cost: Custo total (opcional)
    """
    # Se não foram fornecidos parâmetros, usar os valores da sessão
    if input_tokens is None and st.session_state.token_info:
        input_tokens = st.session_state.token_info['input_tokens']
        output_tokens = st.session_state.token_info['output_tokens']
        input_cost = st.session_state.token_info['input_cost']
        output_cost = st.session_state.token_info['output_cost']
        total_cost = st.session_state.token_info['total_cost']
    
    # Se não há informações de tokens, não exibir nada
    if input_tokens is None:
        return
    
    # Criar o HTML para exibir as informações
    token_info_html = f"""<div class='token-info'>
        <p><b>Tokens:</b> {input_tokens:,} entrada | {output_tokens:,} saída | {input_tokens + output_tokens:,} total</p>
        <p><b>Custo:</b> ${input_cost:.4f} entrada | ${output_cost:.4f} saída | ${total_cost:.4f} total</p>
    </div>"""
    
    # Exibir no container fornecido ou criar um novo
    if container:
        container.markdown(token_info_html, unsafe_allow_html=True)
    else:
        st.markdown(token_info_html, unsafe_allow_html=True)

def display_download_options(idioma_origem, idioma_destino):
    """
    Exibe as opções de download para os resultados.
    
    Args:
        idioma_origem: Idioma de origem
        idioma_destino: Idioma de destino
    """
    # Gerar PDF formatado se ainda não foi gerado
    if st.session_state.pdf_bytes is None:
        with st.spinner("Gerando PDF formatado..."):
            pdf_bytes = generate_formatted_pdf(st.session_state.translated_text)
            update_pdf_bytes(pdf_bytes)
    
    # Não exibir informações de tokens aqui, pois já estão sendo exibidas no container
    # durante o processo de tradução
    
    # Criar botões de download
    create_download_buttons(idioma_origem, idioma_destino)
    
    # Exibir informações de tokens após criar os botões de download
    display_token_info()
