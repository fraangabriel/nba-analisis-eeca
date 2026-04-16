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
        sql = st.text_area("Consulta SQL", value=f"SELECT * FROM {selected} LIMIT 10", height=250)
        
        if st.button("▶ Ejecutar SQL", use_container_width=True):
            try:
                res = pd.read_sql_query(sql, con)
                st.dataframe(res, use_container_width=True)
                st.download_button("📥 Descargar CSV", res.to_csv(index=False), "query.csv", "text/csv")
            except Exception as e:
                st.error(f"Error: {e}")

st.divider()
navegacion("Regresión", "Conclusión")
