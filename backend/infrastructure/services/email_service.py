import base64
import requests
from django.conf import settings

class EmailService:
    @staticmethod
    def send_report_email(email, pdf_content, ai_analysis_preview):
        api_key = getattr(settings, 'RESEND_API_KEY', None)
        
        if not api_key or 're_' not in api_key:
             raise ValueError("RESEND_API_KEY inválida.")

        try:
            url = "https://api.resend.com/emails"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            attachment_b64 = base64.b64encode(pdf_content).decode('utf-8')

            payload = {
                "from": "StockPro <onboarding@resend.dev>",
                "to": [email],
                "subject": "Reporte Inteligente de Inventario - StockPro",
                "html": f"<strong>Hola!</strong><br/><br/>Adjuntamos el reporte ejecutivo generado por nuestra IA.<br/><br/><i>Resumen:</i><br/>{ai_analysis_preview}...",
                "attachments": [{"content": attachment_b64, "filename": "inventario_smart.pdf"}]
            }

            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code not in [200, 201]:
                raise Exception(f"Error Resend: {response.json()}")
                
            return response.json()
        except Exception as e:
            raise Exception(f"Error al enviar email: {str(e)}")
