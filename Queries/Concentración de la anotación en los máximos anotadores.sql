WITH Puntos_Por_Jugador AS (
    -- Cálculo de puntos totales por jugador en cada temporada y equipo
    SELECT 
        T.codigo_temporada,
        EJ.id_equipo,
        EJ.id_jugador,
        SUM((EJ.FG - EJ."3P") * 2 + EJ."3P" * 3 + EJ.FT) AS pts_totales_jugador
    FROM Est_Jugadores EJ
    JOIN Partidos P ON EJ.id_partido = P.id_partido
    JOIN Temporadas T ON P.id_temporada = T.id_temporada
    GROUP BY T.id_temporada, EJ.id_equipo, EJ.id_jugador
),
Ranking_Anotadores AS (
    -- Rankeao a los jugadores dentro de su equipo
    SELECT 
        *,
        RANK() OVER (PARTITION BY codigo_temporada, id_equipo ORDER BY pts_totales_jugador DESC) as ranking_anotador
    FROM Puntos_Por_Jugador
),
Totales_Equipo AS (
    -- Suma de los puntos totales de cada equipo por temporada
    SELECT 
        codigo_temporada, 
        id_equipo, 
        SUM(pts_totales_jugador) as pts_equipo
    FROM Puntos_Por_Jugador
    GROUP BY codigo_temporada, id_equipo
)
-- % de puntos de los 2 mejores anotadores por temporada
SELECT 
    RA.codigo_temporada AS "Temporada",
    ROUND(AVG( (SELECT SUM(pts_totales_jugador) 
                FROM Ranking_Anotadores RA2 
                WHERE RA2.id_equipo = RA.id_equipo 
                AND RA2.codigo_temporada = RA.codigo_temporada 
                AND RA2.ranking_anotador <= 2) * 100.0 / TE.pts_equipo ), 2) AS "Dependencia de Estrellas (%)"
FROM Ranking_Anotadores RA
JOIN Totales_Equipo TE ON RA.id_equipo = TE.id_equipo AND RA.codigo_temporada = TE.codigo_temporada
GROUP BY RA.codigo_temporada
ORDER BY RA.codigo_temporada ASC;