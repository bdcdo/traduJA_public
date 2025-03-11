from datetime import datetime
import os
import re

from docx import Document
from docx.shared import Pt, Cm

from openai import OpenAI

def pergunta_LLM(client, current_model, prompt, question):
    return client.chat.completions.create(
          model=current_model,
          messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
          ],
          temperature=0
        ).choices[0].message.content

def seleciona_anteriores(texto, i, linhas):
    if i == 0:
        texto_anterior = ""
    elif i == 1:
        texto_anterior = f'Aqui estão as linhas imediatamente anteriores a essa, já traduzidas:\n{linhas[0]}'
    elif i == 2:
        texto_anterior = 'Aqui estão as linhas imediatamente anteriores a essa, já traduzidas:\n' + "\n".join(linhas[:2])
    else:
        texto_anterior = 'Aqui estão as linhas imediatamente anteriores a essa, já traduzidas:\n' + "\n".join(linhas[(i-3):i])

    return texto_anterior

def seleciona_posteriores(texto, i, linhas):
    if i >= len(linhas) - 1:
        texto_posterior = ""
    elif i == len(linhas) - 2:
        texto_posterior = f'Aqui estão as linhas imediatamente posteriores a essa, ainda não traduzidas:\n{linhas[i+1]}'
    elif i == len(linhas) - 3:
        texto_posterior = 'Aqui estão as linhas imediatamente posteriores a essa, ainda não traduzidas:\n' + "\n".join(linhas[i+1:i+3])
    else:
        texto_posterior = 'Aqui estão as linhas imediatamente posteriores a essa, ainda não traduzidas:\n' + "\n".join(linhas[i+1:i+4])

    return texto_posterior

# Mapeamento de códigos de idioma para nomes completos
NOMES_IDIOMAS = {
    "en": "inglês",
    "pt": "português",
    "es": "espanhol",
    "fr": "francês",
    "de": "alemão",
    "it": "italiano"
}

def organiza_prompt(texto, texto_traduzido, i, linhas, idioma_origem="en", idioma_destino="pt"):
    paragrafos_anteriores = seleciona_anteriores(texto_traduzido, i, linhas)
    paragrafos_posteriores = seleciona_posteriores(texto, i, linhas)
    
    origem_nome = NOMES_IDIOMAS.get(idioma_origem, idioma_origem)
    destino_nome = NOMES_IDIOMAS.get(idioma_destino, idioma_destino)

    prompt = f"""Você é um tradutor especializado em traduzir textos.
            Irei te fornecer um trecho de um texto escrito em {origem_nome} e quero que você o traduza para {destino_nome}.
            O trecho pode ser qualquer parte do texto - além de parágrafos, pode também ser um título, um subtítulo ou a descrição de uma tabela.

            Para que você possa traduzir melhor, sempre que possível, irei te fornecer algumas linhas já traduzidas, que vem imediatamente antes da linha que você deve traduzir no texto.
            Além disso, sempre irei te fornecer algumas linhas que vem imediatamente depois da linha que você deve traduzir.
            Utilize o contexto apresentado por essas linhas anteriores e posteriores para traduzir melhor. No entanto, traduza apenas a linha indicada como sendo a que você deve traduzir.

            Me responda direto ao ponto, respondendo única e exclusivamente com a tradução da linha indicada.

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
        linha_traduzida = pergunta_LLM(client, 'gpt-4o-mini-2024-07-18', prompt, linha.strip())
        linhas_traduzidas.append(linha_traduzida.strip())
        
        if progress_callback:
            progress_callback(i + 1, total_linhas)
        
    return '\n'.join(linhas_traduzidas)
