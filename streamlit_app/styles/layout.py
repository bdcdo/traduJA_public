"""
Módulo com estilos CSS para layout da aplicação.
"""

def get_layout_styles():
    """
    Retorna os estilos CSS para layout da aplicação.
    
    Returns:
        String contendo os estilos CSS para layout
    """
    return """
    /* Centralizar o botão de traduzir */
    .center-content {
        display: flex;
        justify-content: center;
        margin: 1rem 0;
    }
    
    /* Container para os botões de download */
    .download-buttons-container {
        margin-top: 1.5rem;
    }
    
    /* Estilo para os botões de download */
    [data-testid="column"] .stButton {
        display: flex;
        justify-content: center;
    }
    
    /* Tamanho fixo para os botões de download */
    [data-testid="column"] .stButton > button {
        min-width: 180px;
        height: auto;
        padding: 0.75rem 1rem;
        text-align: center;
    }
    """
