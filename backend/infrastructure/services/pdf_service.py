from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
from management.models import Producto

class PDFService:
    @staticmethod
    def generate_pdf(buffer, ai_analysis, tx_hash=None):
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2e1065'),
            spaceAfter=30,
            alignment=1 # Center
        )
        story.append(Paragraph("StockPro - Reporte de Inventario Inteligente", title_style))
        story.append(Spacer(1, 12))

        # AI Analysis Section
        story.append(Paragraph("Análisis Ejecutivo (IA)", styles['Heading2']))
        normal_style = styles['Normal']
        normal_style.fontSize = 11
        normal_style.leading = 14
        story.append(Paragraph(ai_analysis.replace('\n', '<br/>'), normal_style))
        story.append(Spacer(1, 20))

        # Table Header
        story.append(Paragraph("Detalle de Productos", styles['Heading2']))
        
        data = [['Código', 'Producto', 'Empresa', 'Precio USD', 'Precio COP']]
        for p in Producto.objects.all():
            data.append([
                p.codigo,
                p.nombre[:25] + ('...' if len(p.nombre) > 25 else ''),
                p.empresa.nombre[:20],
                f"${p.precios.get('USD', 0)}",
                f"${p.precios.get('COP', 0)}"
            ])

        table = Table(data, colWidths=[60, 180, 120, 80, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#5b21b6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f3ff')),
            ('GRID', (0, 0), (-1, -1), 1, colors.white),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f3ff')])
        ]))
        story.append(table)
        
        if tx_hash:
            story.append(Spacer(1, 30))
            story.append(Paragraph("Certificación de Integridad Blockchain (Solana)", styles['Heading2']))
            
            blockchain_style = ParagraphStyle(
                'BlockchainStyle',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#4b5563')
            )
            
            story.append(Paragraph(f"<b>ID Transacción:</b> {tx_hash}", blockchain_style))
            story.append(Paragraph(f"<b>Fecha de Verificación:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", blockchain_style))
            story.append(Paragraph("<b>Red:</b> Solana Devnet", blockchain_style))
            story.append(Paragraph("<b>Concepto:</b> Este documento ha sido sellado criptográficamente en la red de Solana, garantizando que el estado del inventario no ha sido modificado desde la fecha de emisión.", blockchain_style))

        doc.build(story)
