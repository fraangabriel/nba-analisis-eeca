import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.database import get_resumen_temporadas
from modules.stats_logic import ajustar_regresion_lineal

st.set_page_config(page_title="Contrastes y Confianza", layout="wide")

df = get_resumen_temporadas()

# Seleccionar la variable para el contraste
def seleccionar_variable(df):
    options = ['avg_pace', 'avg_efg']
    format_func = lambda x: "Ritmo (Pace)" if x == 'avg_pace' else "Eficiencia (eFG%)" 
    return st.selectbox("Variable para el Contraste:", options, format_func=format_func)

# Funcion para crear el grafico de contraste, x = variable independiente
def grafico_contraste(model,x):
    t_stat = model.tvalues[x]
    p_val_t = model.pvalues[x]
    df_resid = int(model.df_resid)
    t_critico = stats.t.ppf(1 - 0.05/2, df_resid)

    x = np.linspace(-5, 5, 500)
    y = stats.t.pdf(x, df_resid)
    fig_t = go.Figure()
    fig_t.add_trace(go.Scatter(x=x, y=y, mode='lines', name='t-Student', line=dict(color='white')))

    x_rechazo_der = np.linspace(t_critico, 5, 100)
    fig_t.add_trace(go.Scatter(x=x_rechazo_der, y=stats.t.pdf(x_rechazo_der, df_resid), fill='tozeroy', name='Zona de Rechazo', fillcolor='rgba(255, 0, 0, 0.5)', line=dict(width=0)))
    x_rechazo_izq = np.linspace(-5, -t_critico, 100)
    fig_t.add_trace(go.Scatter(x=x_rechazo_izq, y=stats.t.pdf(x_rechazo_izq, df_resid), fill='tozeroy', showlegend=False, fillcolor='rgba(255, 0, 0, 0.5)', line=dict(width=0)))

    fig_t.add_vline(x=t_stat, line_width=3, line_dash="dash", line_color="yellow")
    fig_t.add_annotation(x=t_stat, y=0.1, text=f"t-calculado: {t_stat:.2f}", showarrow=True, arrowhead=1, bgcolor="yellow", font=dict(color="black"))

    fig_t.update_layout(title="Distribución t de Student y Región Crítica", template="plotly_dark", height=400)
    return fig_t

if not df.empty:
    variable_x = seleccionar_variable(df)

    # LLamada a la funcion de regresion lineal
    model = ajustar_regresion_lineal(df, variable_x, 'avg_ppg')

    st.plotly_chart(grafico_contraste(model, variable_x), use_container_width=True)
