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

def organiza_prompt(texto, texto_traduzido, i, linhas):
    paragrafos_anteriores = seleciona_anteriores(texto_traduzido, i, linhas)
    paragrafos_posteriores = seleciona_posteriores(texto, i, linhas)

    prompt = f"""Você é um tradutor especializado em traduzir textos sobre pesquisa empírica em direito.
            Irei te fornecer um trecho de um artigo acadêmico escrito em inglês e quero que você o traduza para o português.
            O trecho pode ser qualquer parte do do texto - além de parágrafos, pode também ser um título, um subtítulo ou a descrição de uma tabela.

            Para que você possa traduzir melhor, sempre que possível, irei te fornecer algumas linhas já traduzidas, que vem imediatamente antes da linha que você deve traduzir no texto.
            Além disso, sempre irei te fornecer algumas linhas que vem imediatamente depois da linha que você deve traduzir.
            Utilize o contexto apresentado por essas linhas anteriores e posteriores para traduzir melhor. No entanto, traduza apenas a linha indicada como sendo a que você deve traduzir.

            Me responda direto ao ponto, respondendo única e exclusivamente com a tradução da linha indicada.

            {paragrafos_anteriores}
            {paragrafos_posteriores}
            Aqui está o trecho que deve ser traduzido:\n"""
    
    return prompt

def traduzir_texto(texto: str, client: OpenAI, progress_callback=None) -> str:
    """
    Traduz o texto fornecido do inglês para o português.
    
    Args:
        texto: Texto em inglês para ser traduzido
        client: Cliente OpenAI configurado
        progress_callback: Função de callback para atualizar o progresso
        
    Returns:
        Texto traduzido em português
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
            
        prompt = organiza_prompt(texto, '\n'.join(linhas_traduzidas), i, linhas)
        linha_traduzida = pergunta_LLM(client, 'gpt-4o-mini-2024-07-18', prompt, linha.strip())
        linhas_traduzidas.append(linha_traduzida.strip())
        
        if progress_callback:
            progress_callback(i + 1, total_linhas)
        
    return '\n'.join(linhas_traduzidas)

def main():
    for i in range(len(doc.paragraphs)):
        para_atual = doc.paragraphs[i]

        prompt = organiza_prompt(doc, doc2, i)        

        if para_atual.text != '':
            para_traduzido = pergunta_LLM(openAI_client, 'gpt-4', prompt, para_atual.text.strip())
            para_traduzido = para_traduzido.strip()
        else:
            continue
        print(para_traduzido)

        novo_para = doc2.add_paragraph()

        if para_atual.runs:
            novo_run = novo_para.add_run(para_traduzido)
            novo_run.font.name = font_name
            novo_run.font.size = font_size
        else:
            novo_para.add_run(para_traduzido)

        print(f'{i}/{len(doc.paragraphs)}')
        #sleep(2)

    doc2.save(f'GPT-4o-mini-{datetime.now().strftime("%Y%m%d%H%M%S")}.docx')

if __name__ == '__main__':
    openAI_client = OpenAI()
    #groqClient = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    #anthropic_client = anthropic.Anthropic()
    
    font_name = "Times New Roman"
    font_size = Pt(12)
    first_line_indent = Cm(1.25)

    script_dir = os.path.dirname(__file__)
    docx_dir = os.path.join(script_dir, 'docx/fulltext_revisado.docx')
    
    doc = Document(docx_dir)
    doc2 = Document()

    main()