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
