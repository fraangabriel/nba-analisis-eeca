# modules/style.py
import streamlit as st

def aplicar_estilos_globales():
    """Aplica estilos CSS a todas las páginas"""
    
    st.markdown(
        """
        <style>
            /* Ocultar la navegación automática de Streamlit */
            [data-testid="stSidebarNav"] {
                display: none !important;
            }
            
            .stSidebarNav {
                display: none !important;
            }
            
            nav[data-testid="stSidebarNav"] {
                display: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )