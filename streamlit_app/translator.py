from datetime import datetime
import os
import re

from docx import Document
from docx.shared import Pt, Cm

from openai import OpenAI
from language_utils import NOMES_IDIOMAS

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
    
    Args:
        texto: Texto completo
        i: Índice da linha atual
        linhas: Lista de linhas
        tipo: Tipo de contexto ("anteriores" ou "posteriores")
        
    Returns:
        Texto formatado com as linhas de contexto
    """
    if tipo == "anteriores":
        # Seleciona linhas anteriores (já traduzidas)
        if i == 0:
            return ""
        elif i == 1:
            return f'Aqui estão as linhas imediatamente anteriores a essa, já traduzidas:\n{linhas[0]}'
        elif i == 2:
            return 'Aqui estão as linhas imediatamente anteriores a essa, já traduzidas:\n' + "\n".join(linhas[:2])
        else:
            return 'Aqui estão as linhas imediatamente anteriores a essa, já traduzidas:\n' + "\n".join(linhas[(i-3):i])
    else:
        # Seleciona linhas posteriores (ainda não traduzidas)
        if i >= len(linhas) - 1:
            return ""
        elif i == len(linhas) - 2:
            return f'Aqui estão as linhas imediatamente posteriores a essa, ainda não traduzidas:\n{linhas[i+1]}'
        elif i == len(linhas) - 3:
            return 'Aqui estão as linhas imediatamente posteriores a essa, ainda não traduzidas:\n' + "\n".join(linhas[i+1:i+3])
        else:
            return 'Aqui estão as linhas imediatamente posteriores a essa, ainda não traduzidas:\n' + "\n".join(linhas[i+1:i+4])

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

def traduzir_texto(texto: str, client: OpenAI, idioma_origem="en", idioma_destino="pt", progress_callback=None) -> str:
    """
    Traduz o texto fornecido do idioma de origem para o idioma de destino.
    
    Args:
        texto: Texto para ser traduzido
        client: Cliente OpenAI configurado
        idioma_origem: Código ISO do idioma de origem (padrão: "en" para inglês)
        idioma_destino: Código ISO do idioma de destino (padrão: "pt" para português)
        progress_callback: Função de callback para atualizar o progresso
        
    Returns:
        Texto traduzido no idioma de destino
    """
    linhas = texto.split('\n')
    linhas_traduzidas = []
    total_linhas = len(linhas)
    
    for i, linha in enumerate(linhas):
        if linha.strip() == '':
            linhas_traduzidas.append('')
            if progress_callback:
                progress_callback(i + 1, total_linhas)
            continue
            
        prompt = organiza_prompt(texto, '\n'.join(linhas_traduzidas), i, linhas, idioma_origem, idioma_destino)
        linha_traduzida = pergunta_LLM(client, 'gpt-4o-2024-08-06', prompt, linha.strip())
        linhas_traduzidas.append(linha_traduzida.strip())
        
        if progress_callback:
            progress_callback(i + 1, total_linhas)
        
    return '\n'.join(linhas_traduzidas)
