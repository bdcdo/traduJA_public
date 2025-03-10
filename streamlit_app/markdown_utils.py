import re
import base64
import logging

# Configuração do logger
logger = logging.getLogger(__name__)

def process_footnotes(text):
    """
    Processa notas de rodapé no formato [^N] e ${ }^{NÚMERO}$ e converte para o formato HTML.
    
    Args:
        text (str): Texto contendo notas de rodapé
        
    Returns:
        str: Texto com notas de rodapé convertidas para HTML
    """
    # Processa notas no formato [^N]
    text = re.sub(r'\[\^(\d+)\]', r'<sup>\1</sup>', text)
    
    # Processa notas no formato ${ }^{NÚMERO}$
    pattern = r'\$\{ \}\^\{(\d+)\}\$'
    def replace_footnote(match):
        number = match.group(1)
        return f'<sup>{number}</sup>'
    
    return re.sub(pattern, replace_footnote, text)

def replace_images_in_markdown(markdown_str: str, images_dict: dict) -> str:
    """
    Substitui referências de imagens no markdown pelos dados base64 correspondentes.
    
    Args:
        markdown_str (str): String markdown contendo referências de imagens
        images_dict (dict): Dicionário com IDs de imagens e seus dados base64
        
    Returns:
        str: Markdown com imagens substituídas por dados base64
    """
    for img_name, base64_str in images_dict.items():
        markdown_str = markdown_str.replace(f"![{img_name}]({img_name})", f"![{img_name}]({base64_str})")
    return markdown_str

def process_markdown_content(markdown_text: str) -> str:
    """
    Processa o conteúdo markdown aplicando todas as transformações necessárias.
    
    Args:
        markdown_text (str): Texto markdown original
        
    Returns:
        str: Texto markdown processado
    """
    # Processar notas de rodapé
    markdown_text = process_footnotes(markdown_text)
    
    # Aqui podemos adicionar mais processamentos específicos se necessário
    
    return markdown_text

def extract_images_from_html(html):
    """
    Extrai imagens embutidas base64 do HTML.
    Retorna uma lista de tuplas (formato, dados).
    """
    # Encontrar todas imagens base64 no HTML
    pattern = r'<img.*?src="data:image/(.*?);base64,(.*?)".*?>'
    images = re.findall(pattern, html, re.DOTALL)
    return images 