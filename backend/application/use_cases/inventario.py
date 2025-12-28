from io import BytesIO
from infrastructure.services.ai_service import AIService
from infrastructure.services.pdf_service import PDFService
from infrastructure.services.blockchain_service import BlockchainService
from infrastructure.services.email_service import EmailService
from infrastructure.django_models.models import ProductoModel

class ProcesarInventarioUseCase:
    @staticmethod
    def ejecutar(email=None, tx_hash=None, send_email=False):
        # 1. Obtener datos de infraestructura
        productos_query = ProductoModel.objects.all()
        
        # 2. IA Service
        ai_analysis = AIService.generate_inventory_analysis(productos_query)
        
        # 3. PDF Service
        buffer = BytesIO()
        PDFService.generate_pdf(buffer, ai_analysis, tx_hash=tx_hash)
        pdf_content = buffer.getvalue()
        buffer.seek(0)
        
        # 4. Email (Opcional)
        if send_email and email:
            EmailService.send_report_email(email, pdf_content, ai_analysis[:200])
            
        return {
            "ai_analysis": ai_analysis,
            "pdf_buffer": buffer,
            "pdf_content": pdf_content
        }

class CertificarInventarioUseCase:
    @staticmethod
    def ejecutar():
        productos_query = ProductoModel.objects.all()
        ai_analysis = AIService.generate_inventory_analysis(productos_query)
        
        content_to_hash = f"{ai_analysis}{productos_query.count()}{[p.codigo for p in productos_query]}"
        cert_result = BlockchainService.certify_data(content_to_hash)
        
        return {
            "ai_analysis": ai_analysis,
            "txHash": cert_result["txHash"],
            "pdf_hash": cert_result["pdf_hash"],
            "status": cert_result["status"]
        }
