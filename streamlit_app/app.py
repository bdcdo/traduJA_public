import streamlit as st
import os
import tempfile
import sys
import io
import base64
import logging
from typing import Optional, Tuple
from pathlib import Path
from openai import OpenAI
import time
from datetime import datetime
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configurações de segurança
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'pdf'}

# Configuração do diretório de uploads para Streamlit Cloud
if os.environ.get('STREAMLIT_SERVER_RUNNING'):
    # Em produção (Streamlit Cloud)
    UPLOAD_DIR = Path('/tmp/traduja_uploads')
else:
    # Em desenvolvimento local
    UPLOAD_DIR = Path(tempfile.gettempdir()) / 'traduja_uploads'

UPLOAD_DIR.mkdir(exist_ok=True)

# Adicionar o diretório do projeto ao path
def add_project_root_to_path():
    """
    Adiciona o diretório raiz do projeto ao sys.path para permitir importações relativas.
    """
    current_dir = Path(__file__).parent
    if str(current_dir) not in sys.path:
        sys.path.append(str(current_dir))

add_project_root_to_path()

from ocr_mistral_md import process_pdf_ocr
from pdf_modules import markdown_to_pdf
from css import load_css
from translator import traduzir_texto, NOMES_IDIOMAS
from markdown_utils import process_markdown_content, extract_images_from_html

# Configuração do cliente OpenAI
def get_openai_client():
    """
    Retorna uma instância do cliente OpenAI com a chave API apropriada.
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY não encontrada nas variáveis de ambiente")
    return OpenAI(api_key=api_key)

def validate_file(file) -> Tuple[bool, str]:
    """
    Valida o arquivo carregado.
    
    Args:
        file: Arquivo carregado pelo usuário
        
    Returns:
        Tuple contendo um booleano indicando se o arquivo é válido e uma mensagem de erro
    """
    if file.size > MAX_FILE_SIZE:
        return False, f"Arquivo muito grande. Tamanho máximo permitido: {MAX_FILE_SIZE / (1024*1024):.1f}MB"
    
    if not file.type == 'application/pdf':
        return False, "Apenas arquivos PDF são permitidos"
    
    return True, ""

def cleanup_old_files():
    """
    Remove arquivos temporários mais antigos que 1 hora.
    """
    try:
        current_time = time.time()
        for file in UPLOAD_DIR.glob('*'):
            if file.stat().st_mtime < current_time - 3600:  # 1 hora
                file.unlink()
    except Exception as e:
        logger.error(f"Erro ao limpar arquivos antigos: {str(e)}")

def process_uploaded_pdf(temp_path: str) -> Tuple[str, bool]:
    """
    Processa o arquivo PDF e extrai o texto.
    
    Args:
        temp_path: Caminho do arquivo PDF temporário
        
    Returns:
        Tuple contendo o texto extraído e um booleano indicando sucesso
    """
    try:
        extracted_pages = process_pdf_ocr(temp_path)
        
        # Combinar todas as páginas em um único texto
        full_text = "\n\n---\n\n".join(extracted_pages)
        return full_text, True
        
    except Exception as e:
        logger.error(f"Erro ao processar PDF: {str(e)}", exc_info=True)
        return str(e), False

def generate_formatted_pdf(markdown_text: str) -> Optional[bytes]:
    """
    Gera um PDF formatado a partir do texto markdown.
    
    Args:
        markdown_text: Texto em formato markdown
        
    Returns:
        Bytes do PDF gerado ou None em caso de erro
    """
    try:
        return markdown_to_pdf(markdown_text)
    except Exception as e:
        logger.error(f"Erro ao gerar PDF formatado: {str(e)}", exc_info=True)
        return None

def display_pdf_preview(pdf_bytes: bytes) -> None:
    """
    Exibe uma prévia do PDF na interface.
    
    Args:
        pdf_bytes: Bytes do PDF a ser exibido
    """
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64.b64encode(pdf_bytes).decode()}" width="100%" height="500" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def main():
    # Configuração da página
    st.set_page_config(
        page_title="TraduJA - Conversor PDF para Markdown",
        page_icon="📄",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Verificar se as variáveis de ambiente necessárias estão configuradas
    if not os.getenv('OPENAI_API_KEY'):
        st.error("""
        ⚠️ Configuração necessária:
        
        A chave API do OpenAI não está configurada. Por favor, configure a variável de ambiente `OPENAI_API_KEY` no Streamlit Cloud.
        
        Para configurar:
        1. Acesse as configurações do seu app no Streamlit Cloud
        2. Vá para a seção "Secrets"
        3. Adicione a variável `OPENAI_API_KEY` com sua chave
        """)
        return

    # Aplicar CSS personalizado
    st.markdown(load_css(), unsafe_allow_html=True)
    
    # Dicionário de idiomas suportados
    IDIOMAS_SUPORTADOS = {
        "Inglês": "en",
        "Português": "pt",
        "Espanhol": "es",
        "Francês": "fr",
        "Alemão": "de",
        "Italiano": "it"
    }
    
    # Cabeçalho
    st.title("TraduJÁ")
    st.markdown("""
    ### Utilize IA para finalmente entender!
    
    Faça upload de um arquivo PDF para traduzi-lo para o idioma desejado.
    """)
    
    # Upload de arquivo
    uploaded_file = st.file_uploader("Escolha um arquivo PDF", type=["pdf"])
    
    if uploaded_file is not None:
        # Validar arquivo
        is_valid, error_message = validate_file(uploaded_file)
        if not is_valid:
            st.error(error_message)
            return
        
        # Seletores de idioma
        col1, col2 = st.columns(2)
        
        with col1:
            idioma_origem = st.selectbox(
                "Idioma do documento original:",
                options=list(IDIOMAS_SUPORTADOS.keys()),
                index=0  # Inglês como padrão
            )
        
        with col2:
            idioma_destino = st.selectbox(
                "Idioma para tradução:",
                options=list(IDIOMAS_SUPORTADOS.keys()),
                index=1  # Português como padrão
            )
        
        # Botão para traduzir o arquivo (processamento + tradução em sequência)
        if st.button(f"Traduzir para {idioma_destino}"):
            try:
                client = get_openai_client()
                
                # Criar um container para a barra de progresso
                progress_container = st.empty()
                progress_bar = progress_container.progress(0)
                status_text = st.empty()
                
                # Fase 1: Processamento do PDF
                status_text.text("Lendo o PDF... Isso pode levar alguns instantes.")
                progress_bar.progress(0.1)  # Mostrar algum progresso inicial
                
                # Criar um arquivo temporário com timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                temp_path = UPLOAD_DIR / f"temp_{timestamp}_{uploaded_file.name}"
                
                # Salvar o arquivo
                with open(temp_path, 'wb') as temp_file:
                    temp_file.write(uploaded_file.getbuffer())
                
                try:
                    # Processar o PDF
                    full_text, success = process_uploaded_pdf(str(temp_path))
                    
                    if not success:
                        st.error("Erro ao processar o PDF.")
                        return
                    
                    # Armazenar o texto processado na sessão
                    st.session_state.processed_text = full_text
                    
                    # Atualizar progresso após processamento do PDF
                    progress_bar.progress(0.3)
                    status_text.text("PDF processado com sucesso! Iniciando tradução...")
                    
                    # Fase 2: Tradução
                    def update_progress(current, total):
                        # Ajustar a barra de progresso para começar de 30% (processamento do PDF)
                        # e ir até 100% (tradução completa)
                        progress = 0.3 + (current / total * 0.7)
                        progress_bar.progress(progress)
                        status_text.text(f"Traduzindo... {current}/{total} linhas ({int((current/total) * 100)}%)")
                    
                    # Iniciar a tradução com a barra de progresso
                    texto_traduzido = traduzir_texto(
                        full_text, 
                        client,
                        idioma_origem=IDIOMAS_SUPORTADOS[idioma_origem],
                        idioma_destino=IDIOMAS_SUPORTADOS[idioma_destino],
                        progress_callback=update_progress
                    )
                    
                    # Limpar a barra de progresso e mostrar sucesso
                    progress_container.empty()
                    status_text.empty()
                    st.success("Tradução concluída com sucesso!")
                    
                    # Exibir o texto original extraído
                    st.markdown("### Texto extraído (formato Markdown):")
                    st.text_area("", full_text, height=200)
                    
                    # Exibir o texto traduzido
                    st.markdown("### Texto traduzido:")
                    st.text_area("", texto_traduzido, height=200)
                    
                    # Criar colunas para os botões de download
                    col1, col2, col3 = st.columns(3)
                    
                    # Botão para download do resultado em Markdown original
                    with col1:
                        output_filename = Path(uploaded_file.name).stem
                        st.download_button(
                            label=f"Baixar Markdown ({idioma_origem})",
                            data=full_text,
                            file_name=f"{output_filename}.md",
                            mime="text/markdown",
                        )
                    
                    # Botão para download do resultado em Markdown traduzido
                    with col2:
                        st.download_button(
                            label=f"Baixar Markdown ({idioma_destino})",
                            data=texto_traduzido,
                            file_name=f"{output_filename}_{IDIOMAS_SUPORTADOS[idioma_destino]}.md",
                            mime="text/markdown",
                        )
                    
                    # Botão para download do PDF formatado
                    with col3:
                        with st.spinner("Gerando PDF formatado..."):
                            pdf_bytes = generate_formatted_pdf(texto_traduzido)
                            
                            if pdf_bytes:
                                st.download_button(
                                    label=f"Baixar PDF ({idioma_destino})",
                                    data=pdf_bytes,
                                    file_name=f"{output_filename}_{IDIOMAS_SUPORTADOS[idioma_destino]}.pdf",
                                    mime="application/pdf",
                                )
                            else:
                                st.error("Não foi possível gerar o PDF formatado")
                                
                finally:
                    # Garantir que o arquivo temporário seja sempre removido
                    if temp_path.exists():
                        temp_path.unlink()
                        
            except Exception as e:
                logger.error("Erro inesperado", exc_info=True)
                st.error(f"Ocorreu um erro inesperado: {str(e)}")
    
    # Limpar arquivos antigos periodicamente
    cleanup_old_files()

if __name__ == "__main__":
    main()
