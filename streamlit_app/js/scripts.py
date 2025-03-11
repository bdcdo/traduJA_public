"""
Módulo com scripts JavaScript para a aplicação.
"""

def get_js_scripts():
    """
    Retorna os scripts JavaScript para a aplicação.
    
    Returns:
        String contendo os scripts JavaScript
    """
    return """
    <script>
    // Função para traduzir os textos do uploader
    function traduzirTextos() {
        // Encontrar o elemento de upload
        const uploaders = document.querySelectorAll('.stFileUploader');
        
        uploaders.forEach(uploader => {
            // Encontrar o texto "Drag and drop file here"
            const dragDropTexts = uploader.querySelectorAll('span');
            
            dragDropTexts.forEach(span => {
                if (span.textContent.includes('Drag and drop file here')) {
                    span.textContent = 'Arraste e solte o arquivo aqui';
                }
                
                if (span.textContent.includes('Limit')) {
                    span.textContent = span.textContent.replace('Limit', 'Limite');
                    span.textContent = span.textContent.replace('per file', 'por arquivo');
                }
            });
            
            // Traduzir o botão "Browse files"
            const buttons = uploader.querySelectorAll('button');
            buttons.forEach(button => {
                if (button.textContent.includes('Browse files')) {
                    button.textContent = 'Procurar arquivos';
                }
            });
        });
    }
    
    // Função para fazer o botão personalizado de tradução funcionar
    function configurarBotaoTraduzir() {
        const botaoTraduzir = document.getElementById('traduzir-btn');
        const botaoReal = document.querySelector('[data-testid="baseButton-secondary"]');
        
        if (botaoTraduzir && botaoReal) {
            botaoTraduzir.addEventListener('click', function() {
                botaoReal.click();
            });
        }
    }
    
    // Executar as funções quando o DOM estiver carregado
    document.addEventListener('DOMContentLoaded', function() {
        traduzirTextos();
        configurarBotaoTraduzir();
    });
    
    // Executar as funções periodicamente para garantir que funcionem
    // mesmo após recarregar componentes
    setInterval(function() {
        traduzirTextos();
        configurarBotaoTraduzir();
    }, 1000);
    </script>
    """
