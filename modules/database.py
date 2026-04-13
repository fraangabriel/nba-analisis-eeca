import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = 'Base de Datos/Version_Normalizada/NBA-Boxscore-Database-Normalizado-Limpio.sqlite'

@st.cache_data
def run_query(query):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"No se pudo leer la base de datos: {e}")
        return pd.DataFrame()

def get_resumen_temporadas():
    """Consulta con variables base, para la matriz de correlación"""
    query = """
    SELECT
        t.codigo_temporada AS season,
        AVG((ee."3P" * 3) + (ee.FG - ee."3P") * 2 + ee.FT) AS avg_ppg,
        AVG(ee.FGA + (0.44 * ee.FTA) - ee.ORB + ee.TOV) AS avg_pace,
        AVG((ee.FG + 0.5 * ee."3P") / NULLIF(ee.FGA, 0)) AS avg_efg,
        AVG(ee.FGA) AS avg_fga,
        AVG(ee."3P") AS avg_3p,
        AVG(ee.TOV) AS avg_tov,
        AVG(ee.ORB) AS avg_orb
    FROM Est_Equipos ee
    JOIN Partidos p ON ee.id_partido = p.id_partido
    JOIN Temporadas t ON p.id_temporada = t.id_temporada
    WHERE t.codigo_temporada BETWEEN 1314 AND 2223
    GROUP BY t.codigo_temporada
    ORDER BY t.codigo_temporada;
    """
    return run_query(query)

def get_eficiencia_jugadores():
    """ EFICIENCIA INDIVIDUAL DE JUGADORES"""
    query = """
    SELECT
        j.nombre_completo AS player,
        t.codigo_temporada AS season,
        AVG(((ej."3P" * 3) + (ej.FG - ej."3P") * 2 + ej.FT) / (2 * NULLIF(ej.FGA + 0.44 * ej.FTA, 0))) AS avg_tsp
    FROM Est_Jugadores ej
    JOIN Jugadores j ON ej.id_jugador = j.id_jugador
    JOIN Partidos p ON ej.id_partido = p.id_partido
    JOIN Temporadas t ON p.id_temporada = t.id_temporada
    GROUP BY j.nombre_completo, t.codigo_temporada
    HAVING COUNT(ej.id_partido) > 10
    ORDER BY avg_tsp DESC;
    """
    return run_query(query)

def get_lista_equipos():
    return run_query("SELECT DISTINCT abreviatura FROM Equipos")
