import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats
from modules.style import aplicar_estilos_globales
from modules.sidebar import mostrar_sidebar_secciones
from modules.navegacion import navegacion

st.set_page_config(page_title="Correlación NBA", layout="wide")
st.title("📉 Análisis de Correlación")
st.markdown("Mide la relación entre ritmo de juego, puntos por partido y eficiencia de tiro mediante coeficientes estadísticos.")
st.divider()

# ==================== BANNER CORRELACIÓN ====================
st.markdown(
    """
    <div style="
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2070');
        background-size: cover;
        background-position: center;
        height: 130px;
        border-radius: 10px;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        justify-content: center;
    ">
        <div style="text-align: center;">
            <span style="color: white; font-size: 1.6rem; font-weight: bold;">📐 PRUEBAS DE HIPÓTESIS</span>
            <br>
            <span style="color: white; font-size: 1rem;">t-Student · p-valor · Región Crítica</span>
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

df_raw = st.session_state['df_resumen'].copy()

def convertir_temporada(codigo):
    codigo_str = str(codigo)
    if len(codigo_str) == 4:
        return f"20{codigo_str[:2]}-{codigo_str[2:]}"
    return codigo_str

df_raw['Temporada'] = df_raw['season'].apply(convertir_temporada)
df_raw = df_raw.rename(columns={
    'avg_ppg': 'PPG', 'avg_pace': 'Pace', 'avg_efg': 'eFG%',
    'avg_fga': 'FGA', 'avg_3p': '3PM', 'avg_tov': 'TOV', 'avg_orb': 'ORB'
})

# ==================== INICIALIZAR ESTADO ====================
if 'seccion_correlacion' not in st.session_state:
    st.session_state.seccion_correlacion = 'coeficientes'

# ==================== FILTROS ====================
with st.container():
    st.subheader("🔍 Filtros de temporada")
    st.caption("💡 **Consejo:** Selecciona un rango amplio (ej: 2013-14 a 2022-23) para ver tendencias generales, o rangos cortos para analizar épocas específicas como la era del triple (2015-16 en adelante).")
    
    col_f1, col_f2 = st.columns(2)
    temps = df_raw['Temporada'].tolist()
    
    with col_f1:
        inicio = st.selectbox("📅 Temporada inicio", temps, index=0)
    with col_f2:
        idx = temps.index(inicio)
        fin = st.selectbox("📅 Temporada fin", temps[idx:], index=len(temps[idx:])-1)

idx_i, idx_f = temps.index(inicio), temps.index(fin)
df = df_raw.iloc[idx_i:idx_f+1].copy()
# ===== VALIDACIÓN (agregar aquí) =====
n = len(df)
if n < 4:
    st.warning(f"⚠️ **Temporadas insuficientes:** Seleccionaste solo {n} temporada(s). Para un análisis de correlación válido se necesitan al menos **4 temporadas**.")
    st.info("💡 **Sugerencia:** Amplía el rango de temporadas para obtener resultados estadísticamente significativos.")
    st.stop()
# ===== FIN VALIDACIÓN =====

st.markdown("---")
st.divider()

# ==================== SELECTOR DE VARIABLES ====================
with st.container():
    st.subheader("🎯 Selección de variables")
    st.caption("💡 **Concepto:** La **variable independiente (X)** es la causa o predictor. La **variable dependiente (Y)** es el efecto o lo que queremos explicar. Ejemplo: ¿El ritmo (X) influye en los puntos (Y)?")
    
    vars_dict = {
        'PPG': '🏀 Puntos por Partido',
        'Pace': '⚡ Ritmo de Juego',
        'eFG%': '🎯 Eficiencia de Tiro',
        'FGA': '📊 Tiros Intentados',
        '3PM': '🎯 Triples Anotados',
        'TOV': '⚠️ Pérdidas',
        'ORB': '🔄 Rebotes Ofensivos'
    }
    
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        st.markdown("**Variable Independiente (X - Causa)**")
        var_x = st.selectbox("Selecciona X", list(vars_dict.keys()), index=1, format_func=lambda x: vars_dict[x], label_visibility="collapsed")
    
    with col_v2:
        st.markdown("**Variable Dependiente (Y - Efecto)**")
        var_y = st.selectbox("Selecciona Y", list(vars_dict.keys()), index=0, format_func=lambda x: vars_dict[x], label_visibility="collapsed")

st.divider()
# ==================== BOTONES ARRIBA (como en exploración) ====================
with st.container():
    st.subheader("🎯 Análisis disponibles")
    
    col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns(5)
    
    with col_b1:
        if st.button("📊 Coeficientes", use_container_width=True):
            st.session_state.seccion_correlacion = 'coeficientes'
    with col_b2:
        if st.button("📈 Dispersión", use_container_width=True):
            st.session_state.seccion_correlacion = 'dispersion'
    with col_b3:
        if st.button("🔢 Matriz", use_container_width=True):
            st.session_state.seccion_correlacion = 'matriz'
    with col_b4:
        if st.button("📊 Rangos", use_container_width=True):
            st.session_state.seccion_correlacion = 'rangos'
    with col_b5:
        if st.button("🔄 Comparar", use_container_width=True):
            st.session_state.seccion_correlacion = 'comparar'

st.divider()
# ==================== CÁLCULOS BASE ====================
x, y = df[var_x], df[var_y]
n = len(df)

r_p, p_p = stats.pearsonr(x, y)
r_s, p_s = stats.spearmanr(x, y)
t_pearson = r_p * np.sqrt((n-2)/(1-r_p**2)) if abs(r_p) < 1 else 0

# Intervalo de confianza
z = np.arctanh(r_p)
se = 1 / np.sqrt(n - 3)
z_crit = stats.norm.ppf(0.975)
ci_low, ci_high = np.tanh(z - z_crit * se), np.tanh(z + z_crit * se)

# ==================== SECCIÓN 1: COEFICIENTES ====================
if st.session_state.seccion_correlacion == 'coeficientes':
    with st.container():
        st.subheader("📊 Coeficientes de Correlación")
        
        col_m1, col_m2 = st.columns(2)
        
        with col_m1:
            st.metric("📈 Pearson (r)", f"{r_p:.4f}")
            st.write(f"**t-statistic:** {t_pearson:.3f}")
            st.write(f"**p-valor:** {p_p:.4f}")
            st.write(f"**IC 95%:** [{ci_low:.4f}, {ci_high:.4f}]")
            if p_p < 0.05:
                st.success("✅ Correlación lineal **significativa** (p < 0.05)")
            else:
                st.warning("⚠️ Correlación lineal **no significativa** (p ≥ 0.05)")
            
            # Interpretación Pearson
            fuerza = "Muy Fuerte" if abs(r_p) >= 0.8 else "Fuerte" if abs(r_p) >= 0.6 else "Moderada" if abs(r_p) >= 0.4 else "Débil" if abs(r_p) >= 0.2 else "Muy Débil"
            st.info(f"📌 **Interpretación:** Correlación {fuerza}. {'Esto significa que cuando aumenta ' + vars_dict[var_x] + ', también aumenta ' + vars_dict[var_y] if r_p > 0 else 'Esto significa que cuando aumenta ' + vars_dict[var_x] + ', disminuye ' + vars_dict[var_y] if r_p < 0 else 'No hay relación lineal entre las variables.'}")
        
        with col_m2:
            st.metric("📊 Spearman (ρ)", f"{r_s:.4f}")
            st.write(f"**p-valor:** {p_s:.4f}")
            if p_s < 0.05:
                st.success("✅ Relación monótona **significativa** (p < 0.05)")
            else:
                st.warning("⚠️ Relación monótona **no significativa** (p ≥ 0.05)")
            
            fuerza_s = "Muy Fuerte" if abs(r_s) >= 0.8 else "Fuerte" if abs(r_s) >= 0.6 else "Moderada" if abs(r_s) >= 0.4 else "Débil" if abs(r_s) >= 0.2 else "Muy Débil"
            st.info(f"📌 **Interpretación:** Spearman mide tendencias monótonas (no solo lineales). Es {fuerza_s}, menos sensible a valores atípicos. {'Los rangos de las temporadas son consistentes entre ambas variables.' if abs(r_s) > 0.6 else 'Los rangos no siguen una tendencia clara.'}")

# ==================== SECCIÓN 2: DISPERSIÓN ====================
elif st.session_state.seccion_correlacion == 'dispersion':
    with st.container():
        st.subheader("🔍 Diagrama de Dispersión")
        
        fig = px.scatter(df, x=var_x, y=var_y, text='Temporada',
                         title=f'{vars_dict[var_x]} vs {vars_dict[var_y]} (r = {r_p:.3f})',
                         trendline="ols", trendline_color_override="yellow",
                         template='plotly_dark')
        fig.update_traces(textposition='top center', marker=dict(size=18, opacity=0.8))
        fig.update_layout(height=550)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info(f"📌 **Interpretación visual:** Los puntos {'se concentran alrededor de la línea' if abs(r_p) > 0.7 else 'están dispersos'}. La línea roja muestra la tendencia {'positiva' if r_p > 0 else 'negativa'}. En el período {inicio}→{fin} se observa {'una clara relación' if abs(r_p) > 0.6 else 'una relación moderada' if abs(r_p) > 0.4 else 'poca relación'} entre las variables.")

# ==================== SECCIÓN 3: MATRIZ ====================
elif st.session_state.seccion_correlacion == 'matriz':
    with st.container():
        st.subheader("🔢 Matriz de Correlación")
        st.caption("💡 **Qué observar:** Busca valores cercanos a +1 (rojo) o -1 (azul). Las correlaciones más fuertes indican qué variables están más relacionadas.")
        
        vars_matriz = ['PPG', 'Pace', 'eFG%', 'FGA', '3PM']
        corr_matrix = df[vars_matriz].corr()
        
        fig_heat = px.imshow(corr_matrix, text_auto=True, aspect="auto",
                             color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
                             title="Mapa de Calor de Correlaciones")
        fig_heat.update_layout(height=500)
        st.plotly_chart(fig_heat, use_container_width=True)
        
        # Encontrar correlación más fuerte
        max_corr = 0
        max_pair = ""
        for i in range(len(vars_matriz)):
            for j in range(i+1, len(vars_matriz)):
                if abs(corr_matrix.iloc[i, j]) > abs(max_corr):
                    max_corr = corr_matrix.iloc[i, j]
                    max_pair = f"{vars_matriz[i]} y {vars_matriz[j]}"
        
        st.info(f"📌 **Correlación más fuerte:** {max_pair} con r = {max_corr:.3f}. {'Esto tiene sentido porque...' if 'Pace' in max_pair and 'PPG' in max_pair else 'Esto indica una relación importante en el juego moderno.'}")

# ==================== SECCIÓN 4: RANGOS ====================
elif st.session_state.seccion_correlacion == 'rangos':
    with st.container():
        st.subheader("📊 Tabla de Rangos por Temporada")
        st.caption("💡 **Cómo leer:** Rango 1 = mayor valor. Si una temporada tiene rangos similares en X e Y, significa que ambas variables se comportan igual. Si la diferencia es grande, una variable destaca más que la otra.")
        
        df_rank = df[['Temporada', var_x, var_y]].copy()
        df_rank['Rango_X'] = df_rank[var_x].rank(ascending=False).astype(int)
        df_rank['Rango_Y'] = df_rank[var_y].rank(ascending=False).astype(int)
        df_rank['Diferencia'] = df_rank['Rango_X'] - df_rank['Rango_Y']
        
        st.dataframe(df_rank, use_container_width=True)
        
        mejor_temp = df_rank.loc[df_rank['Diferencia'].abs().idxmin()]
        peor_temp = df_rank.loc[df_rank['Diferencia'].abs().idxmax()]
        
        st.info(f"📌 **Interpretación:** La temporada más consistente es **{mejor_temp['Temporada']}** (diferencia de {mejor_temp['Diferencia']} puestos). La menos consistente es **{peor_temp['Temporada']}** (diferencia de {peor_temp['Diferencia']} puestos). Esto {'confirma la correlación de Spearman' if abs(r_s) > 0.6 else 'explica por qué Spearman no es tan alto'}.")

# ==================== SECCIÓN 5: COMPARAR ====================
elif st.session_state.seccion_correlacion == 'comparar':
    with st.container():
        st.subheader("🔄 Comparación entre Períodos")
        st.caption("💡 **Consejo:** Selecciona períodos con al menos 4-5 temporadas para obtener resultados significativos. Períodos muy cortos (2-3 temporadas) dan correlaciones engañosas.")
        
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.markdown("**Período 1**")
            p1_i = st.selectbox("Inicio", temps, index=0, key="p1i")
            # Limitar opciones de fin para asegurar mínimo 4 temporadas
            idx_p1_i = temps.index(p1_i)
            opciones_p1 = [t for t in temps[idx_p1_i:] if temps.index(t) >= idx_p1_i + 3]
            if len(opciones_p1) == 0:
                opciones_p1 = [temps[-1]]
            p1_f = st.selectbox("Fin", opciones_p1, index=min(len(opciones_p1)-1, 2), key="p1f")
        
        with col_c2:
            st.markdown("**Período 2**")
            p2_i = st.selectbox("Inicio", temps, index=max(0, len(temps)-5), key="p2i")
            idx_p2_i = temps.index(p2_i)
            opciones_p2 = [t for t in temps[idx_p2_i:] if temps.index(t) >= idx_p2_i + 3]
            if len(opciones_p2) == 0:
                opciones_p2 = [temps[-1]]
            p2_f = st.selectbox("Fin", opciones_p2, index=len(opciones_p2)-1, key="p2f")
        
        i1, f1 = temps.index(p1_i), temps.index(p1_f)
        i2, f2 = temps.index(p2_i), temps.index(p2_f)
        
        n1 = f1 - i1 + 1
        n2 = f2 - i2 + 1
        
        # Verificar tamaño mínimo
        if n1 < 4 or n2 < 4:
            st.warning(f"⚠️ **Períodos muy cortos:** Período 1 tiene {n1} temporadas, Período 2 tiene {n2} temporadas. Para correlaciones confiables se recomiendan al menos 4 temporadas por período.")
            
            if n1 >= 2 and n2 >= 2:
                r1, _ = stats.pearsonr(df_raw.iloc[i1:f1+1][var_x], df_raw.iloc[i1:f1+1][var_y])
                r2, _ = stats.pearsonr(df_raw.iloc[i2:f2+1][var_x], df_raw.iloc[i2:f2+1][var_y])
                
                col_r1, col_r2, col_r3 = st.columns(3)
                col_r1.metric(f"{p1_i} → {p1_f} ({n1} temps)", f"{r1:.3f}")
                col_r2.metric(f"{p2_i} → {p2_f} ({n2} temps)", f"{r2:.3f}")
                col_r3.metric("Diferencia", f"{r2-r1:+.3f}")
                
                st.warning(f"⚠️ **Precaución:** Con solo {n1} y {n2} temporadas, estos resultados pueden no ser representativos. Amplía los rangos para obtener conclusiones más sólidas.")
        else:
            # Cálculo normal con períodos suficientes
            r1, p1 = stats.pearsonr(df_raw.iloc[i1:f1+1][var_x], df_raw.iloc[i1:f1+1][var_y])
            r2, p2 = stats.pearsonr(df_raw.iloc[i2:f2+1][var_x], df_raw.iloc[i2:f2+1][var_y])
            
            col_r1, col_r2, col_r3 = st.columns(3)
            col_r1.metric(f"{p1_i} → {p1_f} ({n1} temps)", f"{r1:.3f}")
            col_r2.metric(f"{p2_i} → {p2_f} ({n2} temps)", f"{r2:.3f}")
            col_r3.metric("Diferencia", f"{r2-r1:+.3f}", delta="Aumentó" if r2 > r1 else "Disminuyó")
            
            # Gráfico de barras comparativo
            fig_comp = go.Figure()
            fig_comp.add_trace(go.Bar(
                x=[f"{p1_i}\n→\n{p1_f}", f"{p2_i}\n→\n{p2_f}"],
                y=[r1, r2],
                text=[f"{r1:.3f}", f"{r2:.3f}"],
                textposition='auto',
                marker_color=['#636efa', '#ef553b']
            ))
            fig_comp.update_layout(
                title=f"Comparación de Correlaciones: {vars_dict[var_x]} vs {vars_dict[var_y]}",
                yaxis_title="Coeficiente de Correlación (r)",
                yaxis_range=[-1, 1],
                template='plotly_dark',
                height=400
            )
            st.plotly_chart(fig_comp, use_container_width=True)
            
            # Interpretación con contexto
            if abs(r2 - r1) > 0.2:
                st.info(f"📌 **Interpretación:** La correlación {'aumentó' if r2 > r1 else 'disminuyó'} significativamente en {abs(r2-r1):.3f} puntos. Esto sugiere que la relación entre {vars_dict[var_x]} y {vars_dict[var_y]} se ha {'fortalecido' if r2 > r1 else 'debilitado'} en la segunda época.")
            else:
                st.info(f"📌 **Interpretación:** La correlación se mantiene estable (diferencia de {abs(r2-r1):.3f}). La relación entre {vars_dict[var_x]} y {vars_dict[var_y]} es consistente a lo largo del tiempo.")
            
            # Mostrar significancia
            st.caption(f"Período 1 p-valor: {p1:.4f} | Período 2 p-valor: {p2:.4f}")
# ==================== TABLA COMPLETA (siempre visible al final) ====================
with st.expander("📋 Ver tabla completa de datos"):
    df_show = df[['Temporada', 'Pace', 'PPG', 'eFG%', 'FGA', '3PM']].copy()
    st.dataframe(df_show.round(2), use_container_width=True)
    
    csv = df_show.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar CSV", data=csv, file_name=f"correlacion_{inicio}_a_{fin}.csv", mime="text/csv")

st.divider()

# ==================== NAVEGACIÓN ====================
navegacion("Exploración", "Contrastes")
