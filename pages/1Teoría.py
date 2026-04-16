import streamlit as st
from modules.style import aplicar_estilos_globales
from modules.sidebar import mostrar_sidebar

st.set_page_config(
    page_title="Teoría | NBA Analytics",
    page_icon="📖",
    layout="wide"
)

# Aplicar estilos globales
aplicar_estilos_globales()

# Mostrar sidebar
mostrar_sidebar()

# ==================== INICIALIZAR ESTADO ====================
if 'seccion_teoria' not in st.session_state:
    st.session_state.seccion_teoria = 'objetivos'

# ==================== TÍTULO PRINCIPAL ====================
st.title("📖 Fundamentos Teóricos de la Investigación")
st.markdown("*Marco conceptual y metodológico del estudio*")
st.markdown("---")

# ==================== BOTONES DE NAVEGACIÓN INTERNA ====================
with st.container():
    st.markdown("### 📌 Navegación rápida")
    
    col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns(5)
    
    with col_b1:
        if st.button("🎯 Objetivos", use_container_width=True, key="teo_obj"):
            st.session_state.seccion_teoria = 'objetivos'
    
    with col_b2:
        if st.button("📑 Problema", use_container_width=True, key="teo_prob"):
            st.session_state.seccion_teoria = 'problema'
    
    with col_b3:
        if st.button("⚠️ Limitantes", use_container_width=True, key="teo_lim"):
            st.session_state.seccion_teoria = 'limitantes'
    
    with col_b4:
        if st.button("📊 Metodología", use_container_width=True, key="teo_met"):
            st.session_state.seccion_teoria = 'metodologia'
    
    with col_b5:
        if st.button("🔧 Datos", use_container_width=True, key="teo_dat"):
            st.session_state.seccion_teoria = 'datos'

st.markdown("---")

# ==================== SECCIÓN 1: OBJETIVOS ====================
if st.session_state.seccion_teoria == 'objetivos':
    with st.container(border=True):
        st.markdown("## 🎯 Objetivos del Estudio")
        
        st.markdown("### Objetivo General")
        st.markdown("""
        > Analizar la relación entre el incremento del ritmo de juego (Pace) y la anotación en la NBA durante la última década, 
        > evaluando el papel fundamental que ha desempeñado la efectividad de tiro en esta evolución.
        """)
        
        st.markdown("### Objetivos Específicos")
        st.markdown("""
        1. **Monitorear la evolución histórica:** Documentar el comportamiento del ritmo, los puntos por partido y la efectividad de tiro (eFG%) temporada tras temporada para identificar patrones de cambio.
        
        2. **Validar la correlación ritmo-anotación:** Determinar estadísticamente si el aumento en la velocidad de las posesiones se traduce de manera directa en un incremento proporcional del marcador.
        
        3. **Evaluar el impacto en la precisión:** Analizar si jugar a una mayor velocidad beneficia o perjudica la efectividad de los tiros de campo de los equipos.
        
        4. **Definir el factor de crecimiento:** Identificar si el auge anotador de la última década es impulsado primordialmente por un mayor volumen de jugadas o por una mejora técnica en la puntería.
        """)

# ==================== SECCIÓN 2: PLANTEAMIENTO DEL PROBLEMA ====================
elif st.session_state.seccion_teoria == 'problema':
    with st.container(border=True):
        st.markdown("## 📑 Planteamiento del Problema")
        st.markdown("""
        ### Situación Actual
        
        En los últimos años, la NBA ha vivido una transformación radical: el ritmo es más vertiginoso, 
        el volumen de triples se ha disparado y los marcadores son cada vez más altos. 
        
        ### Pregunta Central de Investigación
        
        **¿El aumento en los puntos por partido se debe a un mayor volumen de posesiones o a una mejora sustancial en la puntería?**
        
        ### Hipótesis de Trabajo
        
        - **H₁:** El ritmo de juego (Pace) tiene una correlación positiva y significativa con los puntos por partido (PPG).
        - **H₂:** La eficiencia de tiro (eFG%) también ha mejorado durante la década, contribuyendo al aumento anotador.
        - **H₃:** El ritmo de juego explica un porcentaje significativo de la variación en los puntos (R² > 0.7).
        """)

# ==================== SECCIÓN 3: LIMITANTES ====================
elif st.session_state.seccion_teoria == 'limitantes':
    with st.container(border=True):
        st.markdown("## ⚠️ Limitantes del Estudio")
        st.markdown("""
        | Limitante | Descripción |
        |-----------|-------------|
        | **Período de análisis** | Solo se analizan 10 temporadas (2013-14 a 2022-23), no se consideran temporadas anteriores ni posteriores |
        | **Datos agregados** | Se utilizan promedios por temporada, no datos a nivel de partido individual |
        | **Variables incluidas** | El estudio se enfoca en Pace, PPG y eFG%, excluyendo otras variables como defensa, lesiones, etc. |
        | **Generalización** | Los resultados aplican a la NBA en su conjunto, no a equipos o jugadores específicos |
        | **Causalidad** | La correlación no implica causalidad directa; pueden existir variables no consideradas |
        """)

# ==================== SECCIÓN 4: METODOLOGÍA ====================
elif st.session_state.seccion_teoria == 'metodologia':
    with st.container(border=True):
        st.markdown("## 📊 Metodología de Investigación")
        
        st.markdown("""
        ### Tipo de Investigación
        
        **Cuantitativa - Correlacional y Explicativa**
        
        ### Variables del Estudio
        
        | Tipo | Variable | Nombre Técnico | Unidad de Medida |
        |------|----------|----------------|------------------|
        | Independiente (X) | Ritmo de juego | Pace | Posesiones por 48 minutos |
        | Dependiente (Y) | Puntos por partido | PPG | Puntos |
        | Secundaria | Eficiencia de tiro | eFG% | Porcentaje ajustado |
        
        ### Métodos Estadísticos Aplicados
        
        | Objetivo | Método | Justificación |
        |----------|--------|---------------|
        | Evolución histórica | Análisis temporal con gráficos de línea | Visualizar tendencias a lo largo del tiempo |
        | Correlación | Coeficiente de Pearson (r) y Spearman (ρ) | Medir fuerza y dirección de la relación lineal |
        | Significancia | Contraste de hipótesis (t-Student) | Validar si la relación es estadísticamente significativa (α=0.05) |
        | Predicción | Regresión lineal simple | Cuantificar el poder explicativo (R²) y predecir valores |
        """)

# ==================== SECCIÓN 5: PROCESAMIENTO DE DATOS ====================
# ==================== SECCIÓN 5: PROCESAMIENTO DE DATOS ====================
else:
    with st.container(border=True):
        st.markdown("## 🔧 Procesamiento de Datos")
        
        st.markdown("""
        ### Fuente de Datos
        
        Los datos fueron extraídos de una base de datos SQLite que contiene información de:
        - **Partidos:** Resultados, fechas, equipos participantes
        - **Estadísticas de equipos:** Puntos, tiros, rebotes, pérdidas, etc.
        - **Temporadas:** Período 2013-14 a 2022-23
        
        ### Normalización y Limpieza
        
        | Paso | Descripción |
        |------|-------------|
        | **1. Extracción** | Consulta SQL para agregar estadísticas por temporada |
        | **2. Manejo de nulos** | Uso de `NULLIF()` para evitar división por cero en cálculos de porcentajes |
        | **3. Agregación** | Promedio de estadísticas por temporada (10 registros finales) |
        | **4. Transformación** | Conversión de códigos de temporada (1516 → "2015-16") |
        
        ### Variables Calculadas
        """)
        
        # Mostrar código SQL como texto plano (sin ejecutar)
        st.code("""
        -- Puntos por partido (PPG)
        AVG((ee."3P" * 3) + (ee.FG - ee."3P") * 2 + ee.FT) AS avg_ppg
        
        -- Ritmo (Pace) - Fórmula estándar NBA
        AVG(ee.FGA + (0.44 * ee.FTA) - ee.ORB + ee.TOV) AS avg_pace
        
        -- Eficiencia de tiro (eFG%)
        AVG((ee.FG + 0.5 * ee."3P") / NULLIF(ee.FGA, 0)) AS avg_efg
        """, language="sql")
        
