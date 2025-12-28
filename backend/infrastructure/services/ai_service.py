import google.generativeai as genai
from django.conf import settings

class AIService:
    @staticmethod
    def generate_inventory_analysis(productos):
        api_key = getattr(settings, 'GOOGLE_API_KEY', None)
        if not api_key or "REEMPLAZAR" in api_key:
            return "Resumen de Inventario:\nInventario generado automáticamente sin análisis de IA (API Key no configurada)."
        
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash-lite')
            
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
