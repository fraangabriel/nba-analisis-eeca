import streamlit as st
from modules.style import aplicar_estilos_globales
from modules.sidebar import mostrar_sidebar_secciones
from modules.navegacion import navegacion

st.set_page_config(page_title="Consultas SQL (SQLite)", layout="wide")

aplicar_estilos_globales()
mostrar_sidebar_secciones()

# ==================== NAVEGACIÓN ====================
st.divider()
navegacion("Regresión", "Conclusión")
