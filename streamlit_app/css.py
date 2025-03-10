"""
Módulo com estilos CSS para melhorar a aparência da aplicação Streamlit.
"""

def load_css():
    """
    Retorna o CSS customizado para a aplicação.
    """
    return """
    <style>
    /* Estilo global */
    .main .block-container {
        padding-top: 2rem;
    }
    
    /* Título principal */
    h1 {
        color: #2c3e50;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }
    
    /* Subtítulos */
    h3 {
        color: #2980b9;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Botões */
    .stButton > button {
        font-weight: 600;
        border-radius: 5px;
        height: 2.5rem;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Área de texto */
    .stTextArea textarea {
        border-radius: 5px;
        border: 1px solid #e0e0e0;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-width: 3px;
    }
    
    /* Detalhes do arquivo */
    .css-nahz7x {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    
    /* Mensagem de sucesso */
    .css-1siy2j7 {
        font-weight: 600;
        padding: 0.75rem 1rem;
    }
    
    /* Iframe do PDF */
    iframe {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    </style>
    """