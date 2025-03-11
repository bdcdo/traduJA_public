"""
Aplicação principal do TraduJA.
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório pai ao sys.path para permitir importações do pacote streamlit_app
current_dir = Path(__file__).parent
project_root = current_dir.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import streamlit as st
from streamlit_app.config import setup_environment
from streamlit_app.ui.layout import setup_page_config, apply_custom_css, create_header
from streamlit_app.ui.pages import render_main_page

def main():
    """
    Função principal da aplicação.
    """
    # Configuração do ambiente
    setup_environment()
    
    # Configuração da página
    setup_page_config()
    
    # Aplicar CSS personalizado
    apply_custom_css()
    
    # Cabeçalho
    create_header()
    
    # Renderizar a página principal
    render_main_page()

if __name__ == "__main__":
    main()
