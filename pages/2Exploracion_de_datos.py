import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from assets.styles.style import aplicar_estilos_globales
from modules.sidebar import mostrar_sidebar_secciones
from modules.navegacion import navegacion

st.set_page_config(page_title="Exploración NBA", layout="wide")
st.title("📊 Exploración de Datos NBA (2013-2023)")
st.divider()

st.markdown(
    """
    <div style="
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1504450758481-7338eba7524a?q=80&w=2069');
        background-size: cover;
        background-position: center;
        height: 120px;
        border-radius: 10px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
    ">
        <div style="text-align: center;">
            <span style="color: white; font-size: 1.5rem; font-weight: bold;">📊 EVOLUCIÓN HISTÓRICA</span>
            <br>
            <span style="color: white;">Pace · PPG · eFG% (2013-2023)</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Aplicar estilos globales
aplicar_estilos_globales()

# Mostrar sidebar
mostrar_sidebar_secciones()

# ==================== CARGA DE DATOS ====================
if 'df_resumen' not in st.session_state:
    from modules.database import get_resumen_temporadas
    st.session_state['df_resumen'] = get_resumen_temporadas()

# Preparar datos
df_raw = st.session_state['df_resumen'].copy()

def convertir_temporada(codigo):
    codigo_str = str(codigo)
    if len(codigo_str) == 4:
        inicio = int(codigo_str[:2])
        fin = int(codigo_str[2:])
        return f"20{inicio:02d}-{fin:02d}"
    return codigo_str

df_raw['Temporada'] = df_raw['season'].apply(convertir_temporada)
df_raw['Season_Num'] = df_raw['season']
df_raw = df_raw.sort_values('Season_Num')

df_raw = df_raw.rename(columns={
    'avg_ppg': 'PPG',
    'avg_pace': 'Pace',
    'avg_efg': 'eFG%',
    'avg_fga': 'FGA',
    'avg_3p': '3PM',
    'avg_tov': 'TOV',
    'avg_orb': 'ORB'
})

# ==================== INICIALIZAR ESTADO ====================
if 'mostrar_detalles' not in st.session_state:
    st.session_state.mostrar_detalles = False
if 'grafico_seleccionado' not in st.session_state:
    st.session_state.grafico_seleccionado = 'PPG'
if 'mostrar_comparacion_triple' not in st.session_state:
    st.session_state.mostrar_comparacion_triple = False

# ==================== FILTROS ====================
with st.container():
    st.subheader("🔍 Filtros de Exploración")
    
    temporadas_disponibles = df_raw['Temporada'].tolist()
    
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        temporada_inicio = st.selectbox(
            "📅 Temporada de inicio",
            options=temporadas_disponibles,
            index=0
        )
    
    with col_f2:
        idx_inicio = temporadas_disponibles.index(temporada_inicio)
        temporadas_fin_disponibles = temporadas_disponibles[idx_inicio:]
        temporada_fin = st.selectbox(
            "📅 Temporada de fin",
            options=temporadas_fin_disponibles,
            index=len(temporadas_fin_disponibles) - 1
        )
    
    col_b1, col_b2, col_b3 = st.columns(3)
    
    with col_b1:
        if st.button("🔄 Resetear filtros", use_container_width=True):
            st.rerun()
    with col_b2:
        mostrar_tabla = st.toggle("📋 Mostrar tabla", value=False)
    with col_b3:
        st.session_state.mostrar_detalles = st.toggle("🔧 Ver detalles técnicos", value=st.session_state.mostrar_detalles)

st.divider()

# ==================== APLICAR FILTROS ====================
idx_inicio = temporadas_disponibles.index(temporada_inicio)
idx_fin = temporadas_disponibles.index(temporada_fin)
df_filtrado = df_raw.iloc[idx_inicio:idx_fin+1].copy()

# Métricas
pace_inicio = df_filtrado['Pace'].iloc[0]
pace_fin = df_filtrado['Pace'].iloc[-1]
cambio_pace = ((pace_fin - pace_inicio) / pace_inicio) * 100 if pace_inicio != 0 else 0

ppg_inicio = df_filtrado['PPG'].iloc[0]
ppg_fin = df_filtrado['PPG'].iloc[-1]
cambio_ppg = ((ppg_fin - ppg_inicio) / ppg_inicio) * 100 if ppg_inicio != 0 else 0

efg_inicio = df_filtrado['eFG%'].iloc[0]
efg_fin = df_filtrado['eFG%'].iloc[-1]
cambio_efg = ((efg_fin - efg_inicio) / efg_inicio) * 100 if efg_inicio != 0 else 0

# ==================== MÉTRICAS ====================
with st.container():
    st.subheader(f"📊 Resumen: {temporada_inicio} → {temporada_fin}")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    
    with col_m1:
        st.metric("⚡ Ritmo (Pace)", f"{pace_fin:.1f}", delta=f"{cambio_pace:+.1f}%")
        if st.session_state.mostrar_detalles:
            st.caption(f"Inicio: {pace_inicio:.1f}")
    with col_m2:
        st.metric("🏀 Puntos (PPG)", f"{ppg_fin:.1f}", delta=f"{cambio_ppg:+.1f}%")
        if st.session_state.mostrar_detalles:
            st.caption(f"Inicio: {ppg_inicio:.1f}")
    with col_m3:
        st.metric("🎯 Eficiencia (eFG%)", f"{efg_fin:.3f}", delta=f"{cambio_efg:+.2f}%")
        if st.session_state.mostrar_detalles:
            st.caption(f"Inicio: {efg_inicio:.3f}")

st.divider()

# ==================== BOTONES DE GRÁFICOS ====================
with st.container():
    st.subheader("📈 Selecciona el gráfico a visualizar")
    
    col_g1, col_g2, col_g3, col_g4 = st.columns(4)
    
    with col_g1:
        if st.button("🏀 Puntos (PPG)", use_container_width=True):
            st.session_state.grafico_seleccionado = 'PPG'
            st.session_state.mostrar_comparacion_triple = False
    with col_g2:
        if st.button("⚡ Ritmo (Pace)", use_container_width=True):
            st.session_state.grafico_seleccionado = 'Pace'
            st.session_state.mostrar_comparacion_triple = False
    with col_g3:
        if st.button("🎯 Eficiencia (eFG%)", use_container_width=True):
            st.session_state.grafico_seleccionado = 'eFG%'
            st.session_state.mostrar_comparacion_triple = False
    with col_g4:
        if st.button("📊 Comparación Triple", use_container_width=True):
            st.session_state.mostrar_comparacion_triple = True
    
    st.divider()

# ==================== GRÁFICO PRINCIPAL ====================
if not st.session_state.mostrar_comparacion_triple:
    with st.container():
        variable_grafico = st.session_state.grafico_seleccionado
        colores = {'PPG': '#ef553b', 'Pace': '#636efa', 'eFG%': '#00cc96'}
        titulos = {'PPG': 'Puntos por Partido', 'Pace': 'Ritmo de Juego', 'eFG%': 'Eficiencia de Tiro'}
        
        fig = px.line(df_filtrado, x='Temporada', y=variable_grafico,
                      title=f'Evolución de {titulos[variable_grafico]} ({temporada_inicio} a {temporada_fin})',
                      markers=True, template='plotly_dark')
        fig.update_traces(line_color=colores[variable_grafico], line_width=3, marker=dict(size=12))
        fig.update_layout(xaxis_tickangle=-45, height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        if variable_grafico == 'PPG':
            st.info(f"📌 Puntos: {ppg_inicio:.1f} → {ppg_fin:.1f} ({cambio_ppg:+.1f}%)")
        elif variable_grafico == 'Pace':
            st.info(f"📌 Ritmo: {pace_inicio:.1f} → {pace_fin:.1f} ({cambio_pace:+.1f}%)")
        else:
            st.info(f"📌 Eficiencia: {efg_inicio:.3f} → {efg_fin:.3f} ({cambio_efg:+.2f}%)")

# ==================== COMPARACIÓN TRIPLE ====================
else:
    with st.container():
        st.subheader("📊 Comparación Triple")
        
        fig_triple = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_triple.add_trace(go.Scatter(x=df_filtrado['Temporada'], y=df_filtrado['PPG'],
                                        name='🏀 PPG', line=dict(color='#ef553b', width=3)),
                             secondary_y=False)
        fig_triple.add_trace(go.Scatter(x=df_filtrado['Temporada'], y=df_filtrado['Pace'],
                                        name='⚡ Pace', line=dict(color='#636efa', width=3, dash='dot')),
                             secondary_y=True)
        
        efg_scaled = df_filtrado['eFG%'] * 200
        fig_triple.add_trace(go.Scatter(x=df_filtrado['Temporada'], y=efg_scaled,
                                        name='🎯 eFG% x200', line=dict(color='#00cc96', width=3, dash='dash')),
                             secondary_y=False)
        
        fig_triple.update_layout(title='Evolución Comparada', xaxis_tickangle=-45, height=500, template='plotly_dark')
        fig_triple.update_yaxes(title_text="PPG / eFG% escalado", secondary_y=False)
        fig_triple.update_yaxes(title_text="Pace", secondary_y=True)
        st.plotly_chart(fig_triple, use_container_width=True)
        
        st.info("📌 Los tres indicadores han crecido durante la década.")
        
        if st.button("◀ Volver", use_container_width=True):
            st.session_state.mostrar_comparacion_triple = False
            st.rerun()

st.divider()

# ==================== TABLA OPCIONAL ====================
if mostrar_tabla:
    with st.container():
        st.subheader("📋 Datos por Temporada")
        df_tabla = df_filtrado[['Temporada', 'Pace', 'PPG', 'eFG%', 'FGA', '3PM']].copy()
        df_tabla = df_tabla.rename(columns={'Temporada': '📅 Temporada', 'Pace': '⚡ Ritmo',
                                            'PPG': '🏀 Puntos', 'eFG%': '🎯 Eficiencia',
                                            'FGA': '📊 Tiros', '3PM': '🎯 Triples'})
        st.dataframe(df_tabla.round(2), use_container_width=True, height=400)
        
        csv = df_tabla.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar CSV", data=csv, file_name=f"datos_nba_{temporada_inicio}_a_{temporada_fin}.csv",
                          mime="text/csv", use_container_width=True)
    st.divider()



# ==================== CONCLUSIÓN Y NAVEGACIÓN ====================
st.success("💡 El aumento en los puntos se debe a **mayor ritmo** y **mejor eficiencia**.")
st.info(f"📌 Período: {temporada_inicio} → {temporada_fin} | Temporadas: {len(df_filtrado)}")

st.divider()
navegacion("Teoría", "Correlación")
