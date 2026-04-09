import os
from dotenv import load_dotenv

load_dotenv()

# SMTP Configuration
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "your_email@domain.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "YOUR_APP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "recipient@domain.com")

# API Keys — get yours free at console.groq.com
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "YOUR_ANTHROPIC_API_KEY_HERE")

# Research Parameters — Duale
KEYWORDS = [
    "noticias Formación Profesional España",
    "startups EdTech española",
    "ayudas formación profesional España startup",
    "proyectos innovación Ministerio Educación Dual",
    "licitaciones públicas educación inclusión tecnológica",
    "subvenciones educación NextGenerationEU startups",
    "tecnología educativa inclusión discapacidad España"
]

REPORT_LANGUAGE = "Spanish"
