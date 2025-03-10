"""
Módulo para conversão de Markdown para PDF.
Importa e exporta as funções necessárias diretamente dos módulos fonte.
"""

from markdown_utils import (
    process_footnotes,
    replace_images_in_markdown,
    process_markdown_content,
    extract_images_from_html
)
from pdf_modules import markdown_to_pdf

__all__ = [
    'process_footnotes',
    'replace_images_in_markdown',
    'process_markdown_content',
    'markdown_to_pdf',
    'extract_images_from_html'
]