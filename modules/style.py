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
            
            /* ===== SIDEBAR AZUL MÁS OSCURO ===== */
            [data-testid="stSidebar"] {
                background-color: #0a1c3a !important;  /* Azul más oscuro */
            }
            
            /* Color del texto en el sidebar */
            [data-testid="stSidebar"] .stMarkdown {
                color: #ffffff !important;
            }
            
            /* Títulos en el sidebar */
            [data-testid="stSidebar"] h1, 
            [data-testid="stSidebar"] h2, 
            [data-testid="stSidebar"] h3 {
                color: #ffffff !important;
            }
            
            /* Texto de captura en sidebar */
            [data-testid="stSidebar"] .stCaption {
                color: #bbbbbb !important;
            }
            
            /* Botones en el sidebar */
            [data-testid="stSidebar"] .stButton button {
                background-color: #c8102e !important;  /* Rojo NBA */
                color: white !important;
            }
            
            /* ===== CONTENEDORES ===== */
            .stContainer {
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                padding: 5px;
                margin-bottom: 20px;
            }
            
            /* ===== BOTONES ===== */
            .stButton button {
                border-radius: 8px;
                font-weight: bold;
                transition: all 0.3s;
                background-color: #7a1525;
                color: white;
            }
            
            .stButton button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                background-color: #e01838;
            }
            
            /* ===== TÍTULOS PRINCIPALES ===== */
            h1 {
                color: #0a1c3a;
                font-size: 2.5rem;
                text-align: center;
            }
            
            /* ===== SUBTÍTULOS ===== */
            h2 {
                color: #0a1c3a;
                border-left: 4px solid #c8102e;
                padding-left: 15px;
            }
            
            /* ===== TÍTULOS DE OBJETIVOS ===== */
            h3 {
                color: #0a1c3a;
            }
            
            /* ===== PIE DE PÁGINA ===== */
            .stCaption {
                text-align: center;
                color: #888;
            }
            
            /* ===== MÉTRICAS ===== */
            [data-testid="stMetric"] {
                border-top: 3px solid #c8102e;
            }
        </style>
        """,
        unsafe_allow_html=True
    )