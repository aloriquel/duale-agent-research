import anthropic
from config import ANTHROPIC_API_KEY, REPORT_LANGUAGE

MODEL = "claude-haiku-4-5-20251001"

# === COMPANY CONTEXT ===
# Duale (www.duale.es) is an AI copilot specialized in Inclusive FP Dual (Spanish vocational training).
# Core product: Automatically adapts tasks, exams and didactic materials for students with NEAE
# (dislexia, TDAH, sensory/motor disabilities) — Human-in-the-loop: teacher reviews & approves.
# Target customers:
#   - Centros educativos (institutos) implementing FP Dual
#   - Empresas colaboradoras (tutores de empresa) receiving FP Dual students
# Key differentiators:
#   - Specialized in Spanish FP Dual inclusive curriculum (all CCAA)
#   - Legal compliance: LOMLOE Art.73, Ley FP 3/2022, LGD, AI Act
#   - Generates Lectura Fácil and Pictogram materials automatically
#   - Integrates with Moodle, Teams, Google Classroom
# Competitors: No direct competitors in this niche. Indirect: generic AI (ChatGPT), basic LMS accessibility tools
# Key market signals to monitor:
#   - BOE / DOGC / BOCM convocatorias for EdTech/inclusión grants
#   - Ministry of Education and regional Consejerías policy moves
#   - New EdTech startups targeting FP Dual or accessibility
#   - EU AI Act implementations affecting EdTech
#   - Corporate tutor compliance obligations

COMPANY_CONTEXT = """
CONTEXTO DE EMPRESA:
Duale (www.duale.es) es un copiloto de IA especializado en FP Dual Inclusiva en España.
- PRODUCTO: Genera automáticamente adaptaciones curriculares y laborales para alumnos con NEAE (Necesidades Específicas de Apoyo Educativo: dislexia, TDAH, discapacidades sensoriales/motoras). El docente o tutor de empresa revisa y aprueba (Human-in-the-loop).
- CLIENTES: (1) Centros educativos con FP Dual, (2) Empresas colaboradoras (tutores de empresa con obligación legal de "ajustes razonables").
- DIFERENCIADORES: Alineado con currículos oficiales de todas las CCAA. Cumple LOMLOE Art.73, Ley FP 3/2022, LGD y AI Act. Genera materiales en Lectura Fácil y Pictogramas. Integra con Moodle, Teams, Classroom.
- COMPETIDORES DIRECTOS: Ninguno conocido en este nicho (IA para FP Dual inclusiva España). Competencia indirecta: ChatGPT genérico, funcionalidades básicas de accesibilidad en LMS.
- ETAPA: Startup early-stage buscando primeros centros piloto y subvenciones públicas.
"""


def _compact_results(search_results, max_items_per_query=3, max_title_chars=120):
    """Serialize search results compactly to keep prompt size manageable."""
    lines = []
    for query, items in search_results.items():
        lines.append(f"[{query}]")
        for item in items[:max_items_per_query]:
            content = item.get("content", "")
            parts = content.split("\n")
            title = parts[0][:max_title_chars] if parts else ""
            url = item.get("url", "")[:200]
            lines.append(f"  - {title} | {url}")
    return "\n".join(lines)


def _call_claude(prompt):
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    try:
        print("Calling Claude API...")
        message = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        text = message.content[0].text
        return text.replace("```html", "").replace("```", "").strip()
    except Exception as e:
        print(f"Claude API error: {e}")
        return None


class ReportGenerator:
    def generate_report(self, search_results):
        prompt = f"""Eres el analista de mercado interno de Duale. Tienes acceso al siguiente contexto de empresa:

{COMPANY_CONTEXT}

A partir de los siguientes resultados de búsqueda de esta semana:
{_compact_results(search_results)}

Redacta un informe de inteligencia de mercado semanal en HTML puro (sin <html> ni <body>).
El informe debe ser ESPECÍFICO y ACCIONABLE. Menciona nombres reales, fechas, importes, entidades concretas.
Nunca uses frases vagas como "se recomienda vigilar". En su lugar, di qué entidad hace qué y cuándo.

ESTRUCTURA OBLIGATORIA:

<h2>🏁 Competidores y Movimientos del Sector EdTech</h2>
¿Hay nuevas startups EdTech en España? ¿Algún actor ha lanzado herramientas de IA para educación/inclusión?
¿Alguna empresa relevante ha conseguido financiación? Menciona nombres, cuantías y fechas.

<h2>📰 Noticias Relevantes (FP Dual, IA Educativa, Inclusión)</h2>
Noticias de esta semana sobre FP Dual, tecnología educativa, NEAE, reformas legislativas.
Con fecha y medio de comunicación. Enfócate en España y Europa (AI Act).

<h2>💰 Ayudas, Subvenciones y Financiación</h2>
Convocatorias abiertas o recién publicadas: BOE, diarios oficiales de CCAA, fondos NextGenEU, CDTI, ENISA.
Incluye: nombre de la convocatoria, entidad, cuantía máxima y fecha de cierre si está disponible.
Estas ayudas son CRÍTICAS para Duale — no omitas ninguna aunque sea pequeña.

<h2>🏛️ Licitaciones y Proyectos Públicos</h2>
Contratos del Ministerio de Educación, Consejerías, ayuntamientos para tecnología educativa, accesibilidad o FP.
Incluye referencia del contrato y presupuesto estimado si está disponible.

<h2>🎯 Oportunidades Clave para Duale esta semana</h2>
Basándote en todo lo anterior, identifica 3-5 acciones concretas que Duale debería tomar esta semana.
Ejemplo: "Presentarse a la convocatoria X antes del DD/MM", "Contactar con la empresa Y que acaba de anunciar Z".

REGLAS DE FORMATO:
- Usa <ul><li> para bullets. Pon en <strong> nombres de entidades, empresas y convocatorias.
- Incluye el enlace fuente cuando exista: <a href="URL" target="_blank">[Fuente]</a>
- Si no hay datos para una sección: <p><em>Sin noticias relevantes esta semana.</em></p>
- Idioma: Español."""

        result = _call_claude(prompt)
        if result:
            return result
        return self._fallback(search_results)

    def generate_linkedin_post(self, search_results):
        prompt = f"""Eres el Community Manager de Duale (www.duale.es), startup de IA para FP Dual Inclusiva en España.

{COMPANY_CONTEXT}

Basándote en estos resultados de búsqueda de esta semana:
{_compact_results(search_results)}

Redacta un post de LinkedIn semanal de máximo 300 palabras. Público objetivo: directores de FP, tutores de empresa, responsables de RRHH de empresas colaboradoras, inversores EdTech.

Estructura:
1. Gancho poderoso en la primera línea (dato, pregunta o provocación sobre FP Dual o inclusión).
2. 3 puntos clave de la semana con datos concretos (noticias, ayudas, tendencias).
3. Conexión con el problema que resuelve Duale (sin ser vendedor, sutil).
4. CTA: comentar, compartir o visitar duale.es.

Tono: Profesional, motivador, orientado a la inclusión. Saltos de línea frecuentes.
Hashtags: #FPDual #EdTech #InclusiónEducativa #Duale #NEAE #FormaciónProfesional
Idioma: Español."""

        result = _call_claude(prompt)
        return result or "Post no disponible esta semana."

    def _fallback(self, search_results):
        html = "<h1>Informe Duale — Datos Recopilados</h1>"
        html += "<p><em>El motor de IA no pudo conectar esta semana. Aquí están los datos en bruto:</em></p>"
        for query, items in search_results.items():
            html += f"<h3>🔍 {query}</h3><ul>"
            for item in items:
                if isinstance(item, dict):
                    url = item.get('url', '#')
                    content = item.get('content', '')[:300]
                    html += f"<li><a href='{url}' target='_blank'>[Fuente]</a> — {content}</li>"
            html += "</ul>"
        return html
