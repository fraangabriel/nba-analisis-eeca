WITH Estadisticas_Base AS (
    -- Agrupar las métricas claves por temporada para el cálculo de tasas
    SELECT 
        T.codigo_temporada,
        COUNT(DISTINCT P.id_partido) AS total_partidos,
        SUM(EE.FGA + 0.44 * EE.FTA + EE.TOV) AS total_posesiones,
        SUM(EE.TOV) AS total_perdidas,
        SUM(EE.MP / 5.0) AS minutos_totales -- Dividir entre 5 jugadores en cancha
    FROM Est_Equipos EE
    JOIN Partidos P ON EE.id_partido = P.id_partido
    JOIN Temporadas T ON P.id_temporada = T.id_temporada
    GROUP BY T.id_temporada
)
-- Análisis de la relación entre Velocidad (Pace) y Errores (TOV%)
SELECT 
    codigo_temporada AS "Temporada",
    ROUND((total_posesiones * 48.0) / minutos_totales, 2) AS "Pace (Ritmo)",
    ROUND((total_perdidas * 100.0) / total_posesiones, 2) AS "Turnover % (Tasa de Error)",
    total_partidos AS "Partidos Analizados"
FROM Estadisticas_Base
ORDER BY "Temporada" ASC;