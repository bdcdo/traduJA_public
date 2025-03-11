# TraduJA

TraduJA é uma aplicação para conversão de documentos PDF para texto formatado em Markdown e geração de PDF formatado, com futuras funcionalidades de tradução.

## Funcionalidades atuais

- Upload de arquivos PDF
- Conversão de PDF para texto formatado em Markdown usando Mistral AI OCR
- Visualização do resultado na interface
- Download do arquivo Markdown resultante
- Geração de PDF formatado a partir do markdown extraído
- Suporte para notas de rodapé e formatação avançada
- Prévia do PDF gerado diretamente na interface
- Interface amigável com design responsivo

## Instalação

1. Clone este repositório
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:

   - Copie o arquivo `.env.example` para `.env`:
   ```bash
   cp .env.example .env
   ```
   
   - Edite o arquivo `.env` e adicione suas chaves de API:
   ```
   OPENAI_API_KEY=sua_chave_openai_aqui
   MISTRAL_API_KEY=sua_chave_mistral_aqui
   ```

## Executando a aplicação

Para iniciar a aplicação Streamlit:

```bash
cd traduJA/streamlit_app
streamlit run app.py
```

A aplicação estará disponível no navegador, geralmente em http://localhost:8501

## Configuração no Streamlit Cloud

Para configurar as variáveis de ambiente no Streamlit Cloud:

1. Acesse o painel de controle do seu aplicativo no Streamlit Cloud
2. Vá para a seção "Secrets"
3. Adicione as seguintes variáveis:
   ```
   OPENAI_API_KEY = "sua_chave_openai_aqui"
   MISTRAL_API_KEY = "sua_chave_mistral_aqui"
   ```
4. Salve as alterações e reinicie o aplicativo

## Compatibilidade

Esta versão foi projetada para funcionar em diferentes sistemas operacionais, incluindo Windows, sem dependências externas complexas.

## Próximos passos

- Implementação de funcionalidades de tradução
- Melhorar a formatação do arquivo
- Desenvolvimento de uma versão com Django (backend) e React (frontend)
- Melhorias na interface e na experiência do usuário
