"""
Módulo para gerenciamento do estado da sessão do Streamlit.
"""

import streamlit as st
from ..language_utils import IDIOMAS_SUPORTADOS

def initialize_session_state():
    """
    Inicializa as variáveis de estado da sessão se elas ainda não existirem.
    """
    # Texto processado do PDF
    if 'processed_text' not in st.session_state:
        st.session_state.processed_text = None
    
    # Texto traduzido
    if 'translated_text' not in st.session_state:
        st.session_state.translated_text = None
    
    # Bytes do PDF gerado
    if 'pdf_bytes' not in st.session_state:
        st.session_state.pdf_bytes = None
    
    # Nome do arquivo de saída
    if 'output_filename' not in st.session_state:
        st.session_state.output_filename = None
    
    # Idiomas selecionados
    if 'idioma_origem' not in st.session_state:
        st.session_state.idioma_origem = "Inglês"
    
    if 'idioma_destino' not in st.session_state:
        st.session_state.idioma_destino = "Português"
    
    # Estado da tradução
    if 'traducao_concluida' not in st.session_state:
        st.session_state.traducao_concluida = False
    
    # Mensagem de sucesso
    if 'mensagem_sucesso' not in st.session_state:
        st.session_state.mensagem_sucesso = None
        
    # Informações de tokens e custos
    if 'token_info' not in st.session_state:
        st.session_state.token_info = None

def update_processed_text(text, filename):
    """
    Atualiza o texto processado e o nome do arquivo na sessão.
    
    Args:
        text: Texto processado
        filename: Nome do arquivo
    """
    st.session_state.processed_text = text
    st.session_state.output_filename = filename

def update_translated_text(text):
    """
    Atualiza o texto traduzido na sessão e marca a tradução como concluída.
    
    Args:
        text: Texto traduzido
    """
    st.session_state.translated_text = text
    st.session_state.traducao_concluida = True
    st.session_state.mensagem_sucesso = "Tradução concluída com sucesso!"

def update_pdf_bytes(pdf_bytes):
    """
    Atualiza os bytes do PDF na sessão.
    
    Args:
        pdf_bytes: Bytes do PDF gerado
    """
    st.session_state.pdf_bytes = pdf_bytes

def get_idioma_origem_index():
    """
    Retorna o índice do idioma de origem na lista de idiomas suportados.
    
    Returns:
        Índice do idioma de origem
    """
    return list(IDIOMAS_SUPORTADOS.keys()).index(st.session_state.idioma_origem)

def get_idioma_destino_index():
    """
    Retorna o índice do idioma de destino na lista de idiomas suportados.
    
    Returns:
        Índice do idioma de destino
    """
    return list(IDIOMAS_SUPORTADOS.keys()).index(st.session_state.idioma_destino)

def update_idioma_origem(idioma):
    """
    Atualiza o idioma de origem na sessão.
    
    Args:
        idioma: Novo idioma de origem
    """
    st.session_state.idioma_origem = idioma

def update_idioma_destino(idioma):
    """
    Atualiza o idioma de destino na sessão.
    
    Args:
        idioma: Novo idioma de destino
    """
    st.session_state.idioma_destino = idioma

def reset_translation_state():
    """
    Reseta o estado da tradução.
    """
    st.session_state.processed_text = None
    st.session_state.translated_text = None
    st.session_state.pdf_bytes = None
    st.session_state.output_filename = None
    st.session_state.traducao_concluida = False
    st.session_state.mensagem_sucesso = None

def update_token_info(input_tokens, output_tokens, input_cost, output_cost, total_cost):
    """
    Atualiza as informações de tokens e custos na sessão.
    
    Args:
        input_tokens: Número de tokens de entrada
        output_tokens: Número de tokens de saída
        input_cost: Custo dos tokens de entrada
        output_cost: Custo dos tokens de saída
        total_cost: Custo total
    """
    st.session_state.token_info = {
        'input_tokens': input_tokens,
        'output_tokens': output_tokens,
        'input_cost': input_cost,
        'output_cost': output_cost,
        'total_cost': total_cost
    }
