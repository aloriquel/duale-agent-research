import requests
import json
from config import GEMINI_API_KEY, REPORT_LANGUAGE

class ReportGenerator:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        # Use v1beta and gemini-2.5-flash (confirmed available via browser)
        self.model_name = "models/gemini-2.5-flash"
        self.url = f"https://generativelanguage.googleapis.com/v1beta/{self.model_name}:generateContent?key={self.api_key}"
        print(f"Using Gemini URL: {self.url.split('?')[0]}?key=HIDDEN")

    def generate_report(self, search_results):
        """Synthesize search results into a 1-page structured report using REST API."""
        if not self.api_key or self.api_key == "YOUR_GEMINI_API_KEY_HERE":
            return self._generate_fallback_report(search_results)

        prompt = f"""
        Actúa como un analista de mercado experto para la startup 'Duale' (www.duale.es).
        Duale es un copilot de IA para FP Dual que ayuda a la inclusión de alumnos con NEE (Necesidades Educativas Especiales).
        
        A partir de los siguientes resultados de búsqueda REALES de esta semana (que incluyen el contenido extraído de las webs), redacta un informe de 1 página bien organizado en HTML.
        
        Resultados de búsqueda (Contenido extraído):
        {search_results}
        
        El informe debe ser EXTREMADAMENTE ESPECÍFICO. No acepto generalidades.
        Si mencionas un competidor, di qué está haciendo. Si mencionas una ayuda, di el nombre, plazo y cuantía si aparece.
        Si mencionas una noticia, di la fecha y el medio.
        
        Estructura:
        1. COMPETIDORES (Nuevos o movimientos detectados).
        2. TENDENCIAS Y NOTICIAS RECIENTES (FP, IA en inclusión).
        3. AYUDAS Y FINANCIACIÓN (Convocatorias abiertas, BOE, diarios oficiales, NextGen).
        4. PROYECTOS PÚBLICOS Y LICITACIONES (Ministerio, Consejerías).
        5. OPORTUNIDADES CLAVE PARA DUALE.
        
        Instrucciones CRUDAS:
        - No uses frases como "Se recomienda vigilancia". Di "Se ha publicado X en la web Y".
        - Incluye siempre los enlaces <a href='...'> originales de donde sale la información.
        - Idioma: {REPORT_LANGUAGE}.
        - Formato: HTML puro para email.
        """
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.2
            }
        }
        
        try:
            print("Generating report via Gemini REST API...")
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            # Extract text from response
            if "candidates" in data and len(data["candidates"]) > 0:
                report_html = data["candidates"][0]["content"]["parts"][0]["text"]
                # Clean up if Gemini wrapped it in markdown
                report_html = report_html.replace("```html", "").replace("```", "").strip()
                return report_html
            else:
                print("No candidates found in Gemini response.")
                return self._generate_fallback_report(search_results)
                
        except Exception as e:
            print(f"Error generating report with Gemini REST API: {e}")
            return self._generate_fallback_report(search_results)

    def generate_linkedin_post(self, search_results):
        """Generate a LinkedIn newsletter post from the search results."""
        if not self.api_key or self.api_key == "YOUR_GEMINI_API_KEY_HERE":
            return "No se pudo generar el post de LinkedIn porque la API de Gemini no está configurada."

        prompt = f"""
        Actúa como el Community Manager de 'Duale' (www.duale.es), una startup EdTech que crea un copilot de IA para la inclusión en FP Dual.
        
        A partir de los siguientes resultados de búsqueda de esta semana, redacta un POST DE LINKEDIN brillante, estilo "Newsletter Semanal" que resuma la actualidad del sector para un público profesional y corporativo (centros de FP, tutores de empresa, inversores).
        
        Resultados de búsqueda:
        {search_results}
        
        Instrucciones para el POST:
        - Tono: Profesional, motivador y orientado a la inclusión (\u267f) y la tecnología (\ud83d\ude80).
        - Estructura: 
          1. Un "gancho" inicial (titular).
          2. Tres puntos clave (bullets) con los descubrimientos más importantes de la semana (ayudas, noticias o competidores).
          3. Una reflexión final sobre cómo Duale forma parte del futuro de la FP Dual.
          4. Llamada a la acción (CTA) animando a comentar o visitar duale.es.
        - Longitud: Un formato ideal para leer en móvil, saltos de línea frecuentes.
        - Hashtags: Incluye de 3 a 5 hashtags relevantes (ej. #FPDual #EdTech #DesarrolloInclusivo).
        - Idioma: Español.
        """
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.2
            }
        }
        
        try:
            print("Generating LinkedIn post via Gemini REST API...")
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            if "candidates" in data and len(data["candidates"]) > 0:
                post_text = data["candidates"][0]["content"]["parts"][0]["text"]
                return post_text.strip()
            else:
                return "Error: No se encontró contenido en la respuesta de Gemini."
        except Exception as e:
            print(f"Error generating LinkedIn post: {e}")
            return f"Error: {e}"

    def _generate_fallback_report(self, search_results):
        """Simple fallback if Gemini is not available."""
        html = "<h1>Informe Semanal de Mercado - Duale</h1>"
        html += "<p>Nota: Este es un informe simplificado (Error en Gemini API o clave no configurada).</p>"
        for query, urls in search_results.items():
            html += f"<h3>{query}</h3><ul>"
            for url in urls:
                html += f"<li><a href='{url}'>{url}</a></li>"
            html += "</ul>"
        return html
