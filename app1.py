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
    st.markdown("### 📖 ¿Cómo funciona?")
    st.markdown("**OCR** (*Optical Character Recognition*) analiza los píxeles de una imagen para identificar letras y palabras.")
    st.markdown("**Consejos para mejores resultados:**")
    st.markdown("- 💡 Buena iluminación")
    st.markdown("- 📄 Texto nítido y sin desenfoque")
    st.markdown("- ⬛ Buen contraste entre texto y fondo")
    st.markdown("- 📐 Imagen lo más recta posible")

# ── Captura de imagen ──────────────────────────────────────────────
st.markdown("### 📸 Captura")
img_input = None

if fuente == "📷 Cámara":
    img_input = st.camera_input("Toma una foto")
else:
    img_input = st.file_uploader("Sube una imagen:", type=["png", "jpg", "jpeg", "bmp"])

# ── Procesamiento ──────────────────────────────────────────────────
if img_input is not None:
    bytes_data = img_input.getvalue()
    cv2_img    = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    if filtro == "Invertir colores":
        cv2_img_proc = cv2.bitwise_not(cv2_img)
    elif filtro == "Escala de grises":
        gray         = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
        cv2_img_proc = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    elif filtro == "Alto contraste":
        gray         = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
        _, thresh    = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        cv2_img_proc = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    else:
        cv2_img_proc = cv2_img

    img_rgb = cv2.cvtColor(cv2_img_proc, cv2.COLOR_BGR2RGB)

    st.markdown("---")

    # ── Comparación de imágenes ────────────────────────────────────
    st.markdown("### 🖼️ Imagen procesada")
    col_orig, col_proc = st.columns(2)
    with col_orig:
        st.markdown("**Original**")
        st.image(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB), use_container_width=True)
    with col_proc:
        st.markdown(f"**Con filtro: {filtro}**")
        st.image(img_rgb, use_container_width=True)

    # ── OCR ───────────────────────────────────────────────────────
    st.markdown("---")
    with st.spinner("🔍 Extrayendo texto..."):
        text = pytesseract.image_to_string(img_rgb)

    # ── Métricas ───────────────────────────────────────────────────
    palabras   = len(text.split()) if text.strip() else 0
    caracteres = len(text.strip())
    lineas     = len([l for l in text.split("\n") if l.strip()])

    st.markdown("### 📊 Resumen")
    m1, m2, m3 = st.columns(3)
    m1.metric("📝 Palabras detectadas", palabras)
    m2.metric("🔤 Caracteres",          caracteres)
    m3.metric("📄 Líneas",              lineas)

    # ── Texto extraído ─────────────────────────────────────────────
    st.markdown("### 📋 Texto extraído")
    if text.strip():
        st.markdown(
            f'<div class="texto-resultado">{text}</div>',
            unsafe_allow_html=True
        )
        st.download_button(
            "⬇️ Descargar texto (.txt)",
            data=text,
            file_name="texto_extraido.txt",
            mime="text/plain"
        )
    else:
        st.warning("⚠️ No se detectó texto. Intenta mejorar la iluminación o el enfoque.")
