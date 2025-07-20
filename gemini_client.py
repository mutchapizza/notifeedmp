import google.generativeai as genai

class GeminiClient:
    def __init__(self):
        genai.configure(api_key="AIzaSyBzyixuHhdYAXsoE1exnykEL1b8vAVtaq0")
        self.model = genai.GenerativeModel('gemini-pro')
        
    def resumir(self, texto):
        """Genera resumen en español latinoamericano"""
        prompt = f"Resume en 2-3 frases: {texto[:2000]}"
        response = self.model.generate_content(prompt)
        return response.text.strip()
    
    def extraer_localizacion(self, texto, municipio):
        """Extrae dirección/colonia con contexto"""
        prompt = f"""
        Extrae cualquier dirección, colonia, calle o punto de referencia mencionado en el texto sobre {municipio}.
        Si no hay localización específica, devuelve "No especificada".
        
        Texto: {texto[:1500]}
        """
        response = self.model.generate_content(prompt)
        return response.text.strip()