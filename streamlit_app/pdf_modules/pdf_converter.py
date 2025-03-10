import markdown2
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate
from bs4 import BeautifulSoup
import logging

from pdf_modules.styles import get_custom_styles
from pdf_modules.html_processor import HTMLProcessor
from markdown_utils import process_markdown_content

logger = logging.getLogger(__name__)

def markdown_to_pdf(markdown_text, output_path=None):
    """
    Converte texto markdown para PDF usando ReportLab.
    
    Args:
        markdown_text (str): Texto em formato markdown
        output_path (str, optional): Caminho para salvar o PDF. Se None, retorna os bytes do PDF.
    
    Returns:
        bytes ou None: Se output_path for None, retorna os bytes do PDF. Caso contrário, salva o PDF e retorna None.
    """
    # Processar o conteúdo markdown
    markdown_text = process_markdown_content(markdown_text)
    
    # Converter markdown para HTML usando markdown2 com extras
    html = markdown2.markdown(
        markdown_text,
        extras=[
            'fenced-code-blocks',
            'footnotes',
            'tables',
            'header-ids',
            'code-friendly',
            'cuddled-lists',
            'markdown-in-html',
            'break-on-newline',
            'tables',
            'wiki-tables',
            'metadata',
            'footnotes'  # Garante que as notas de rodapé são processadas
        ]
    )
    
    # Criar buffer ou arquivo de saída
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer if output_path is None else output_path,
        pagesize=A4,
        rightMargin=72, 
        leftMargin=72,
        topMargin=72, 
        bottomMargin=72
    )
    
    # Obter estilos personalizados
    styles = get_custom_styles()
    
    # Criar processador HTML
    processor = HTMLProcessor(styles, doc.width, doc.height)
    
    # Parse o HTML com BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Processar cada elemento
    for element in soup.children:
        processor.process_element(element)
    
    # Adicionar notas de rodapé
    processor.add_footnotes()
    
    # Construir o documento
    doc.build(processor.get_flowables())
    
    # Retornar bytes ou salvar arquivo
    if output_path is None:
        buffer.seek(0)
        return buffer.getvalue()
    return None 