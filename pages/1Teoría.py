import streamlit as st
from modules.style import aplicar_estilos_globales
from modules.sidebar import mostrar_sidebar

st.set_page_config(page_title="Fundamentos Teóricos", layout="wide")

# Aplicar estilos globales
aplicar_estilos_globales()

# Mostrar sidebar
mostrar_sidebar()

st.title("📖 Fundamentos de la Investigación")
st.info("Basado en el programa de Estadística II - Escuela de Estadística y Ciencias Actuariales (UCV).")

st.markdown("""
### 1. Definición del Problema
En la última década, la NBA ha pasado de un juego posicional a uno de transiciones rápidas.
Este estudio busca determinar si el aumento en los marcadores se debe al **volumen** (Pace) o a la **eficiencia** (eFG%).

### 2. Diferenciación del Análisis
* **Análisis de Regresión:** Busca establecer la *naturaleza* de la relación funcional para realizar predicciones.
* **Análisis de Correlación:** Determina el *grado y sentido* de la relación lineal.

### 3. El Modelo Probabilístico
No asumimos una relación exacta, sino una con perturbación aleatoria:
""")

st.latex(r"Y_i = A + B X_i + E_i")

st.markdown("""
* **A (Intercepto):** Valor medio de Y cuando X es 0.
* **B (Pendiente):** Cambio en el valor medio de Y por cada unidad de cambio en X.
* **E (Residuo):** Parte estocástica que recoge variables no incluidas o errores de medición.
""") 