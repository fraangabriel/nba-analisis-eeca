import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy import stats
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.database import get_resumen_temporadas

st.set_page_config(page_title="Contrastes NBA", layout="wide")
st.title("📐 Contraste de Hipótesis: Ritmo vs Puntos")
st.markdown("Verificamos si la relación entre **ritmo de juego (Pace)** y **puntos por partido (PPG)** es estadísticamente significativa.")
st.markdown("---")

# ==================== CARGA DE DATOS ====================
if 'df_resumen' not in st.session_state:
    st.session_state['df_resumen'] = get_resumen_temporadas()

df_raw = st.session_state['df_resumen'].copy()

def convertir_temporada(codigo):
    codigo_str = str(codigo)
    if len(codigo_str) == 4:
        return f"20{codigo_str[:2]}-{codigo_str[2:]}"
    return codigo_str

df_raw['Temporada'] = df_raw['season'].apply(convertir_temporada)
df_raw = df_raw.rename(columns={
    'avg_ppg': 'PPG', 
    'avg_pace': 'Pace', 
    'avg_efg': 'eFG%'
})


# ==================== FILTROS ====================
with st.container():
    st.subheader("🔍 Filtros")
    
    col_f1, col_f2 = st.columns(2)
    temps = df_raw['Temporada'].tolist()
    
    with col_f1:
        inicio = st.selectbox("Temporada inicio", temps, index=0)
    with col_f2:
        idx = temps.index(inicio)
        fin = st.selectbox("Temporada fin", temps[idx:], index=len(temps[idx:])-1)

idx_i, idx_f = temps.index(inicio), temps.index(fin)
df = df_raw.iloc[idx_i:idx_f+1].copy()

st.markdown("---")
# ==================== PLANTEAMIENTO DE HIPÓTESIS ====================
with st.container():
    st.subheader("🎯 Planteamiento de la Hipótesis")
    
    st.markdown("""
    **Hipótesis Nula (H₀):** El ritmo de juego **NO tiene efecto** sobre los puntos por partido.
    
    **Hipótesis Alternativa (H₁):** El ritmo de juego **SÍ tiene efecto** sobre los puntos por partido.
    """)
    
    st.latex(r"H_0: \beta = 0 \quad \text{(la pendiente es cero)}")
    st.latex(r"H_1: \beta \neq 0 \quad \text{(la pendiente es distinta de cero)}")

st.markdown("---")
# ==================== CÁLCULOS ====================
# Calcular correlación y estadístico t
x = df['Pace']
y = df['PPG']
n = len(df)  

r, p_valor = stats.pearsonr(x, y)
t_stat = r * np.sqrt((n-2)/(1-r**2)) if abs(r) < 1 else 0
df_resid = n - 2
t_critico = stats.t.ppf(1 - 0.05/2, df_resid)

# ==================== RESULTADOS ====================
with st.container():
    st.subheader("📊 Resultados del Contraste")
    
    col_r1, col_r2, col_r3, col_r4 = st.columns(4)
    with col_r1:
        st.metric("📈 Correlación (r)", f"{r:.4f}")
    with col_r2:
        st.metric("📐 Estadístico t", f"{t_stat:.4f}")
    with col_r3:
        st.metric("⚖️ Valor crítico (α=0.05)", f"{t_critico:.4f}")
    with col_r4:
        st.metric("📋 Grados de libertad", f"{df_resid}")

st.markdown("---")
# ==================== GRÁFICO REGIÓN CRÍTICA ====================
with st.container():
    st.subheader("📈 Distribución t-Student y Región Crítica")
    
    x_vals = np.linspace(-5, 5, 500)
    y_vals = stats.t.pdf(x_vals, df_resid)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', 
                              name=f't-Student (gl={df_resid})', 
                              line=dict(color='white', width=2)))
    
    x_rechazo_der = np.linspace(t_critico, 5, 100)
    fig.add_trace(go.Scatter(x=x_rechazo_der, y=stats.t.pdf(x_rechazo_der, df_resid),
                              fill='tozeroy', name='Zona de Rechazo (α=0.05)',
                              fillcolor='rgba(255, 0, 0, 0.4)', line=dict(width=0)))
    
    x_rechazo_izq = np.linspace(-5, -t_critico, 100)
    fig.add_trace(go.Scatter(x=x_rechazo_izq, y=stats.t.pdf(x_rechazo_izq, df_resid),
                              fill='tozeroy', showlegend=False,
                              fillcolor='rgba(255, 0, 0, 0.4)', line=dict(width=0)))
    
    fig.add_vline(x=t_stat, line_width=3, line_dash="dash", line_color="yellow")
    fig.add_annotation(x=t_stat, y=0.15, text=f"t = {t_stat:.3f}",
                        showarrow=True, arrowhead=1, bgcolor="yellow", 
                        font=dict(color="black", size=12))
    
    fig.add_vline(x=t_critico, line_width=1, line_dash="dot", line_color="orange")
    fig.add_vline(x=-t_critico, line_width=1, line_dash="dot", line_color="orange")
    
    fig.update_layout(title=f"Distribución t-Student con {df_resid} grados de libertad",
                      xaxis_title="Valor t", yaxis_title="Densidad",
                      template="plotly_dark", height=500)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
# ==================== DECISIÓN ESTADÍSTICA ====================
with st.container():
    st.subheader("📌 Decisión Estadística")
    
    if abs(t_stat) > t_critico:
        mensaje = f"""
✅ **Se rechaza la hipótesis nula (H₀)**

| Medida | Valor |
|--------|-------|
| t-estadístico | {t_stat:.4f} |
| t-crítico (α=0.05) | {t_critico:.4f} |
| p-valor | {p_valor:.4f} |

**Conclusión:** El ritmo de juego **SÍ tiene un efecto estadísticamente significativo** sobre los puntos por partido.

➡️ Esto confirma que **a mayor ritmo, mayor anotación**, y esta relación no es producto del azar.
"""
        st.success(mensaje)
    else:
        mensaje = f"""
⚠️ **No se rechaza la hipótesis nula (H₀)**

| Medida | Valor |
|--------|-------|
| t-estadístico | {t_stat:.4f} |
| t-crítico (α=0.05) | {t_critico:.4f} |
| p-valor | {p_valor:.4f} |

**Conclusión:** No hay evidencia suficiente para afirmar que el ritmo de juego afecta los puntos por partido.

➡️ Esto sugiere que otros factores (como la eficiencia de tiro) podrían tener mayor impacto.
"""
        st.warning(mensaje)

st.markdown("---")
# ==================== INTERPRETACIÓN ADICIONAL ====================
with st.expander("📖 ¿Qué significa el p-valor?"):
    st.markdown(f"""
    **p-valor = {p_valor:.4f}**
    
    - Si p-valor < 0.05: La relación es **estadísticamente significativa**
    - Si p-valor ≥ 0.05: La relación **no es significativa**
    
    **En este caso:** {'p-valor < 0.05, por lo que rechazamos H₀' if p_valor < 0.05 else 'p-valor ≥ 0.05, por lo que no rechazamos H₀'}
    
    Esto significa que la probabilidad de obtener esta correlación por azar es del **{p_valor*100:.2f}%**.
    """)

# ==================== TABLA DE DATOS OPCIONAL ====================
with st.expander("📋 Ver datos del período"):
    df_show = df[['Temporada', 'Pace', 'PPG']].copy()
    st.dataframe(df_show.round(2), use_container_width=True)
    
    csv = df_show.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar CSV", data=csv, 
                       file_name=f"contraste_pace_ppg_{inicio}_a_{fin}.csv", 
                       mime="text/csv")

st.markdown("---")# ==================== NAVEGACIÓN ====================
col_n1, col_n2 = st.columns(2)
with col_n1:
    if st.button("◀ Volver a Correlación", use_container_width=True):
        st.switch_page("pages/3Correlacion.py")
with col_n2:
    if st.button("➡️ Ir a Regresión", use_container_width=True):
        st.switch_page("pages/5Regression.py")

st.caption(f"📌 **Período:** {inicio} → {fin} | **n = {n}** temporadas | **p-valor = {p_valor:.4f}** | **r = {r:.3f}**")