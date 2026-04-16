import streamlit as st
from assets.styles.style import aplicar_estilos_globales
from modules.sidebar import mostrar_sidebar_secciones
from modules.navegacion import navegacion

st.set_page_config(page_title="Conclusión", layout="wide")

aplicar_estilos_globales()
mostrar_sidebar_secciones()

st.title("🎯 Conclusión General")
st.markdown(
    "Síntesis final del análisis sobre la relación entre el **ritmo de juego**, "
    "la **anotación** y la **eficiencia ofensiva** en la NBA entre 2013 y 2023."
)
st.divider()

with st.container(border=True):
    st.subheader("📌 Conclusión principal")
    st.markdown(
        """
        El análisis realizado pera NBA durante la última década **no puede explicarse por una sola causa**, sino por la combinación de dos procesos complementarios: un **aumento del ritmo de juego** y una **mejora sostenida en la eficiencia ofensiva**. En términos generales, los equipos no solo juegan más rápido que hace diez años, sino que además convierten mejor sus posesiones en puntos, especialmente en un contexto donde el tiro exterior y la selección de lanzamientos han adquirido un peso estratégico cada vez mayor.mite concluir que el incremento de la anotación en l

        Los resultados estadísticos muestran que existe una **relación positiva y significativa entre el Pace y los puntos por partido**, lo que confirma que un mayor número de posesiones tiende a traducirse en una producción ofensiva superior. Sin embargo, esta relación por sí sola no agota la explicación del fenómeno. El crecimiento simultáneo del **eFG%** indica que el aumento anotador también está asociado con una ofensiva más eficiente, mejor estructurada y más adaptada a las tendencias modernas del juego.

        En consecuencia, la evidencia respalda que la transformación ofensiva de la NBA entre 2013 y 2023 responde a una evolución integral del baloncesto: **se juega más rápido, pero también se juega mejor en términos de eficiencia**. Por tanto, el auge anotador reciente debe entenderse como el resultado conjunto del volumen de juego y de una mejora técnica y táctica en la forma de atacar.
        """
    )

with st.container(border=True):
    st.subheader("🧠 Interpretación final")
    st.info(
        """
        La pregunta central del proyecto era si el aumento en los puntos por partido se debía principalmente al ritmo o a la puntería. La respuesta más sólida, a la luz del análisis, es que **el ritmo impulsa el crecimiento de la anotación**, pero **la eficiencia explica por qué ese crecimiento se ha vuelto sostenible y tan marcado** en la NBA moderna.
        """
    )

with st.container(border=True):
    st.subheader("🏀 Cierre")
    st.success(
        """
        En definitiva, la década analizada evidencia un cambio estructural en el baloncesto profesional: la NBA moderna ha logrado anotar más porque combina **mayor velocidad**, **mejor toma de decisiones ofensivas** y **mayor efectividad en los tiros**, especialmente desde el perímetro.
        """
    )

# ==================== NAVEGACIÓN ====================
st.divider()
navegacion("Consultas", "Inicio")
