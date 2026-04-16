# modules/sidebar.py
import streamlit as st

def membrete():
    st.markdown("### 🏛️ Universidad Central de Venezuela")
    st.markdown("**Facultad de Ciencias Económicas y Sociales**")
    st.markdown("*Escuela de Estadística y Ciencias Actuariales*")

def metodologia_sidebar():
    with st.expander("📊 Sobre el estudio"):
        st.caption("📅 **Período:** 2013-14 a 2022-23")
        st.caption("🏀 **Temporadas:** 10")
        st.caption("📈 **Variable clave:** Pace (posesiones por 48 min) → PPG")
        st.caption("🎯 **Objetivo:** Analizar relación velocidad vs anotación")

def nav(nombre:str,pagina:str):
    """
    Crea un botón de navegación personalizado
    
    Args:
        nombre (str): el texto que mostrará el botón
        pagina (str): la página a la que redirigirá el botón
    """
    if st.button(nombre, use_container_width=True):
        st.switch_page(pagina)

def nav_sidebar():
    st.divider()
    st.markdown("### 🧭 Navegación")
    nav("🏠 Inicio", "app.py")
    nav("📖 Teoría", "pages/1Teoría.py")
    nav("📊 Exploración", "pages/2Exploracion_de_datos.py")
    nav("📈 Correlación", "pages/3Correlacion.py")
    nav("📐 Contrastes", "pages/4Contrastes.py")
    nav("🧪 Regresión", "pages/5Regresion.py")
    nav("🖥️ Consultas SQL", "pages/6Consultas.py")
    nav("🎯 Conclusión", "pages/7Conclusion.py")
    st.divider()

def mostrar_sidebar_inicio():
    """Sidebar unificado para el inicio"""
    
    with st.sidebar:
        st.markdown("# 🏀 NBA Analytics")
        st.divider()
        membrete()
        nav_sidebar()
        metodologia_sidebar()

def mostrar_sidebar_secciones():
    """Sidebar unificado para las secciones"""

    with st.sidebar:
        st.markdown("# 🏀 NBA Analytics")
        nav_sidebar()
        metodologia_sidebar()
        membrete()
