"""
Módulo com estilos CSS para componentes da aplicação.
"""

def get_component_styles():
    """
    Retorna os estilos CSS para componentes da aplicação.
    
    Returns:
        String contendo os estilos CSS para componentes
    """
    return """
    /* Botões */
    .stButton > button {
        font-weight: 600;
        border-radius: 5px;
        height: 2.5rem;
        transition: all 0.2s ease;
        background-color: var(--accent-color);
        color: white;
        white-space: pre-wrap;
        line-height: 1.2;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        background-color: #005b8c;
    }
    
    /* Estilo para o botão de traduzir */
    [data-testid="baseButton-secondary"] {
        background-color: var(--accent-color);
        color: white;
        padding: 0.5rem 2rem;
        font-weight: 600;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        font-size: 1rem;
        transition: all 0.2s ease;
    }
    
    [data-testid="baseButton-secondary"]:hover {
        background-color: #005b8c;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    """
