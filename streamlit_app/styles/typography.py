"""
Módulo com estilos CSS para tipografia da aplicação.
"""

def get_typography_styles():
    """
    Retorna os estilos CSS para tipografia da aplicação.
    
    Returns:
        String contendo os estilos CSS para tipografia
    """
    return """
    /* Título principal centralizado */
    h1 {
        color: var(--text-color);
        font-family: 'Open Sans', sans-serif;
        font-weight: 700;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    /* Subtítulos */
    h3 {
        color: var(--accent-color);
        font-family: 'Open Sans', sans-serif;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Centralizar texto do cabeçalho */
    .stMarkdown p {
        text-align: center;
    }
    
    /* Centralizar o texto de status abaixo da barra de progresso */
    .status-text {
        text-align: center;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    """
