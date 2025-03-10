from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT, TA_CENTER

def get_custom_styles():
    """
    Retorna um dicionário com estilos personalizados para o PDF.
    """
    styles = getSampleStyleSheet()
    
    # Melhorar os estilos existentes
    styles['Normal'].fontName = 'Helvetica'
    styles['Normal'].fontSize = 11
    styles['Normal'].leading = 14
    styles['Normal'].alignment = TA_JUSTIFY
    
    styles['Heading1'].fontSize = 24
    styles['Heading1'].leading = 28
    styles['Heading1'].spaceBefore = 24
    styles['Heading1'].spaceAfter = 16
    
    styles['Heading2'].fontSize = 18
    styles['Heading2'].leading = 22
    styles['Heading2'].spaceBefore = 20
    styles['Heading2'].spaceAfter = 14
    
    styles['Heading3'].fontSize = 14
    styles['Heading3'].leading = 18
    styles['Heading3'].spaceBefore = 16
    styles['Heading3'].spaceAfter = 12
    
    # Custom styles
    if 'Justify' not in styles:
        styles.add(ParagraphStyle(
            name='Justify',
            parent=styles['Normal'],
            alignment=TA_JUSTIFY,
            spaceAfter=12
        ))
    
    if 'Footnote' not in styles:
        styles.add(ParagraphStyle(
            name='Footnote',
            fontName='Helvetica',
            fontSize=9,
            leading=11,
            leftIndent=20,
            rightIndent=20,
            firstLineIndent=-20,
            alignment=TA_LEFT,
            spaceBefore=3,
            spaceAfter=3
        ))
    
    if 'Code' not in styles:
        styles.add(ParagraphStyle(
            name='Code',
            fontName='Courier',
            fontSize=10,
            leading=12,
            leftIndent=20,
            rightIndent=20,
            backColor=colors.lightgrey,
            textColor=colors.black,
            spaceBefore=6,
            spaceAfter=6
        ))
    
    if 'Caption' not in styles:
        styles.add(ParagraphStyle(
            name='Caption',
            fontName='Helvetica-Oblique',
            fontSize=10,
            leading=12,
            alignment=TA_CENTER,
            spaceBefore=6,
            spaceAfter=12,
            textColor=colors.darkgrey
        ))
    
    if 'FootnoteReference' not in styles:
        styles.add(ParagraphStyle(
            name='FootnoteReference',
            parent=styles['Normal'],
            fontSize=9,
            superscript=True
        ))
    
    if 'TableCell' not in styles:
        styles.add(ParagraphStyle(
            name='TableCell',
            fontName='Helvetica',
            fontSize=11,
            leading=13,
        ))
    
    if 'TableHeader' not in styles:
        styles.add(ParagraphStyle(
            name='TableHeader',
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=13,
            alignment=TA_CENTER
        ))
    
    return styles 