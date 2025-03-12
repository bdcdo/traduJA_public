from datetime import datetime
import os
import re
import tiktoken  # Add this import for token counting

from docx import Document
from docx.shared import Pt, Cm

from openai import OpenAI
from language_utils import NOMES_IDIOMAS

# Add token pricing constants
TOKEN_PRICE_INPUT = 2.50 / 1_000_000  # $2.50 per million tokens
TOKEN_PRICE_OUTPUT = 10.00 / 1_000_000  # $10.00 per million tokens

def count_tokens(text, model="gpt-4o-2024-08-06"):
    """
    Conta o número de tokens em um texto para um modelo específico.
    
    Args:
        text: Texto para contar tokens
        model: Modelo para o qual contar tokens
        
    Returns:
        Número de tokens no texto
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception:
        # Fallback to approximation if tiktoken fails or model not found
        return len(text.split()) * 1.3  # Rough approximation

def pergunta_LLM(client, current_model, prompt, question):
    return client.chat.completions.create(
          model=current_model,
          messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
          ],
          temperature=0.6
        ).choices[0].message.content

def seleciona_contexto(texto, i, linhas, tipo="anteriores"):
    """
    Seleciona linhas de contexto (anteriores ou posteriores) para auxiliar na tradução.
    """
    def get_non_empty_lines(start, end, lines):
        return [l for l in lines[start:end] if l.strip()]

    if tipo == "anteriores":
        # Seleciona linhas anteriores (já traduzidas)
        if i == 0:
            return ""
        else:
            # Pegar até 3 linhas não vazias anteriores
            context_lines = []
            count = 0
            pos = i - 1
            while pos >= 0 and count < 3:
                if linhas[pos].strip():
                    context_lines.insert(0, linhas[pos])
                    count += 1
                pos -= 1
            
            if not context_lines:
                return ""
            return 'Aqui estão as linhas imediatamente anteriores a essa, já traduzidas:\n' + "\n".join(context_lines)
    else:
        # Seleciona linhas posteriores (ainda não traduzidas)
        if i >= len(linhas) - 1:
            return ""
        else:
            # Pegar até 3 linhas não vazias posteriores
            context_lines = []
            count = 0
            pos = i + 1
            while pos < len(linhas) and count < 3:
                if linhas[pos].strip():
                    context_lines.append(linhas[pos])
                    count += 1
                pos += 1
            
            if not context_lines:
                return ""
            return 'Aqui estão as linhas imediatamente posteriores a essa, ainda não traduzidas:\n' + "\n".join(context_lines)

def organiza_prompt(texto, texto_traduzido, i, linhas, idioma_origem="en", idioma_destino="pt"):
    paragrafos_anteriores = seleciona_contexto(texto_traduzido, i, linhas, "anteriores")
    paragrafos_posteriores = seleciona_contexto(texto, i, linhas, "posteriores")
    
    origem_nome = NOMES_IDIOMAS.get(idioma_origem, idioma_origem)
    destino_nome = NOMES_IDIOMAS.get(idioma_destino, idioma_destino)

    prompt = f"""Você é um tradutor senior especializado na tradução de {origem_nome} para {destino_nome}.
            Irei te fornecer um trecho de um texto escrito em {origem_nome} e quero que você o traduza para {destino_nome}.
            O trecho pode ser qualquer parte do texto - como parágrafos, títulos, subtítulos ou descrições de tabelas.

            Para garantir consistência e precisão na tradução:
            1. Use o contexto das linhas anteriores (já traduzidas) e posteriores (ainda não traduzidas) fornecidas
            2. Mantenha o mesmo tom, estilo e terminologia do texto original e das partes já traduzidas
            3. Preserve formatações especiais, como marcadores, numerações ou ênfases
            4. Traduza apenas a linha indicada, nada mais

            Responda apenas com a tradução da linha indicada, sem explicações ou comentários adicionais.
            Se encontrar termos técnicos ou específicos que não devem ser traduzidos, mantenha-os no idioma original.

            {paragrafos_anteriores}
            {paragrafos_posteriores}
            Aqui está o trecho que deve ser traduzido:\n"""
    
    return prompt

def traduzir_texto(texto: str, client: OpenAI, idioma_origem="en", idioma_destino="pt", progress_callback=None, token_callback=None) -> str:
    """
    Traduz o texto fornecido do idioma de origem para o idioma de destino.
    
    Args:
        texto: Texto para ser traduzido
        client: Cliente OpenAI configurado
        idioma_origem: Código ISO do idioma de origem (padrão: "en" para inglês)
        idioma_destino: Código ISO do idioma de destino (padrão: "pt" para português)
        progress_callback: Função de callback para atualizar o progresso
        token_callback: Função de callback para atualizar informações de tokens e custos
        
    Returns:
        Texto traduzido no idioma de destino
    """
    linhas = texto.split('\n')
    linhas_traduzidas = []
    total_linhas = len(linhas)
    
    # Inicializar contadores de tokens
    total_input_tokens = 0
    total_output_tokens = 0
    model = 'gpt-4o-2024-08-06'
    
    for i, linha in enumerate(linhas):
        if linha.strip() == '':
            linhas_traduzidas.append('')
            if progress_callback:
                progress_callback(i + 1, total_linhas)
            continue
            
        prompt = organiza_prompt(texto, '\n'.join(linhas_traduzidas), i, linhas, idioma_origem, idioma_destino)
        
        # Contar tokens de entrada (prompt do sistema + linha a ser traduzida)
        input_tokens = count_tokens(prompt, model) + count_tokens(linha.strip(), model)
        total_input_tokens += input_tokens
        
        # Traduzir a linha
        linha_traduzida = pergunta_LLM(client, model, prompt, linha.strip())
        
        # Contar tokens de saída (resposta do modelo)
        output_tokens = count_tokens(linha_traduzida.strip(), model)
        total_output_tokens += output_tokens
        
        linhas_traduzidas.append(linha_traduzida.strip())
        
        # Calcular custos
        input_cost = total_input_tokens * TOKEN_PRICE_INPUT
        output_cost = total_output_tokens * TOKEN_PRICE_OUTPUT
        total_cost = input_cost + output_cost
        
        # Atualizar progresso e informações de tokens
        if progress_callback:
            progress_callback(i + 1, total_linhas)
        
        if token_callback:
            token_callback(total_input_tokens, total_output_tokens, input_cost, output_cost, total_cost)
        
    return '\n'.join(linhas_traduzidas)
