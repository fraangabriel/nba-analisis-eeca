import streamlit as st
from modules.database import get_resumen_temporadas
from assets.styles.style import aplicar_estilos_globales  
from modules.sidebar import mostrar_sidebar_inicio

st.set_page_config(
    page_title="NBA Analytics | Velocidad vs Eficiencia",
    page_icon="🏀",
    layout="wide"
)

# Aplicar estilos globales
aplicar_estilos_globales()  
mostrar_sidebar_inicio()

# ==================== CONTENIDO PRINCIPAL ====================
st.title("🏀 Velocidad vs Eficiencia: La Década que Cambió la NBA")
st.markdown("*Análisis estadístico de la transformación de la NBA (2013-2023)*")
st.divider()


# ==================== BANNER HORIZONTAL ====================
st.markdown(
    """
    <div style="
        background-image: url('https://images.unsplash.com/photo-1546519638-68e109498ffc?q=80&w=2090');
        background-size: cover;
        background-position: center 30%;
        height: 150px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    ">
    </div>
    """,
    unsafe_allow_html=True
)

# Descripción del Proyecto
with st.container(border=True):
    st.markdown("## 📋 Descripción del Proyecto")
    st.markdown("""
    Este proyecto estudia cómo ha cambiado la forma de jugar y de anotar en la NBA desde el año 2013 hasta el 2023. 
    El estudio se enfoca en ver si los equipos anotan más puntos porque ahora juegan más rápido o porque han mejorado su puntería, 
    explicando de forma clara por qué los partidos de hoy son tan diferentes a los de hace diez años.
    """)

st.divider()

# Planteamiento del Problema
with st.container(border=True):
    st.markdown("## 📑 Planteamiento del Problema")
    st.markdown("""
    En los últimos años, la NBA ha vivido una transformación radical: el ritmo es más vertiginoso, 
    el volumen de triples se ha disparado y los marcadores son cada vez más altos. 
    
    **Pregunta central:** ¿El aumento en los puntos por partido se debe a un mayor volumen de posesiones o a una mejora sustancial en la puntería?
    
    Este trabajo busca responder estas interrogantes mediante un análisis estadístico riguroso de 10 temporadas completas.
    """)

st.divider()

# Objetivo General
with st.container(border=True):
    st.markdown("## 🎯 Objetivo General")
    st.markdown("""
    > Analizar la relación entre el incremento del ritmo de juego (Pace) y la anotación en la NBA durante la última década, 
    > evaluando el papel fundamental que ha desempeñado la efectividad de tiro en esta evolución.
    """)

st.divider()

# Objetivos Específicos
st.markdown("## 📌 Objetivos Específicos")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("### 📊 Objetivo 1")
        st.markdown("**Monitorear la evolución histórica**")
        st.markdown("Documentar el comportamiento del ritmo, los puntos por partido y la efectividad de tiro (eFG%) temporada tras temporada para identificar patrones de cambio.")
        if st.button("📈 Ver evolución histórica →", use_container_width=True, key="btn_obj1"):
            st.switch_page("pages/2Exploracion_de_datos.py")
    
    st.divider()
    
    with st.container(border=True):
        st.markdown("### 📈 Objetivo 2")
        st.markdown("**Validar la correlación ritmo-anotación**")
        st.markdown("Determinar estadísticamente si el aumento en la velocidad de las posesiones se traduce de manera directa en un incremento proporcional del marcador.")
        if st.button("📉 Ver correlación →", use_container_width=True, key="btn_obj2"):
            st.switch_page("pages/3Correlacion.py")

with col2:
    with st.container(border=True):
        st.markdown("### 🎯 Objetivo 3")
        st.markdown("**Evaluar el impacto en la precisión**")
        st.markdown("Analizar si jugar a una mayor velocidad beneficia o perjudica la efectividad de los tiros de campo de los equipos.")
        if st.button("📐 Ver impacto en precisión →", use_container_width=True, key="btn_obj3"):
            st.switch_page("pages/4Contrastes.py")
    
    st.divider()
    
    with st.container(border=True):
        st.markdown("### 🔮 Objetivo 4")
        st.markdown("**Definir el factor de crecimiento**")
        st.markdown("Identificar si el auge anotador de la última década es impulsado primordialmente por un mayor volumen de jugadas o por una mejora técnica en la puntería.")
        if st.button("🧪 Ver factor de crecimiento →", use_container_width=True, key="btn_obj4"):
            st.switch_page("pages/5Regresión.py")

st.divider()

# Metodología
with st.expander("📊 Ver metodología del análisis"):
    st.markdown("""
    ### Enfoque Estadístico
    
    | Objetivo | Método | Página |
    |----------|--------|--------|
    | Evolución histórica | Análisis temporal con gráficos de línea | Exploración |
    | Correlación ritmo-anotación | Coeficientes de Pearson y Spearman | Correlación |
    | Impacto en precisión | Contraste de hipótesis (t-Student) | Pruebas de Hipótesis |
    | Factor de crecimiento | Regresión lineal simple (R²) | Modelo de Regresión |
    
    ### Variable Principal
    
    - **Pace (Ritmo):** Número de posesiones por cada 48 minutos de juego
    - **PPG (Puntos):** Puntos por partido
    - **eFG% (Eficiencia):** Effective Field Goal Percentage
    """)

st.divider()

# Respuesta Esperada
st.info("""
💡 **Al final del análisis, este dashboard responderá:**
- ¿El ritmo de juego aumentó significativamente en la última década?
- ¿Los puntos por partido crecieron por el ritmo o por la eficiencia?
- ¿Qué porcentaje de la variación en los puntos explica el ritmo (R²)?
- ¿Jugar más rápido afecta la efectividad de tiro?
""")

st.success("👈 **Usa el menú lateral** para explorar cada objetivo específico del estudio.")

# ==================== PIE DE PÁGINA ====================
st.divider()
st.caption("🏀 Universidad Central de Venezuela - Escuela de Estadística y Ciencias Actuariales")
st.caption("📊 Proyecto de Análisis NBA 2013-2023 | Velocidad vs Eficiencia")

st.divider()
if st.button("Ir a Teoría ➡️", use_container_width=True):
                st.switch_page("pages/1Teoría.py")
