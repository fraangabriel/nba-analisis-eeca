import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
from modules.style import aplicar_estilos_globales
from modules.sidebar import mostrar_sidebar_secciones
from modules.navegacion import navegacion

st.set_page_config(page_title="Consultas SQL (SQLite)", layout="wide")
aplicar_estilos_globales()
mostrar_sidebar_secciones()

st.title("🖥️ Consultas SQL")
st.write("Consulta y exploración de la **Version Normalizada** de la **Base de Datos** usando **SQLite**.")
PARQUET_DIR = Path("Data parquet/Version_Normalizada")

@st.cache_resource
def get_sqlite_connection(path: Path):
    con = sqlite3.connect(":memory:", check_same_thread=False)
    files = list(path.glob("*.parquet"))
    for f in files:
        pd.read_parquet(f).to_sql(f.stem, con, index=False, if_exists='replace')
    return con, sorted([f.stem for f in files])

con, table_names = get_sqlite_connection(PARQUET_DIR)

col_info, col_query = st.columns([1, 2], gap="large")

with col_info:
    with st.container(border=True):
        selected = st.selectbox("Explorar tabla", table_names)
        n = st.slider("Filas", 5, 500, 15)
        
        df_preview = pd.read_sql_query(f"SELECT * FROM {selected} LIMIT {n}", con)
        st.dataframe(df_preview, use_container_width=True, height=300)
        
        st.divider()
        st.subheader(f"🔎 Esquema de `{selected}`")
        df_schema = pd.read_sql_query(f"PRAGMA table_info({selected})", con)
        st.dataframe(df_schema[['name', 'type']], use_container_width=True)

with col_query:
    with st.container(border=True):
        st.subheader("🧾 Ejecutar consulta SQL")
        
        # 1. Diccionario de mapeo con nombres, archivos y sus enunciados detallados
        queries_info = {
            "🏀 1: La Red de Asistencias y el Dúo Más Prolífico": {
                "archivo": "Querie 1.sql",
                "enunciado": """Identifica el "dúo dinámico" de cada temporada (desde 2013-2014 hasta 2022-2023). Encuentra, por cada año, al equipo que tuvo al jugador líder en asistencias totales de la liga y, simultáneamente, a un compañero de equipo que haya estado en el Top 10 de anotadores totales de esa misma campaña. Para cada temporada que cumpla la condición, muestra el año, el nombre del equipo, el nombre del jugador "Armador" (asistencias), el nombre del jugador "Anotador" (puntos), y el total combinado de puntos y asistencias que sumaron entre ambos durante esa temporada regular."""
            },
            "🔄 2: Rendimiento Ofensivo en 'Back-to-Backs'": {
                "archivo": "Querie 2.sql",
                "enunciado": """Evalúa el impacto de jugar en noches consecutivas (Back-to-Back). Calcula para cada equipo el porcentaje de victorias y el promedio de Puntos a Favor (PTS) en partidos que se jugaron exactamente al día siguiente de otro encuentro de la misma franquicia. Compáralo contra su rendimiento en partidos jugados con 2 o más días de descanso acumulado. Muestra el equipo, el porcentaje de victorias con descanso, el porcentaje de victorias en Back-to-Back y la diferencia absoluta entre ambos porcentajes. Muestra solo el Top 5 de equipos más perjudicados por el Back-to-Back, basándote en la caída de su porcentaje de victorias."""
            },
            "🔥 3: Rachas de Triples-Dobles e Impacto en Victoria": {
                "archivo": "Querie 3.sql",
                "enunciado": """Identifica a los jugadores que hayan registrado una racha de al menos tres partidos consecutivos (ordenados cronológicamente por fecha de juego para su respectivo equipo) logrando un "triple-doble" (doble dígito en Puntos, Rebotes y Asistencias). Para la racha más larga de cada jugador identificado, muestra su nombre, la temporada en que ocurrió, la longitud de la racha (cantidad de partidos), la fecha de inicio, la fecha de fin y el margen de victoria (Plus/Minus general del partido) promedio del equipo durante esos encuentros específicos."""
            },
            "📊 4: Brecha Estadística entre Titulares y Suplentes": {
                "archivo": "Querie 4.sql",
                "enunciado": """Para las estadísticas de Puntos (PTS), Asistencias (AST) y Rebotes Totales (TREB), determina cuál es la métrica que presenta la mayor brecha porcentual entre el grupo de jugadores titulares y el grupo de suplentes, usando el promedio por partido de la temporada más reciente disponible (2022-2023). Un jugador se considera titular en un partido si la columna correspondiente indica que inició el juego. Muestra el nombre de la estadística, el valor promedio del grupo titular, el valor promedio del grupo suplente y la brecha porcentual calculada."""
            },
            "🏹 5: La Revolución del Triple y Evolución del Juego": {
                "archivo": "Querie 5.sql",
                "enunciado": """El baloncesto ha experimentado un cambio radical hacia el tiro exterior a lo largo de los años. Para cada equipo, determina el porcentaje de sus puntos totales que provinieron de tiros de tres puntos (sabiendo que cada tiro encestado vale 3 puntos) en la temporada más antigua registrada para ese equipo y compáralo con el mismo porcentaje en su temporada más reciente. Muestra el nombre del equipo, la temporada inicial, el porcentaje inicial de dependencia del triple, la temporada más reciente, el porcentaje final y el crecimiento porcentual absoluto entre ambas. Ordena los resultados de mayor a menor según este crecimiento. Excluye a los equipos que tengan menos de 5 años de diferencia entre su primer y último registro."""
            }
        }

        # 2. Selectbox principal
        opcion_elegida = st.selectbox(
            "📂 Seleccionar pregunta del cuestionario", 
            ["⌨️ Escribir propia consulta..."] + list(queries_info.keys())
        )

        # 3. Mostrar el enunciado en un Expander si se selecciona una pregunta
        valor_sql = f"SELECT * FROM {selected} LIMIT 10" # Default
        
        # Diccionario de interpretaciones
        interpretaciones = {
            "🏀 1: La Red de Asistencias y el Dúo Más Prolífico": "📌 **Interpretación:** Revela las duplas más letales de la última década. Combina al mejor asistente de la liga con un compañero Top 10 en anotación. El total combinado (puntos + asistencias) mide la producción ofensiva conjunta. Temporadas recientes muestran totales más altos debido al mayor ritmo de juego.",
            
            "🔄 2: Rendimiento Ofensivo en 'Back-to-Backs'": "📌 **Interpretación:** Cuantifica el impacto del cansancio en el rendimiento. Equipos con plantilla profunda (Clippers, Raptors) son menos afectados. Una caída >15% en el porcentaje de victorias sugiere falta de profundidad en la banca. Esta métrica es clave para evaluar estrategias de rotación.",
            
            "🔥 3: Rachas de Triples-Dobles e Impacto en Victoria": "📌 **Interpretación:** Los triples-dobles consecutivos son el sello de jugadores versátiles. Russell Westbrook (5 seguidos en 2017) y Nikola Jokić son ejemplos recientes. El margen de victoria promedio (Plus/Minus) indica si esas rachas se traducen en éxito colectivo. Valores > +10 sugieren dominio real; cercanos a cero indican estadísticas 'vistosas' pero no determinantes.",
            
            "📊 4: Brecha Estadística entre Titulares y Suplentes": "📌 **Interpretación:** Mide la profundidad de plantilla de cada equipo. Una brecha >60% en puntos indica alta dependencia de titulares (ej: Lakers 2023). Brechas bajas (<40%) sugieren bancas productivas (ej: Kings 2023). En asistencias, las brechas suelen ser más pronunciadas porque los bases titulares son los principales generadores.",
            
            "🏹 5: La Revolución del Triple y Evolución del Juego": "📌 **Interpretación:** Confirma estadísticamente la 'revolución del triple' en la NBA. Equipos como Houston Rockets (25% → 48%) y Golden State Warriors (28% → 42%) muestran los crecimientos más drásticos. El promedio de la liga pasó de ~22% (2014) a ~38% (2023), explicando en parte el aumento del ritmo (Pace) y los puntos por partido (PPG)."
        }

        if not opcion_elegida.startswith("⌨️"):
            info = queries_info[opcion_elegida]
            
            with st.expander("📖 Ver Enunciado Completo"):
                st.write(info["enunciado"])
            
            QUERY_DIR = Path("Queries/Respuesta de Cuestionario")
            ruta_archivo = QUERY_DIR / info["archivo"]
            try:
                valor_sql = ruta_archivo.read_text(encoding="utf-8")
            except FileNotFoundError:
                st.error(f"No se encontró el archivo: {info['archivo']}")

        # 4. Editor de texto
        sql = st.text_area("Editor SQL", value=valor_sql, height=250)
        
        # 5. Botón de ejecución
        if st.button("🚀 Ejecutar Consulta", use_container_width=True):
            try:
                res = pd.read_sql_query(sql, con)
                st.dataframe(res, use_container_width=True)
                
                # Mostrar interpretación si es consulta predefinida
                if not opcion_elegida.startswith("⌨️") and opcion_elegida in interpretaciones:
                    st.info(interpretaciones[opcion_elegida])
                
                st.download_button("📥 Descargar CSV", res.to_csv(index=False), "resultado_nba.csv", "text/csv")
            except Exception as e:
                st.error(f"Error en la consulta: {e}")