import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

# ── Configuración ──────────────────────────────────────────────────
st.set_page_config(page_title="OCR - Reconocimiento de Texto", page_icon="📷", layout="wide")

# ── Estilos ────────────────────────────────────────────────────────
st.markdown("""
<style>
.stApp { background-color: #fffde7; color: #333333; }

div.stButton > button {
    background-color: #f9a825;
    color: white;
    border-radius: 10px;
    padding: 10px 24px;
    border: none;
    font-size: 16px;
    transition: background-color 0.3s ease;
}
div.stButton > button:hover { background-color: #f57f17; color: white; }
section[data-testid="stSidebar"] { background-color: #fff9c4; }
h1, h2, h3 { color: #f57f17; }

[data-testid="metric-container"] {
    background: #fff8e1;
    border: 1px solid #ffe082;
    border-top: 3px solid #f9a825;
    border-radius: 8px;
    padding: 18px 22px;
}
[data-testid="metric-container"] label {
    color: #f57f17 !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #333333 !important;
    font-weight: 700 !important;
}

div[data-testid="stExpander"] {
    border: 1px solid #ffe082 !important;
    border-radius: 8px !important;
    background: #fff8e1 !important;
}
hr { border-color: #ffe082 !important; }

.texto-resultado {
    background: #fff8e1;
    border: 1px solid #ffe082;
    border-left: 5px solid #f9a825;
    border-radius: 8px;
    padding: 20px;
    font-size: 16px;
    line-height: 1.8;
    color: #333333;
    white-space: pre-wrap;
}
</style>
""", unsafe_allow_html=True)

# ── Título ─────────────────────────────────────────────────────────
st.title("📷 Reconocimiento Óptico de Caracteres")
st.markdown("Toma una foto o sube una imagen y extrae automáticamente el texto que contiene.")

# ── Sidebar ────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Opciones")

    fuente = st.radio("📥 Fuente de imagen:", ["📷 Cámara", "🖼️ Subir imagen"])

    st.markdown("---")
    st.markdown("### 🎨 Filtros de imagen")
    filtro = st.radio("Selecciona un filtro:", [
        "Sin filtro",
        "Invertir colores",
        "Escala de grises",
        "Alto contraste",
    ])

    st.markdown("---")
    st.markdown("""
    ### 📖 ¿Cómo funciona?
    **OCR** (*Optical Character Recognition*) analiza los píxeles de una imagen
    para identificar letras y palabras.

    **Consejos para mejores resultados:**
    - 💡 Buena iluminación
    - 📄 Texto nítido y sin desenfoque
    - ⬛ Buen contraste entre
