import streamlit as st

nombre_pagina = {
    "Inicio": "app.py",
    "Teoría": "pages/1Teoría.py",
    "Exploración": "pages/2Exploracion_de_datos.py",
    "Correlación": "pages/3Correlacion.py",
    "Contrastes": "pages/4Contrastes.py",
    "Regresión": "pages/5Regresion.py",
    "Consultas": "pages/6Consultas.py",
    "Conclusión": "pages/7Conclusion.py"
}

def navegacion(nombre_anterior: str, nombre_siguiente: str):
    """
    Crea un botón de navegación personalizado
    
    Args:
        nombre_anterior (str): Nombre de la página anterior
        nombre_siguiente (str): Nombre de la página siguiente
    """
    col_n1, col_n2 = st.columns(2)
    with col_n1:
        if nombre_anterior == "Inicio":
            if st.button(f"🏠 Volver a {nombre_anterior}", use_container_width=True):
                st.switch_page(nombre_pagina[nombre_anterior])
        else:
            if st.button(f"⬅️ Volver a {nombre_anterior}", use_container_width=True):
                st.switch_page(nombre_pagina[nombre_anterior])
    with col_n2:
        if nombre_siguiente == "Inicio":
            if st.button(f"🏠 Ir a {nombre_siguiente}", use_container_width=True):
                st.switch_page(nombre_pagina[nombre_siguiente])
        else:
            if st.button(f"Ir a {nombre_siguiente} ➡️", use_container_width=True):
                st.switch_page(nombre_pagina[nombre_siguiente])
