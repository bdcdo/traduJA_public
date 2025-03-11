"""
Módulo com estilos CSS base para a aplicação.
"""

def get_base_styles():
    """
    Retorna os estilos CSS base para a aplicação.
    
    Returns:
        String contendo os estilos CSS base
    """
    return """
    /* Importação da fonte Open Sauce */
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap');
    
    /* Variáveis de cores */
    :root {
        --primary-color: #caedf8;
        --text-color: #000000;
        --accent-color: #0077b6;
        --background-color: #ffffff;
        --border-color: #e0e0e0;
    }
    
    /* Estilo global */
    .main .block-container {
        padding-top: 2rem;
        background-color: var(--background-color);
    }
    
    /* Fundo da aplicação */
    .stApp {
        background-color: var(--primary-color);
    }
    
    /* Containers */
    .css-18e3th9, .css-1d391kg {
        background-color: var(--background-color);
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin: 1rem;
    }
    
    /* Área de texto */
    .stTextArea textarea {
        border-radius: 5px;
        border: 1px solid var(--border-color);
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
    
    /* Seletores (dropdown) */
    .stSelectbox > div > div {
        background-color: white;
    }
    
    /* Forçar dropdown para descer em vez de subir */
    .stSelectbox div[data-baseweb="popover"] {
        z-index: 999 !important;
        top: 100% !important;
        bottom: auto !important;
    }
    
    /* Estilos para os seletores de idioma */
    .stSelectbox {
        margin-bottom: 1rem;
    }
    """
