"""
Módulo de estilos CSS para a aplicação.
"""

from .base import get_base_styles
from .components import get_component_styles
from .layout import get_layout_styles
from .typography import get_typography_styles
from ..js.scripts import get_js_scripts

def load_css():
    """
    Carrega todos os estilos CSS e scripts JS.
    
    Returns:
        String contendo todos os estilos CSS e scripts JS
    """
    css = f"""
    <style>
    {get_base_styles()}
    {get_typography_styles()}
    {get_layout_styles()}
    {get_component_styles()}
    </style>
    
    {get_js_scripts()}
    """
    return css
