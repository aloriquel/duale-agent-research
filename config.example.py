import os
from dotenv import load_dotenv

load_dotenv()

# Gemini REST API Endpoint
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

# Email Configuration
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
SMTP_USERNAME = "your_email@domain.com"
SMTP_PASSWORD = "YOUR_APP_PASSWORD"
RECIPIENT_EMAIL = "recipient@domain.com"

# Research Parameters
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
