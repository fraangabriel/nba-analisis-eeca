import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import sqlite3
import plotly.express as px

# 1. Configuración (SOLO UNA VEZ y al principio)
st.set_page_config(page_title="NBA Stats", layout="wide")

# 2. Título Simple
st.title("🏀 Análisis de Datos de la NBA")

# 3. Sidebar
menu = st.sidebar.selectbox(
    "Navega por la app:",
    ["Inicio", "Análisis de tiros", "Estadísticas SQL"]
)

# 4. Lógica de visualización
if menu == "Inicio":
    st.write("### Bienvenido al Dashboard")
    st.info("Selecciona una opción en la barra lateral para ver los datos.")

elif menu == "Análisis de tiros":
    st.subheader("Aquí irán los gráficos de eficiencia")
    # Ejemplo de un widget para probar que responde
    st.slider("Rango de temporadas", 2015, 2025)

else:
    st.write("Sección de SQL Querys")
    # Borrar
    st.title("Verificando mi base de datos NBA")

    # Conexión al archivo con tu ruta específica
    try:
        db_path = 'Base de Datos/Version_Normalizada/NBA-Boxscore-Database-Normalizado-Limpio.sqlite'
        conn = sqlite3.connect(db_path)

        # Este comando te dice los nombres de tus tablas
        tablas = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)

        st.write("### Tablas encontradas en tu archivo:")
        st.table(tablas)

        conn.close()
    except Exception as e:
        st.error(f"No se pudo leer el archivo: {e}")

# Función para conectar a la base de datos (Ruta corregida)
def run_query(query):
    db_path = 'Base de Datos/Version_Normalizada/NBA-Boxscore-Database-Normalizado-Limpio.sqlite'
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql(query, conn)