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
    /* Centralizar o botão de traduzir com margem reduzida */
    .center-content {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        margin: 0.5rem 0 !important; /* Margem reduzida para aproximar do conteúdo acima */
    }
    
    /* Centralizar a mensagem de sucesso - seletor mais forte */
    div[data-testid="stSuccessMessage"] {
        text-align: center !important;
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
    }
    
    /* Estilo para o texto dentro da mensagem de sucesso */
    div[data-testid="stSuccessMessage"] > div {
        text-align: center !important;
        width: 100% !important;
    }
    
    /* Estilo para o texto dentro da mensagem de sucesso */
    div[data-testid="stSuccessMessage"] p {
        text-align: center !important;
        width: 100% !important;
        display: block !important;
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
