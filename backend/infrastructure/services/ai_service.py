import google.generativeai as genai
from django.conf import settings
from shared_domain.exceptions import InfrastructureError

class AIService:
    @staticmethod
    def generate_inventory_analysis(productos):
        print("AIService: Starting analysis...")
        if not settings.GOOGLE_API_KEY:
            print("AIService: Warning: GOOGLE_API_KEY is missing.")
            return "Análisis no disponible: API Key faltante."
        
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        print(f"AIService: Processing {len(productos)} products...")
        try:
            inventory_text = "\n".join([
                f"- {p.nombre} ({p.codigo}) de {p.empresa.nombre if p.empresa else 'Empresa Desconocida'}: {p.precios}" 
                for p in productos[:30]
            ])
        except Exception as e:
            print(f"AIService: Error formatting inventory text: {str(e)}")
            raise InfrastructureError(f"Error formateando datos para IA: {str(e)}")
        
        prompt = (
            f"Actúa como un analista de inventarios experto. Analiza la siguiente lista de productos y genera un reporte ejecutivo breve.\n\n"
            f"Datos del inventario:\n{inventory_text}"
        )
            
        try:
            print("AIService: Requesting Gemini content generation...")
            response = model.generate_content(prompt)
            print("AIService: Gemini response received.")
            return response.text
        except Exception as e:
            print(f"AIService: Gemini Error: {str(e)}")
            raise InfrastructureError(f"Error en el servicio de IA: {str(e)}")
