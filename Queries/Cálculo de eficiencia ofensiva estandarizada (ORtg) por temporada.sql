WITH Metricas_Por_Temporada AS (
    -- Calculamos la producción ofensiva y el volumen de posesiones por temporada 
    SELECT 
        T.codigo_temporada,
        SUM((EE.FG - EE."3P") * 2 + EE."3P" * 3 + EE.FT) AS puntos_totales,
        SUM(EE.FGA + 0.44 * EE.FTA + EE.TOV) AS posesiones_estimadas
    FROM Est_Equipos EE
    JOIN Partidos P ON EE.id_partido = P.id_partido
    JOIN Temporadas T ON P.id_temporada = T.id_temporada
    GROUP BY T.id_temporada
)
-- Reporte de eficiencia pura: aislando el ritmo del juego (Pace) 
SELECT 
    codigo_temporada AS "Temporada",
    ROUND(puntos_totales, 2) AS "Total Puntos",
    ROUND(posesiones_estimadas, 2) AS "Total Posesiones",
    ROUND((puntos_totales * 100.0) / posesiones_estimadas, 2) AS "Eficiencia Ofensiva (ORtg)"
FROM Metricas_Por_Temporada
ORDER BY "Temporada" ASC;