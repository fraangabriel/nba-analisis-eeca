# modules/sidebar.py
import streamlit as st

def mostrar_sidebar():
    """Sidebar unificado para todas las páginas"""
    
    with st.sidebar:
        st.markdown("# 🏀 NBA Analytics")
        st.markdown("---")
 
        
        st.markdown("### 🧭 Navegación")
        
        if st.button("🏠 Inicio", use_container_width=True):
            st.switch_page("app.py")
        
        if st.button("📖 Teoría", use_container_width=True):
            st.switch_page("pages/1Teoría.py")
        
        if st.button("📊 Exploración", use_container_width=True):
            st.switch_page("pages/2Exploracion_de_datos.py")
        
        if st.button("📈 Correlación", use_container_width=True):
            st.switch_page("pages/3Correlacion.py")
        
        if st.button("📐 Contrastes", use_container_width=True):
            st.switch_page("pages/4Contrastes.py")
        
        if st.button("🧪 Regresión", use_container_width=True):
            st.switch_page("pages/5Regresion.py")
        
        st.markdown("---")
        
        st.markdown("### 📊 Sobre el estudio")
        st.caption("📅 **Período:** 2013-14 a 2022-23")
        st.caption("🏀 **Temporadas:** 10")
        st.caption("📈 **Variable clave:** Pace (posesiones por 48 min) → PPG")
        st.caption("🎯 **Objetivo:** Analizar relación velocidad vs anotación")
        
        st.markdown("---")
        st.caption("Proyecto de Análisis NBA 2013-2023")
        st.caption("Velocidad vs Eficiencia")
                
        st.caption("### 🏛️ Universidad Central de Venezuela")
        st.caption("**Facultad de Ciencias Económicas y Sociales**")
        st.caption("*Escuela de Estadística y Ciencias Actuariales*")