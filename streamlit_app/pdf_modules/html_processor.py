import re
import base64
from io import BytesIO
from PIL import Image as PILImage
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
from reportlab.lib import colors
import logging

logger = logging.getLogger(__name__)

class HTMLProcessor:
    def __init__(self, styles, doc_width, doc_height):
        self.styles = styles
        self.doc_width = doc_width
        self.doc_height = doc_height
        self.flowables = []
        self.footnotes = []

    def process_element(self, element):
        """Processa um elemento HTML e adiciona os flowables correspondentes."""
        if element.name is None:  # Skip text nodes at the root level
            return

        processors = {
            'h1': self._process_heading,
            'h2': self._process_heading,
            'h3': self._process_heading,
            'h4': self._process_heading,
            'h5': self._process_heading,
            'h6': self._process_heading,
            'p': self._process_paragraph,
            'pre': self._process_code_block,
            'img': self._process_image,
            'table': self._process_table,
            'hr': self._process_hr,
            'ul': self._process_list,
            'ol': self._process_list,
            'div': self._process_footnote
        }

        processor = processors.get(element.name)
        if processor:
            processor(element)

    def _process_heading(self, element):
        heading_level = int(element.name[1])
        heading_text = element.get_text().strip()
        style_name = f'Heading{min(heading_level, 3)}'
        self.flowables.append(Paragraph(heading_text, self.styles[style_name]))
        self.flowables.append(Spacer(1, 12))

    def _process_paragraph(self, element):
        para_text = str(element)
        
        # Primeiro, vamos limpar todas as tags br
        para_text = re.sub(r'<br[^>]*>.*?</br>', ' ', para_text)
        para_text = re.sub(r'<br[^>]*/?>', ' ', para_text)
        para_text = re.sub(r'</br>', ' ', para_text)
        
        # Processar elementos inline básicos
        para_text = re.sub(r'<strong>(.*?)</strong>', r'<b>\1</b>', para_text)
        para_text = re.sub(r'<em>(.*?)</em>', r'<i>\1</i>', para_text)
        para_text = re.sub(r'<code>(.*?)</code>', r'<font name="Courier">\1</font>', para_text)
        
        # Tratar superscript simplesmente removendo as tags e mantendo o número
        para_text = re.sub(r'<sup[^>]*>(\d+)</sup>', r'\1', para_text)
        para_text = re.sub(r'<super>(\d+)</super>', r'\1', para_text)
        para_text = re.sub(r'<super></super>', '', para_text)
        
        # Limpar tags HTML desnecessárias
        para_text = re.sub(r'</?p[^>]*>', '', para_text)
        para_text = re.sub(r'<a[^>]*>(.*?)</a>', r'\1', para_text)
        para_text = re.sub(r'class="[^"]*"', '', para_text)
        para_text = re.sub(r'<para[^>]*>', '', para_text)
        para_text = re.sub(r'</para>', '', para_text)
        
        # Processar símbolos especiais
        para_text = re.sub(r'\$\\dagger\$', '†', para_text)
        para_text = re.sub(r'\$\\dagger \\dagger\$', '‡', para_text)
        para_text = re.sub(r'\\&amp;', '&', para_text)
        para_text = re.sub(r'&amp;', '&', para_text)
        
        # Limpar espaços extras e quebras de linha
        para_text = re.sub(r'\s+', ' ', para_text)
        para_text = para_text.strip()
        
        try:
            # Tentar criar o parágrafo com o texto processado
            para = Paragraph(para_text, self.styles['Justify'])
            self.flowables.append(para)
            self.flowables.append(Spacer(1, 8))
        except Exception as e:
            logger.error(f"Erro ao processar parágrafo: {str(e)}\nTexto problemático: {para_text}")
            # Se falhar, remover todas as tags HTML e tentar novamente
            clean_text = re.sub(r'<[^>]*>', '', para_text)
            clean_text = clean_text.replace('\\', '')
            clean_text = re.sub(r'\s+', ' ', clean_text)
            clean_text = clean_text.strip()
            self.flowables.append(Paragraph(clean_text, self.styles['Justify']))
            self.flowables.append(Spacer(1, 8))

    def _process_code_block(self, element):
        code_element = element.find('code')
        if code_element:
            code_text = code_element.get_text()
            try:
                code_para = Paragraph(code_text, self.styles['Code'])
                self.flowables.append(code_para)
                self.flowables.append(Spacer(1, 12))
            except Exception as e:
                logger.error(f"Erro ao processar bloco de código: {str(e)}")

    def _process_image(self, element):
        try:
            src = element.get('src', '')
            if src.startswith('data:image'):
                img_data = src.split(',')[1]
                img_bytes = base64.b64decode(img_data)
                img = PILImage.open(BytesIO(img_bytes))
                
                max_width = self.doc_width * 0.8
                max_height = self.doc_height * 0.5
                
                width, height = img.size
                aspect = width / height
                
                if width > max_width:
                    width = max_width
                    height = width / aspect
                
                if height > max_height:
                    height = max_height
                    width = height * aspect
                
                img_flowable = Image(BytesIO(img_bytes), width=width, height=height)
                self.flowables.append(img_flowable)
                self.flowables.append(Spacer(1, 12))
                
                alt_text = element.get('alt', '').strip()
                if alt_text:
                    caption = Paragraph(f"<i>{alt_text}</i>", self.styles['Caption'])
                    self.flowables.append(caption)
                    self.flowables.append(Spacer(1, 12))
        except Exception as e:
            logger.error(f"Erro ao processar imagem: {str(e)}")

    def _process_table(self, element):
        try:
            table_data = []
            rows = element.find_all('tr')
            
            for row in rows:
                headers = row.find_all('th')
                if headers:
                    header_row = []
                    for header in headers:
                        header_text = header.get_text().strip()
                        header_row.append(Paragraph(header_text, self.styles['TableHeader']))
                    table_data.append(header_row)
                else:
                    cells = row.find_all('td')
                    data_row = []
                    for cell in cells:
                        cell_text = cell.get_text().strip()
                        data_row.append(Paragraph(cell_text, self.styles['TableCell']))
                    table_data.append(data_row)
            
            if table_data:
                col_count = max(len(row) for row in table_data)
                col_width = [self.doc_width / col_count] * col_count
                table = Table(table_data, colWidths=col_width)
                
                table_style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                ])
                table.setStyle(table_style)
                
                self.flowables.append(table)
                self.flowables.append(Spacer(1, 15))
        except Exception as e:
            logger.error(f"Erro ao processar tabela: {str(e)}")

    def _process_hr(self, element):
        self.flowables.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
        self.flowables.append(Spacer(1, 12))

    def _process_list(self, element):
        list_items = element.find_all('li', recursive=False)
        for i, item in enumerate(list_items):
            prefix = "• " if element.name == 'ul' else f"{i+1}. "
            item_text = prefix + item.get_text().strip()
            
            try:
                list_para = Paragraph(item_text, self.styles['Justify'])
                self.flowables.append(list_para)
                self.flowables.append(Spacer(1, 6))
            except Exception as e:
                self.flowables.append(Paragraph(item_text, self.styles['Justify']))
                self.flowables.append(Spacer(1, 6))
        
        self.flowables.append(Spacer(1, 6))

    def _process_footnote(self, element):
        if element.get('class') and 'footnote' in element.get('class'):
            fn_id = element.find('sup').get('id').replace('fnref:', '')
            sup = element.find('sup')
            if sup:
                sup.decompose()
            fn_content = element.get_text().strip()
            fn_number = int(re.search(r'\d+', fn_id).group())
            self.footnotes.append((fn_number, fn_content))

    def add_footnotes(self):
        """Adiciona as notas de rodapé ao final do documento."""
        if self.footnotes:
            self.flowables.append(Spacer(1, 24))
            self.flowables.append(HRFlowable(width="25%", thickness=0.5, color=colors.grey))
            self.flowables.append(Spacer(1, 12))
            
            notas_titulo = Paragraph("Notas", self.styles['Heading3'])
            self.flowables.append(notas_titulo)
            self.flowables.append(Spacer(1, 8))
            
            for fn_number, fn_content in sorted(self.footnotes, key=lambda x: x[0]):
                fn_text = f"<b>{fn_number}.</b> {fn_content}"
                fn_para = Paragraph(fn_text, self.styles['Footnote'])
                self.flowables.append(fn_para)

    def get_flowables(self):
        """Retorna a lista de flowables processados."""
        return self.flowables 