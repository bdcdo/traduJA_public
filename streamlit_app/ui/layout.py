"""
Módulo com funções para configuração de layout da aplicação.
"""

import streamlit as st
from ..styles import load_css

def setup_page_config():
    """
    Configura as propriedades da página Streamlit.
    """
    st.set_page_config(
        page_title="TraduJA - Conversor PDF para Markdown",
        page_icon="📄",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

def apply_custom_css():
    """
    Aplica o CSS personalizado à aplicação.
    """
    st.markdown(load_css(), unsafe_allow_html=True)

def create_header():
    """
    Cria o cabeçalho da aplicação.
    """
    st.title("TraduJÁ")
    st.markdown("### Utilize IA para finalmente entender!")

def create_footer():
    """
    Cria o rodapé da aplicação.
    """
    st.markdown("""
    <div style="text-align: center; margin-top: 30px; color: #666;">
        <p>TraduJÁ - Desenvolvido com ❤️ usando Streamlit e OpenAI</p>
    </div>
    """, unsafe_allow_html=True)

def create_centered_container():
    """
    Cria um container centralizado para conteúdo.
    
    Returns:
        Container do Streamlit
    """
    return st.container()

def create_columns(sizes=None):
    """
    Cria colunas com tamanhos específicos.
    
    Args:
        sizes: Lista com os tamanhos relativos das colunas
        
    Returns:
        Lista de colunas do Streamlit
    """
    if sizes is None:
        return st.columns(3)  # Três colunas de tamanho igual
    return st.columns(sizes)
