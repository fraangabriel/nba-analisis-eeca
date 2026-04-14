import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.database import get_resumen_temporadas
from modules.stats_logic import ajustar_regresion_lineal

st.set_page_config(page_title="Contrastes y Confianza", layout="wide")
st.title("⚖️ Contrastes de Hipótesis e Intervalos")

df = get_resumen_temporadas()

if not df.empty:
    modelo = ajustar_regresion_lineal(df, 'avg_pace', 'avg_ppg')

    st.subheader("1. Contraste sobre la Pendiente (B)")
    st.write("¿Es el Ritmo un factor determinante para predecir los Puntos?")

    # Extraer t-stat y p-value para B (avg_pace)
    t_b = modelo.tvalues['avg_pace']
    p_b = modelo.pvalues['avg_pace']
    ic = modelo.conf_int().loc['avg_pace']

    c1, c2 = st.columns(2)
    with c1:
        st.latex(r"H_0: B = 0 \quad H_1: B \neq 0")
        st.write(f"**Valor de t:** {t_b:.4f}")
        st.write(f"**p-valor:** {p_b:.4e}")

    with c2:
        st.write("**Intervalo de Confianza (95%) para B:**")
        st.info(f"Limit. Inferior: {ic[0]:.4f} | Limit. Superior: {ic[1]:.4f}")

    if p_b < 0.05:
        st.success("Rechazamos H0: La velocidad de juego influye linealmente en la anotación.")
