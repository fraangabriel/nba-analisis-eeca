🏀 Análisis de la Evolución de la NBA: Velocidad vs. Eficiencia

Este repositorio contiene un análisis estadístico de la transformación de la NBA durante la última década (2013‑2023). El estudio está orientado a determinar si el aumento de la anotación se debe a un juego más rápido (ritmo) o a una mejora en la puntería (efectividad de tiro), transformando datos brutos de partidos en información cuantitativa mediante técnicas de correlación, regresión y visualizaciones interactivas.

📖 Descripción del Proyecto

El proyecto estudia cómo ha cambiado la forma de jugar y anotar en la NBA desde 2013 hasta 2023. Se enfoca en responder si los equipos anotan más puntos porque ahora juegan más rápido (mayor ritmo) o porque han mejorado su efectividad de tiro. A través de un análisis riguroso de 10 temporadas completas, se explica de forma clara por qué los partidos de hoy son tan diferentes a los de hace diez años.

📑 Planteamiento del Problema

En los últimos años, la NBA ha vivido una transformación radical: el ritmo es más vertiginoso, el volumen de triples se ha disparado y los marcadores son cada vez más altos. Sin embargo, surge la necesidad de determinar con rigor estadístico si este aumento del ritmo está asociado directamente a un incremento real en la anotación.

Bajo este contexto, resulta fundamental analizar si los años con más ritmo son efectivamente los de mayor puntaje y determinar si el aumento de la velocidad en la cancha mejora o, por el contrario, empeora la efectividad de los tiros de campo. En última instancia, el problema radica en definir si el innegable incremento en los puntos por partido observado en la última década se debe principalmente a un mayor volumen de posesiones o a una mejora sustancial en la puntería por parte de los equipos.

Este trabajo responde estas interrogantes mediante un análisis estadístico riguroso de 10 temporadas completas.

🎯 Objetivos del Estudio

✅ Objetivo General

Analizar la relación entre el incremento del ritmo de juego (Pace) y la anotación en la NBA durante la última década, evaluando el papel fundamental que ha desempeñado la efectividad de tiro (eFG%) en esta evolución.

📌 Objetivos Específicos

- Monitorear la evolución histórica: Documentar el comportamiento del ritmo, los puntos por partido y la efectividad de tiro temporada tras temporada para identificar patrones de cambio.

- Validar la correlación ritmo‑anotación: Determinar estadísticamente si el aumento en la velocidad de las posesiones se traduce de manera directa en un incremento proporcional del marcador.

- Evaluar el impacto en la precisión: Analizar si jugar a una mayor velocidad beneficia o perjudica la efectividad de los tiros de campo de los equipos.

- Definir el factor de crecimiento: Identificar si el auge anotador de la última década es impulsado primordialmente por un mayor volumen de jugadas o por una mejora técnica en la puntería de los jugadores.

🧪 Metodología y Tecnologías

Herramienta	Uso

Power BI	Dashboard interactivo con gráficos de dispersión, evolución temporal, tarjetas dinámicas y segmentadores.
Python + Streamlit	Aplicación web complementaria para mostrar coeficientes de correlación (Pearson, Spearman), modelo de regresión y contraste de hipótesis.
SQLite / CSV	Almacenamiento y exportación de los datos normalizados (tablas Est_Equipos, Partidos, Temporadas).
DAX	Medidas dinámicas para calcular pendiente, intercepto, R², y ecuación de regresión en Power BI.

📊 Resultados Clave

-Correlación ritmo‑puntos: r = 0.942 (muy fuerte, p < 0.001). Se rechaza H₀.

-Correlación ritmo‑efectividad: r = 0.855 (fuerte, p < 0.01). También significativa.

-Ecuación de regresión (Puntos):
PPG = -101.66 + 2.0959 × Pace
*Por cada posesión extra → +2.1 puntos.*

-Ecuación de regresión (Efectividad):
eFG% = -0.0865 + 0.0061 × Pace
*Por cada 10 posesiones extra → +6 puntos porcentuales de efectividad.*

Evolución (2013‑2023):

Ritmo: +5.4%

Puntos: +13.7%

Efectividad: +4.4%

La anotación creció mucho más que el ritmo y la efectividad por separado, lo que indica un efecto sinérgico entre ambas variables.

🔗 Enlaces a los Dashboards

Herramienta	Enlace
[![App de Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://nba-estadisticas.streamlit.app/)

[![Power BI Report](https://img.shields.io/badge/Data_Report-Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://app.powerbi.com/links/RE7sq9nTOG?ctid=4c818f79-ab84-4552-9b7c-2fe715b0d0d5&pbi_source=linkShare)
