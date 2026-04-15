import streamlit as st
import plotly.express as px
import scipy.stats as stats
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.database import get_resumen_temporadas
from modules.stats_logic import obtener_metricas_correlacion

st.set_page_config(page_title="Correlación NBA", layout="wide")
st.title("📉 Análisis de Correlación Lineal y por Rangos")

df = get_resumen_temporadas()

if not df.empty:
    # Metricas (Pearson r y Spearman rho)
    m = obtener_metricas_correlacion(df, 'avg_pace', 'avg_ppg')

    st.markdown("### 1. Coeficientes y Contrastes")
    c1, c2 = st.columns(2)

    with c1:
        st.metric("Pearson (r) - Grado Lineal", f"{m['r']:.4f}")
        # Contraste de significación de la correlación (Página 9 PDF UCV)
        t_calc = m['t_r']
        p_val = stats.t.sf(abs(t_calc), m['n'] - 2) * 2
        st.write(f"**Estadístico t:** {t_calc:.4f} | **p-valor:** {p_val:.4f}")
        if p_val < 0.05:
            st.success("Correlación Lineal Significativa ✅")
        else:
            st.warning("No se observa correlación lineal significativa ❌")

    with c2:
        st.metric("Spearman (ρ) - Rango/Orden", f"{m['rho']:.4f}")
        st.write(f"**p-valor (Spearman):** {m['p_rho']:.4f}")
        if m['p_rho'] < 0.05:
            st.success("Relación monótona significativa ✅")

    st.divider()

    st.markdown("### 2. Interpretación por Rangos)")
    def interpretar_rango(valor):
        val = abs(valor)
        if 0.00 <= val <= 0.30: return "Débil o Nula", "gray"
        elif 0.31 <= val <= 0.60: return "Moderada", "blue"
        elif 0.61 <= val <= 0.80: return "Fuerte", "orange"
        else: return "Muy Fuerte", "green"

    interp_p, color_p = interpretar_rango(m['r'])
    interp_s, color_s = interpretar_rango(m['rho'])

    st.write(f"La correlación de Pearson es **{interp_p}**.")
    st.write(f"La correlación de Spearman es **{interp_s}**.")

    # Gráfico interactivo
    fig = px.scatter(df, x='avg_pace', y='avg_ppg', text='season', trendline="ols",
                     title="Ritmo vs Puntos (Diagrama de Dispersión)")
    st.plotly_chart(fig, use_container_width=True)