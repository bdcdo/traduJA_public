"""
Módulo com componentes de UI reutilizáveis.
"""

import streamlit as st
from ..language_utils import IDIOMAS_SUPORTADOS
from ..utils.pdf_processor import display_pdf_preview

def create_file_uploader():
    """
    Cria o componente de upload de arquivo.
    
    Returns:
        O arquivo carregado ou None
    """
    return st.file_uploader(
        "Faça upload de um arquivo PDF para traduzi-lo para o idioma desejado.", 
        type=["pdf"],
        help="Arraste e solte seu arquivo PDF aqui ou clique para selecionar um arquivo. Limite de 10MB por arquivo."
    )

def create_language_selectors():
    """
    Cria os seletores de idioma de origem e destino.
    
    Returns:
        Tuple contendo os idiomas selecionados (origem, destino)
    """
    col1, col3 = st.columns([1, 1])
    
    with col1:
        st.markdown("**Idioma do documento original:**")
        idioma_origem_index = list(IDIOMAS_SUPORTADOS.keys()).index(st.session_state.idioma_origem)
        idioma_origem = st.selectbox(
            "",
            options=list(IDIOMAS_SUPORTADOS.keys()),
            index=idioma_origem_index,
            key="select_origem",
            label_visibility="collapsed"
        )
        st.session_state.idioma_origem = idioma_origem
    
    with col3:
        st.markdown("**Idioma para tradução:**")
        idioma_destino_index = list(IDIOMAS_SUPORTADOS.keys()).index(st.session_state.idioma_destino)
        idioma_destino = st.selectbox(
            "",
            options=list(IDIOMAS_SUPORTADOS.keys()),
            index=idioma_destino_index,
            key="select_destino",
            label_visibility="collapsed"
        )
        st.session_state.idioma_destino = idioma_destino
    
    return idioma_origem, idioma_destino

def create_translate_button(idioma_destino):
    """
    Cria o botão de tradução personalizado.
    
    Args:
        idioma_destino: Idioma de destino para exibir no botão
        
    Returns:
        Boolean indicando se o botão foi clicado
    """
    # Botão personalizado (visual)
    st.markdown(
        f"""<div class="center-content">
            <button id="traduzir-btn" class="stButton">
                Traduzir para {idioma_destino}
            </button>
        </div>""",
        unsafe_allow_html=True
    )
    
    # Botão real (escondido) que será acionado pelo JavaScript
    traduzir_container = st.container()
    with traduzir_container:
        return st.button("Traduzir", key="traduzir_real")

def create_progress_indicators():
    """
    Cria os indicadores de progresso (barra e texto).
    
    Returns:
        Tuple contendo (container_progresso, barra_progresso, texto_status)
    """
    progress_container = st.empty()
    progress_bar = progress_container.progress(0)
    status_text = st.empty()
    
    return progress_container, progress_bar, status_text

def create_download_buttons(idioma_origem, idioma_destino):
    """
    Cria os botões de download para os resultados.
    
    Args:
        idioma_origem: Idioma de origem
        idioma_destino: Idioma de destino
    """
    st.markdown("<div class='download-buttons-container'>", unsafe_allow_html=True)
    
    # Criar três colunas iguais para os botões
    col1, col2, col3 = st.columns(3)
    
    # Botão para download do resultado em Markdown original
    with col1:
        st.download_button(
            label=f"Baixar Markdown\n({idioma_origem})",
            data=st.session_state.processed_text,
            file_name=f"{st.session_state.output_filename}.md",
            mime="text/markdown",
            key="btn_md_original",
            use_container_width=True
        )
    
    # Botão para download do resultado em Markdown traduzido
    with col2:
        st.download_button(
            label=f"Baixar Markdown\n({idioma_destino})",
            data=st.session_state.translated_text,
            file_name=f"{st.session_state.output_filename}_{IDIOMAS_SUPORTADOS[idioma_destino]['code']}.md",
            mime="text/markdown",
            key="btn_md_traduzido",
            use_container_width=True
        )
    
    # Botão para download do PDF formatado
    with col3:
        if st.session_state.pdf_bytes:
            st.download_button(
                label=f"Baixar PDF\n({idioma_destino})",
                data=st.session_state.pdf_bytes,
                file_name=f"{st.session_state.output_filename}_{IDIOMAS_SUPORTADOS[idioma_destino]['code']}.pdf",
                mime="application/pdf",
                key="btn_pdf",
                use_container_width=True
            )
        else:
            st.error("Não foi possível gerar o PDF formatado")
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_pdf_preview(pdf_bytes):
    """
    Exibe uma prévia do PDF na interface.
    
    Args:
        pdf_bytes: Bytes do PDF a ser exibido
    """
    pdf_html = display_pdf_preview(pdf_bytes)
    st.markdown(pdf_html, unsafe_allow_html=True)

def show_error_message(message):
    """
    Exibe uma mensagem de erro.
    
    Args:
        message: Mensagem de erro a ser exibida
    """
    st.error(message)

def show_success_message(message):
    """
    Exibe uma mensagem de sucesso.
    
    Args:
        message: Mensagem de sucesso a ser exibida
    """
    st.success(message)

def show_api_key_error():
    """
    Exibe uma mensagem de erro sobre a chave API do OpenAI.
    """
    st.error("""
    ⚠️ Configuração necessária:
    
    A chave API do OpenAI não está configurada. Por favor, configure a variável de ambiente `OPENAI_API_KEY` no Streamlit Cloud.
    
    Para configurar:
    1. Acesse as configurações do seu app no Streamlit Cloud
    2. Vá para a seção "Secrets"
    3. Adicione a variável `OPENAI_API_KEY` com sua chave
    """)
