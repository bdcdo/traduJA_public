"""
Módulo de configuração para a aplicação TraduJA.
Contém configurações de ambiente, logging e diretórios.
"""

import os
import sys
import logging
from pathlib import Path
import tempfile
from dotenv import load_dotenv
from openai import OpenAI

# Configuração de logging
def setup_logging():
    """
    Configura o sistema de logging da aplicação.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

logger = setup_logging()

# Configurações de segurança
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'pdf'}

# Configuração do diretório de uploads
def setup_upload_directory():
    """
    Configura o diretório de uploads com base no ambiente.
    """
    if os.environ.get('STREAMLIT_SERVER_RUNNING'):
        # Em produção (Streamlit Cloud)
        upload_dir = Path('/tmp/traduja_uploads')
    else:
        # Em desenvolvimento local
        upload_dir = Path(tempfile.gettempdir()) / 'traduja_uploads'
    
    upload_dir.mkdir(exist_ok=True)
    return upload_dir

UPLOAD_DIR = setup_upload_directory()

# Adicionar o diretório do projeto ao path
def add_project_root_to_path():
    """
    Adiciona o diretório raiz do projeto ao sys.path para permitir importações relativas.
    """
    current_dir = Path(__file__).parent  # streamlit_app directory
    project_root = current_dir.parent    # parent directory (traduJA_public)
    
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

# Configuração do cliente OpenAI
def get_openai_client():
    """
    Retorna uma instância do cliente OpenAI com a chave API apropriada.
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY não encontrada nas variáveis de ambiente")
    return OpenAI(api_key=api_key)

# Configuração do cliente Mistral
def get_mistral_api_key():
    """
    Retorna a chave API do Mistral.
    """
    api_key = os.getenv('MISTRAL_API_KEY')
    if not api_key:
        raise ValueError("MISTRAL_API_KEY não encontrada nas variáveis de ambiente")
    return api_key

def setup_environment():
    """
    Configura o ambiente da aplicação.
    """
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Adicionar o diretório do projeto ao path
    add_project_root_to_path()
    
    # Verificar se as variáveis de ambiente necessárias estão configuradas
    if not os.getenv('OPENAI_API_KEY'):
        logger.error("OPENAI_API_KEY não encontrada nas variáveis de ambiente")
    
    if not os.getenv('MISTRAL_API_KEY'):
        logger.error("MISTRAL_API_KEY não encontrada nas variáveis de ambiente")
