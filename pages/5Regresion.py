import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys
import os
from modules.style import aplicar_estilos_globales
from modules.sidebar import mostrar_sidebar_secciones

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.database import get_resumen_temporadas
from modules.stats_logic import ajustar_regresion_lineal

st.set_page_config(page_title="Regresión NBA", layout="wide")
st.title("🧪 Modelo de Regresión Lineal")
st.markdown("Cuantificamos cómo el **ritmo de juego (Pace)** predice los **puntos por partido (PPG)** mediante un modelo de regresión lineal.")
st.markdown("---")

# ==================== BANNER OPCIÓN  ====================
st.markdown(
    """
    <div style="
        background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?q=80&w=2076');
        background-size: cover;
        background-position: center;
        height: 130px;
        border-radius: 10px;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    ">
        <div style="text-align: center;">
            <span style="color: white; font-size: 1.6rem; font-weight: bold; letter-spacing: 3px;">🧪 REGRESIÓN LINEAL</span>
            <br>
            <span style="color: white; font-size: 1rem;">Modelo Predictivo · R² · PPG = a + b·Pace</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)




# Aplicar estilos globales
aplicar_estilos_globales()

# Mostrar sidebar
mostrar_sidebar_secciones()

# ==================== INICIALIZAR ESTADO ====================
if 'seccion_regresion' not in st.session_state:
    st.session_state.seccion_regresion = 'modelo'

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
    st.subheader("🔍 Filtros de temporada")
    st.caption("💡 Selecciona el período para construir el modelo de regresión.")
    
    col_f1, col_f2 = st.columns(2)
    temps = df_raw['Temporada'].tolist()
    
    with col_f1:
        inicio = st.selectbox("📅 Temporada inicio", temps, index=0)
    with col_f2:
        idx = temps.index(inicio)
        fin = st.selectbox("📅 Temporada fin", temps[idx:], index=len(temps[idx:])-1)

idx_i, idx_f = temps.index(inicio), temps.index(fin)
df = df_raw.iloc[idx_i:idx_f+1].copy()
n = len(df)

# Validar mínimo de temporadas
if n < 4:
    st.warning(f"⚠️ Seleccionaste solo {n} temporada(s). Para un análisis estadístico válido se recomiendan al menos 4 temporadas.")
    st.stop()

st.markdown("---")
st.markdown("---")

# ==================== CÁLCULOS DEL MODELO ====================
# Ajustar modelo (se usa en ambas secciones)
modelo = ajustar_regresion_lineal(df, 'Pace', 'PPG')

intercepto = modelo.params['Intercept']
pendiente = modelo.params['Pace']
r2 = modelo.rsquared
r2_adj = modelo.rsquared_adj

# ==================== DEFINIR VARIABLES DE REFERENCIA  ====================
pace_min = df['Pace'].min()
pace_max = df['Pace'].max()
ppg_min = intercepto + pendiente * pace_min
ppg_max = intercepto + pendiente * pace_max

# ==================== BOTONES: MODELO vs PREDICTOR ====================
with st.container():
    st.subheader("📊 ¿Qué deseas visualizar?")
    
    col_b1, col_b2 = st.columns(2)
    
    with col_b1:
        if st.button("📐 Ver Modelo de Regresión", use_container_width=True):
            st.session_state.seccion_regresion = 'modelo'
    
    with col_b2:
        if st.button("🔮 Ver Predictor Interactivo", use_container_width=True):
            st.session_state.seccion_regresion = 'predictor'

st.markdown("---")


# ==================== SECCIÓN 1: MODELO DE REGRESIÓN ====================
if st.session_state.seccion_regresion == 'modelo':
    
    with st.container():
        st.subheader("📐 Parámetros del Modelo")
        
        col_e1, col_e2, col_e3, col_e4 = st.columns(4)
        with col_e1:
            st.metric("📐 Intercepto (a)", f"{intercepto:.2f}")
        with col_e2:
            st.metric("📈 Pendiente (b)", f"{pendiente:.4f}")
        with col_e3:
            st.metric("📊 R²", f"{r2:.4f}")
        with col_e4:
            st.metric("📊 R² Ajustado", f"{r2_adj:.4f}")
    
    st.markdown("---")
    
    with st.container():
        st.subheader("📝 Ecuación del Modelo")
        
        st.latex(rf"PPG = {intercepto:.2f} + {pendiente:.4f} \cdot Pace")
        
        st.caption("📏 **Unidad de medida del Pace:** Número de **posesiones por cada 48 minutos de juego**.")
        
        st.info(f"""
        **Interpretación del modelo:**
        
        - **Pendiente ({pendiente:.4f}):** Por cada **posesión adicional por cada 48 minutos**, los puntos aumentan en **{pendiente:.2f} puntos**.
        
        - **Rango de aplicación:** Ritmos entre **{pace_min:.1f}** y **{pace_max:.1f}** posesiones por 48 minutos.
        
        - **Impacto práctico:** 
            | Ritmo | PPG estimado |
            |-------|--------------|
            | {pace_min:.1f} (más lento) | {ppg_min:.1f} |
            | {pace_max:.1f} (más rápido) | {ppg_max:.1f} |
        
        ➡️ **Un aumento de 10 posesiones** se asocia con **{pendiente*10:.2f} puntos más** por partido.
        """)
    
    st.markdown("---")
    
    with st.container():
        st.subheader("📊 Diagrama de Dispersión con Recta de Regresión")
        
        fig = px.scatter(df, x='Pace', y='PPG', text='Temporada',
                         title=f'Regresión Lineal: R² = {r2:.3f}',
                         trendline="ols", 
                         trendline_color_override="yellow",
                         template='plotly_dark',
                         labels={'Pace': 'Ritmo (Pace) - Posesiones por 48 min', 'PPG': 'Puntos por Partido'})
        fig.update_traces(textposition='top center', marker=dict(size=18, opacity=0.8))
        fig.update_layout(height=550)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    with st.expander("📊 Ver análisis de residuos"):
        
        df['Predicho'] = intercepto + pendiente * df['Pace']
        df['Residuo'] = df['PPG'] - df['Predicho']
        
        col_r1, col_r2 = st.columns(2)
        
        with col_r1:
            st.subheader("Tabla de residuos")
            df_res = df[['Temporada', 'Pace', 'PPG', 'Predicho', 'Residuo']].copy()
            st.dataframe(df_res.round(2), use_container_width=True)
        
        with col_r2:
            st.subheader("Gráfico de residuos")
            fig_res = px.bar(df, x='Temporada', y='Residuo',
                              title='Residuos del Modelo',
                              labels={'Residuo': 'Residuo (puntos)'},
                              template='plotly_dark')
            fig_res.update_layout(height=400)
            st.plotly_chart(fig_res, use_container_width=True)
        
        st.caption(f"""
        **Estadísticas de los residuos:**
        - Media: {df['Residuo'].mean():.4f}
        - Desviación estándar: {df['Residuo'].std():.4f}
        """)

# ==================== SECCIÓN 2: PREDICTOR INTERACTIVO ====================
else:
    
    with st.container():
        st.subheader("🔮 Predictor Interactivo")
        st.caption("💡 Modifica el valor del ritmo (posesiones por 48 min) para predecir los puntos por partido.")
        
        col_p1, col_p2 = st.columns([1, 2])
        
        with col_p1:
            pace_nuevo = st.slider(
                "Selecciona un valor de Pace (posesiones por 48 min):",
                min_value=float(df['Pace'].min()) - 3,
                max_value=float(df['Pace'].max()) + 3,
                value=float(df['Pace'].mean()),
                step=0.5,
                format="%.1f"
            )
            
            prediccion = intercepto + pendiente * pace_nuevo
            
            st.metric("📌 PPG estimado", f"{prediccion:.1f}")
            st.caption(f"Basado en {n} temporadas | R² = {r2:.3f}")
            
            # Mostrar ecuación actual
            st.info(f"**Ecuación:** PPG = {intercepto:.2f} + {pendiente:.4f} × Pace")
        
        with col_p2:
            # Mostrar la predicción en el gráfico
            df_pred = pd.DataFrame({
                'Pace': [pace_nuevo],
                'PPG': [prediccion],
                'Temporada': ['Predicción']
            })
            
            fig_pred = px.scatter(df, x='Pace', y='PPG', 
                                   text='Temporada',
                                   title=f'Predicción: Pace = {pace_nuevo:.1f} posesiones/48min → PPG = {prediccion:.1f}',
                                   labels={'Pace': 'Ritmo (Pace) - Posesiones por 48 min', 'PPG': 'Puntos por Partido'},
                                   template='plotly_dark')
            fig_pred.add_scatter(x=df_pred['Pace'], y=df_pred['PPG'], 
                                  mode='markers', marker=dict(size=20, color='red', symbol='star'),
                                  name='Predicción', text=df_pred['Temporada'])
            fig_pred.update_traces(textposition='top center')
            fig_pred.update_layout(height=400)
            st.plotly_chart(fig_pred, use_container_width=True)
    
    st.markdown("---")
    
    # Tabla comparativa de predicciones
    with st.expander("📊 Ver tabla comparativa de predicciones"):
        
        st.subheader("Predicciones para diferentes ritmos")
        
        valores_pace = [pace_min, pace_nuevo, pace_max]
        predicciones = [intercepto + pendiente * p for p in valores_pace]
        
        df_comparacion = pd.DataFrame({
            'Ritmo (Pace)': [f"{p:.1f}" for p in valores_pace],
            'PPG estimado': [f"{pred:.1f}" for pred in predicciones],
            'Contexto': ['Mínimo del período', 'Tu selección', 'Máximo del período']
        })
        
        st.dataframe(df_comparacion, use_container_width=True)

# ==================== TABLA DE DATOS OPCIONAL ====================
with st.expander("📋 Ver datos originales del período"):
    df_show = df[['Temporada', 'Pace', 'PPG']].copy()
    st.dataframe(df_show.round(2), use_container_width=True)
    
    csv = df_show.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar CSV", data=csv, 
                       file_name=f"regresion_{inicio}_a_{fin}.csv", 
                       mime="text/csv")

st.markdown("---")

# ==================== CONCLUSIÓN ====================
with st.container():
    st.subheader("💡 Conclusión del Modelo")
    
    if r2 > 0.7:
        st.success(f"""
        ✅ **El modelo tiene un poder explicativo muy alto (R² = {r2:.3f})**
        
        El **{r2*100:.1f}%** de la variación en los puntos por partido es explicada por el ritmo de juego.
        
        **Ecuación final:** PPG = {intercepto:.2f} + {pendiente:.4f} × Pace
        
        **Unidad:** Por cada posesión adicional por 48 minutos, los puntos aumentan en {pendiente:.2f}.
        
        ➡️ Esto confirma que **el ritmo es un predictor muy fuerte** de la anotación en la NBA.
        """)
    elif r2 > 0.4:
        st.info(f"""
        📊 **El modelo tiene un poder explicativo moderado (R² = {r2:.3f})**
        
        El **{r2*100:.1f}%** de la variación en los puntos es explicada por el ritmo de juego.
        
        **Ecuación final:** PPG = {intercepto:.2f} + {pendiente:.4f} × Pace
        
        **Unidad:** Por cada posesión adicional por 48 minutos, los puntos aumentan en {pendiente:.2f}.
        
        ➡️ El ritmo explica parte de la anotación, pero también influyen otros factores como la eficiencia de tiro.
        """)
    else:
        st.warning(f"""
        ⚠️ **El modelo tiene un poder explicativo bajo (R² = {r2:.3f})**
        
        Solo el **{r2*100:.1f}%** de la variación en los puntos es explicada por el ritmo de juego.
        
        **Ecuación final:** PPG = {intercepto:.2f} + {pendiente:.4f} × Pace
        
        **Unidad:** Por cada posesión adicional por 48 minutos, los puntos aumentan en {pendiente:.2f}.
        
        ➡️ Esto sugiere que el ritmo no es el principal factor; la eficiencia de tiro podría ser más importante.
        """)

st.markdown("---")

# ==================== NAVEGACIÓN ====================
col_n1, col_n2 = st.columns(2)
with col_n1:
    if st.button("◀ Volver a Contrastes", use_container_width=True):
        st.switch_page("pages/4Contrastes.py")
with col_n2:
    if st.button("🏠 Ir a Inicio", use_container_width=True):
        st.switch_page("app.py")

st.caption(f"📌 **Período:** {inicio} → {fin} | **n = {n}** temporadas | **R² = {r2:.3f}**")