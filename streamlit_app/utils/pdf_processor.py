"""
Módulo para processamento de arquivos PDF.
"""

import base64
import logging
from typing import Optional
from io import BytesIO

from ..config import logger
from ..pdf_modules.pdf_converter import markdown_to_pdf

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

def display_pdf_preview(pdf_bytes: bytes) -> str:
    """
    Gera o HTML para exibir uma prévia do PDF na interface.
    
    Args:
        pdf_bytes: Bytes do PDF a ser exibido
        
    Returns:
        HTML para exibir o PDF
    """
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64.b64encode(pdf_bytes).decode()}" width="100%" height="500" type="application/pdf"></iframe>'
    return pdf_display

def get_download_filename(base_filename: str, idioma_code: str, extension: str) -> str:
    """
    Gera o nome do arquivo para download.
    
    Args:
        base_filename: Nome base do arquivo
        idioma_code: Código do idioma
        extension: Extensão do arquivo
        
    Returns:
        Nome do arquivo para download
    """
    return f"{base_filename}_{idioma_code}.{extension}"
