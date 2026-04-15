import streamlit as st
from modules.database import get_resumen_temporadas

# Configuración de la página
st.set_page_config(
    page_title="NBA Analytics | Velocidad vs Eficiencia",
    page_icon="🏀",
    layout="wide"
)

# ==================== CARGA DE DATOS ====================
# Cargar los datos una sola vez y guardarlos en session_state
if 'df_resumen' not in st.session_state:
    df = get_resumen_temporadas()
    st.session_state['df_resumen'] = df
    
    # También crear un formato amigable para la exploración
    # Renombrar columnas para que coincidan con Exploracion.py
    df_exploracion = df.rename(columns={
        'season': 'Season',
        'avg_ppg': 'PPG',
        'avg_pace': 'Pace',
        'avg_efg': 'eFG%'
    })
    # Agregar columna Team (como promedio de la liga para cada temporada)
    df_exploracion['Team'] = 'NBA Average'
    st.session_state['df'] = df_exploracion

# ==================== PÁGINA PRINCIPAL ====================
st.title("🏀 Análisis de Datos de la NBA (2013-2023)")
st.subheader("Velocidad vs Eficiencia: La Década que Cambió la NBA")

st.markdown("""
**Descripción del proyecto:**
Este proyecto estudia cómo ha cambiado la forma de jugar y de anotar en la NBA desde el año 2013 hasta el 2023. El estudio se enfoca en ver si los equipos anotan más puntos porque ahora juegan más rápido o porque han mejorado su puntería.

En los últimos años, la NBA ha vivido una transformación radical: el ritmo es más vertiginoso, el volumen de triples se ha disparado y los marcadores son cada vez más altos. Este dashboard busca responder mediante rigor estadístico si el innegable incremento en los puntos por partido se debe a un mayor volumen de posesiones o a una mejora sustancial en la puntería.
""")

# Mostrar vista previa de los datos
with st.expander("📊 Ver datos cargados (promedios por temporada)"):
    st.dataframe(st.session_state['df_resumen'])
    
    # Métricas básicas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Temporadas", len(st.session_state['df_resumen']))
    with col2:
        st.metric("Rango", "2013-14 a 2022-23")
    with col3:
        st.metric("Variables", "Pace, PPG, eFG%")

st.info("👈 Selecciona una opción en la barra lateral para comenzar la exploración y el análisis estadístico.")