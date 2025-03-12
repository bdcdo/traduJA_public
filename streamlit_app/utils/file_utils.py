"""
Módulo com utilitários para manipulação de arquivos.
"""

import os
import time
import logging
from typing import Tuple
from datetime import datetime
from pathlib import Path

from ..config import UPLOAD_DIR, MAX_FILE_SIZE, ALLOWED_EXTENSIONS, logger
from ..ocr_mistral_md import process_pdf_ocr

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

def save_uploaded_file(uploaded_file) -> Path:
    """
    Salva o arquivo carregado em um local temporário.
    
    Args:
        uploaded_file: Arquivo carregado pelo usuário
        
    Returns:
        Path do arquivo temporário
    """
    # Criar um arquivo temporário com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_path = UPLOAD_DIR / f"temp_{timestamp}_{uploaded_file.name}"
    
    # Salvar o arquivo
    with open(temp_path, 'wb') as temp_file:
        temp_file.write(uploaded_file.getbuffer())
    
    return temp_path

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
        
        # Combinar todas as páginas em um único texto sem delimitadores
        full_text = "".join(extracted_pages)
        return full_text, True
        
    except Exception as e:
        logger.error(f"Erro ao processar PDF: {str(e)}", exc_info=True)
        return str(e), False

def get_output_filename(original_filename: str) -> str:
    """
    Obtém o nome do arquivo de saída sem a extensão.
    
    Args:
        original_filename: Nome do arquivo original
        
    Returns:
        Nome do arquivo sem extensão
    """
    return Path(original_filename).stem
