import streamlit as st
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.database import get_resumen_temporadas
from modules.stats_logic import ajustar_regresion_lineal

st.set_page_config(page_title="Regresión Lineal NBA", layout="wide")

st.title("🧪 Análisis de Regresión Lineal Bivariante")

df = get_resumen_temporadas()

if not df.empty:
    col_x = 'avg_pace'
    col_y = 'avg_ppg'

    modelo = ajustar_regresion_lineal(df, col_x, col_y)

    col_info, col_graph = st.columns([1, 2])

    with col_info:
        st.subheader("📊 Parámetros del Modelo")

        # Al usar formulas, los nombres cambian:
        # Intercepto -> 'Intercept'
        # Pendiente -> nombre de la variable X ('avg_pace')
        a = modelo.params['Intercept']
        b = modelo.params[col_x]
        r2 = modelo.rsquared

        st.latex(rf"Y = {a:.2f} + {b:.2f} \cdot X")

        st.write(f"**Coeficiente de Determinación ($r^2$):** {r2:.4f}")
        st.info(f"El {r2*100:.1f}% de la variación en los puntos es explicada por el ritmo de juego.")

        # Mostrar resumen estadístico breve
        with st.expander("Ver Resumen Estadístico (Summary)"):
            st.text(modelo.summary().as_text())

    with col_graph:
        st.subheader("📈 Gráfico Interactivo")
        fig = px.scatter(
            df, x=col_x, y=col_y,
            text='season', trendline="ols",
            labels={col_x: 'Ritmo (Pace)', col_y: 'Puntos (PPG)'},
            template="plotly_dark"
        )
        fig.update_traces(textposition='top center')
        st.plotly_chart(fig, use_container_width=True)
