import streamlit as st
from modules.style import aplicar_estilos_globales
from modules.sidebar import mostrar_sidebar_secciones

st.set_page_config(page_title="Conclusión", layout="wide")

aplicar_estilos_globales()
mostrar_sidebar_secciones()
