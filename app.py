import streamlit as st

st.set_page_config(
    page_title="NBA Analytics | Velocidad vs Eficiencia",
    page_icon="🏀",
    layout="wide"
)

# 2. Bienvenida y Planteamiento
st.title("🏀 Análisis de Datos de la NBA (2013-2023)")
st.subheader("Velocidad vs Eficiencia: La Década que Cambió la NBA")

st.markdown("""
**Descripción del proyecto:**
Este proyecto estudia cómo ha cambiado la forma de jugar y de anotar en la NBA desde el año 2013 hasta el 2023. El estudio se enfoca en ver si los equipos anotan más puntos porque ahora juegan más rápido o porque han mejorado su puntería.

En los últimos años, la NBA ha vivido una transformación radical: el ritmo es más vertiginoso, el volumen de triples se ha disparado y los marcadores son cada vez más altos. Este dashboard busca responder mediante rigor estadístico si el innegable incremento en los puntos por partido se debe a un mayor volumen de posesiones o a una mejora sustancial en la puntería.
""")

st.info("👈 Selecciona una opción en la barra lateral para comenzar la exploración y el análisis estadístico.")