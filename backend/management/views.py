from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
import requests
import base64
import hashlib
from django.conf import settings
import traceback
import google.generativeai as genai
from datetime import datetime
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.instruction import Instruction as SInstruction
from solders.message import Message
from solders.transaction import Transaction
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Empresa, Producto
from .serializers import EmpresaSerializer, ProductoSerializer, MyTokenObtainPairSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_administrator

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAdminOrReadOnly]

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), permissions.BasePermission()]

    def generate_ai_content(self, productos):
        api_key = getattr(settings, 'GOOGLE_API_KEY', None)
        if not api_key or "REEMPLAZAR" in api_key:
            return "Resumen de Inventario:\nInventario generado automáticamente sin análisis de IA (API Key no configurada)."
        
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash-lite')
            
            inventory_text = "\n".join([
                f"- {p.nombre} ({p.codigo}) de {p.empresa.nombre}: {p.precios}" 
                for p in productos[:30] # Limit to 30 for token limits
            ])
            
            prompt = (
                f"Actúa como un analista de inventarios experto. Analiza la siguiente lista de productos y genera un reporte ejecutivo breve (máximo 3 párrafos).\n"
                f"Destaca la diversidad de productos, marcas principales y rango de precios. Usa un tono profesional.\n\n"
                f"Datos del inventario (muestra):\n{inventory_text}"
            )
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"No se pudo generar el análisis de IA: {str(e)}"

    def create_pdf(self, buffer, ai_analysis, tx_hash=None):
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

    @action(detail=False, methods=['get'])
    def generate_inventory_pdf(self, request):
        buffer = BytesIO()
        tx_hash = request.query_params.get('tx_hash')
        productos = Producto.objects.all()
        ai_analysis = self.generate_ai_content(productos)
        
        self.create_pdf(buffer, ai_analysis, tx_hash=tx_hash)
        
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

    @action(detail=False, methods=['post'])
    def send_inventory_pdf(self, request):
        email = request.data.get('email')
        tx_hash = request.data.get('tx_hash')
        
        # Generar PDF en memoria con IA
        buffer = BytesIO()
        productos = Producto.objects.all()
        ai_analysis = self.generate_ai_content(productos)
        self.create_pdf(buffer, ai_analysis, tx_hash=tx_hash)
        pdf_content = buffer.getvalue()
        buffer.close()

        # Enviar usando Resend API
        api_key = getattr(settings, 'RESEND_API_KEY', None)
        
        if not api_key or 're_' not in api_key:
             return Response({"error": "RESEND_API_KEY inválida."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            url = "https://api.resend.com/emails"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            attachment_b64 = base64.b64encode(pdf_content).decode('utf-8')

            payload = {
                "from": "StockPro <onboarding@resend.dev>",
                "to": [email],
                "subject": "Reporte Inteligente de Inventario - StockPro",
                "html": f"<strong>Hola!</strong><br/><br/>Adjuntamos el reporte ejecutivo generado por nuestra IA.<br/><br/><i>Resumen:</i><br/>{ai_analysis[:200]}...",
                "attachments": [{"content": attachment_b64, "filename": "inventario_smart.pdf"}]
            }

            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code in [200, 201]:
                return Response({"message": f"Reporte enviado a {email}"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Error al enviar email", "details": response.json()}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def certify_inventory(self, request):
        # 1. Análisis IA
        productos = Producto.objects.all()
        ai_analysis = self.generate_ai_content(productos)

        # 2. Generar Hash del contenido esencial
        content_to_hash = f"{ai_analysis}{productos.count()}{[p.codigo for p in productos]}"
        pdf_hash = hashlib.sha256(content_to_hash.encode()).hexdigest()
        
        # 3. Solana Blockchain
        rpc_url = getattr(settings, 'SOLANA_RPC_URL', "https://api.devnet.solana.com")
        private_key_hex = getattr(settings, 'SOLANA_PRIVATE_KEY', None)

        if not private_key_hex or "REEMPLAZAR" in private_key_hex:
             return Response({
                "message": "Solana no configurado, simulación exitosa.",
                "ai_analysis": ai_analysis,
                "pdf_hash": pdf_hash,
                "txHash": "SIMULATED_TX_HASH",
                "status": "SIMULATED"
            }, status=status.HTTP_200_OK)

        try:
            client = Client(rpc_url)
            seed = bytes.fromhex(private_key_hex)
            keypair = Keypair.from_seed(seed)
            
            memo_program_id = Pubkey.from_string("MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr")
            memo_instruction = SInstruction(memo_program_id, pdf_hash.encode('utf-8'), [])
            
            blockhash = client.get_latest_blockhash().value.blockhash
            message = Message.new_with_blockhash([memo_instruction], keypair.pubkey(), blockhash)
            txn = Transaction([keypair], message, blockhash)
            
            response = client.send_transaction(txn)
            tx_hash = str(response.value)
            
            return Response({
                "message": "Certificado en Solana exitosamente",
                "ai_analysis": ai_analysis,
                "txHash": tx_hash,
                "status": "SUCCESS"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response({"error": f"Error Solana: {str(e)}", "ai_analysis": ai_analysis}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
