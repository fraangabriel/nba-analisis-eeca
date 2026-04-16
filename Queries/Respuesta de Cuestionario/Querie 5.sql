WITH Estadisticas_Base AS (
    --Cálculo de puntos totales y puntos de triples por equipo y temporada
    SELECT 
        E.abreviatura AS equipo_nombre,
        T.codigo_temporada AS temporada,
        SUM((EE.FG - EE."3P") * 2 + EE."3P" * 3 + EE.FT) AS pts_totales,
        SUM(EE."3P" * 3) AS pts_triple
    FROM Est_Equipos EE
    JOIN Equipos E ON EE.id_equipo = E.id_equipo
    JOIN Partidos P ON EE.id_partido = P.id_partido
    JOIN Temporadas T ON P.id_temporada = T.id_temporada
    GROUP BY E.id_equipo, T.id_temporada
),
Rango_Temporal AS (
    -- Extremos por diferencia de al menos 5 años
    SELECT 
        equipo_nombre,
        MIN(temporada) AS primera_temp,
        MAX(temporada) AS ultima_temp
    FROM Estadisticas_Base
    GROUP BY equipo_nombre
    --Conversion del codigo de temporada a entero para restar los años 
    HAVING (CAST(SUBSTR(MAX(temporada), 1, 2) AS INTEGER) - 
            CAST(SUBSTR(MIN(temporada), 1, 2) AS INTEGER)) >= 5
)
--Conclusión
SELECT 
    R.equipo_nombre AS "Equipo",
    R.primera_temp AS "Temporada Inicial",
    ROUND((T1.pts_triple * 100.0 / T1.pts_totales), 2) AS "Dependencia Inicial (%)",
    R.ultima_temp AS "Temporada Reciente",
    ROUND((T2.pts_triple * 100.0 / T2.pts_totales), 2) AS "Dependencia Final (%)",
    ROUND((T2.pts_triple * 100.0 / T2.pts_totales) - (T1.pts_triple * 100.0 / T1.pts_totales), 2) AS "Crecimiento Absoluto"
FROM Rango_Temporal R
JOIN Estadisticas_Base T1 ON R.equipo_nombre = T1.equipo_nombre AND R.primera_temp = T1.temporada
JOIN Estadisticas_Base T2 ON R.equipo_nombre = T2.equipo_nombre AND R.ultima_temp = T2.temporada
ORDER BY "Crecimiento Absoluto" DESC;