import os
import sys
import streamlit as st
import pandas as pd
import joblib
from PIL import Image
import webbrowser, threading

# ==========================
# Funciones de ayuda
# ==========================
def resource_path(relative_path):
    """ Obtiene la ruta absoluta de recursos tanto en .exe como en desarrollo """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)  # Cuando corre empaquetado
    return os.path.join(os.path.dirname(__file__), relative_path)  # En desarrollo


# ==========================
# Configuración de página
# ==========================
st.set_page_config(
    page_title="Sistema de Predicción Para el Acceso al Canal de Buenaventura",
    page_icon="⛵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================
# Cargar modelo y recursos
# ==========================
try:
    modelo = joblib.load(resource_path("modelo_SVMO_SPAB.pkl"))
except:
    st.error("❌ No se encontró el modelo dentro del ejecutable")

try:
    logo_institucional = Image.open(resource_path("dimar-hor.png"))
    imagen_bahia = Image.open(resource_path("puerto-bv.jpg"))
except:
    logo_institucional = Image.new('RGB', (200, 100), color='navy')
    imagen_bahia = Image.new('RGB', (600, 300), color='lightblue')

# ==========================
# Interfaz
# ==========================
col1, col2 = st.columns([1, 3])

with col1:
    st.image(logo_institucional, width=400)
    st.markdown("---")
    st.markdown("### Parámetros de Entrada")
    
    with st.form("parámetros de navegación"):
        oleaje = st.number_input("Altura de oleaje (m)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        viento = st.number_input("Velocidad del viento (m/s)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        preci = st.number_input("Precipitación", min_value=0.0, max_value=500.0, value=0.0, step=10.0)
        marea = st.number_input("Nivel de marea (m)", min_value=0.0, max_value=5.0, value=0.0, step=0.1)
        calado = st.number_input("Calado del barco (m)", min_value=0.0, max_value=10000.0, value=0.0, step=10.0)
        manga = st.number_input("Manga del barco (m)", min_value=0.0, max_value=1000.0, value=0.0, step=10.0)
        eslora = st.number_input("Eslora del barco (m)", min_value=0.0, max_value=1000.0, value=0.0, step=10.0)

        submitted = st.form_submit_button("Evaluar Condiciones de Navegación")

with col2:
    st.markdown("""<h1 style='text-align: center; margin-top: -40px;'>Sistema de Predicción de Condiciones de Navegación</h1>""", unsafe_allow_html=True)
    st.image(imagen_bahia)
    
    if submitted:
        input_data = pd.DataFrame([[oleaje,viento,preci,marea,calado,manga,eslora]],
                                columns=['hs_c_w', 'wind_speed','precipitation','Marea_filtro','Calado', 'Manga','Eslora'])

        resultado = modelo.predict(input_data)
        
        st.markdown("---")
        st.markdown("## Resultado de la Evaluación")
        
        if resultado[0] == 1:
            st.success("✅ **CONDICIONES FAVORABLES** - El barco puede navegar con seguridad")
        else:
            st.error("⛔ **CONDICIONES DESFAVORABLES** - No se recomienda la navegación en estas condiciones")
        
        with st.expander("Detalles técnicos de la predicción"):
            st.write("Parámetros utilizados para la decisión:")
            st.dataframe(input_data)
            st.write("Modelo utilizado: SVMOclass")

# ==========================
# Estilos CSS
# ==========================
st.markdown("""
<style>
    .stNumberInput, .stSelectbox {
        margin-bottom: 15px;
    }
    .st-b7 {
        background-color: #f0f2f6;
    }
    .css-1aumxhk {
        background-color: #0e1117;
    }
    .css-1v3fvcr {
        padding: 2rem 1rem;
    }
</style>
""", unsafe_allow_html=True)
