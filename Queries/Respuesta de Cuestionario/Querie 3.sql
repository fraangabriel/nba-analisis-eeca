WITH Estadisticas_Base AS (
    --Selección de estadísticas base uniendo las tablas del estudio y generando 
    --la secuencia cronológica de partidos jugados por cada jugador
    SELECT 
        J.nombre_completo,
        T.codigo_temporada,
        P.fecha,
        -- Cálculo de puntos y rebotes
        ((EJ.FG - EJ."3P") * 2 + EJ."3P" * 3 + EJ.FT) AS pts,
        (EJ.ORB + EJ.DRB) AS reb,
        EJ.AST AS ast,
        EJ.PM AS margen_victoria,
        ROW_NUMBER() OVER(PARTITION BY J.id_jugador ORDER BY P.fecha) AS seq_juego
    FROM Est_Jugadores EJ
    JOIN Jugadores J ON EJ.id_jugador = J.id_jugador
    JOIN Partidos P ON EJ.id_partido = P.id_partido
    JOIN Temporadas T ON P.id_temporada = T.id_temporada
),
Filtro_Triple_Doble AS (
    -- Selección de triples-dobles y numeración de orden para comparar con el historial de partidos
    SELECT *,
        ROW_NUMBER() OVER(PARTITION BY nombre_completo ORDER BY fecha) AS seq_td
    FROM Estadisticas_Base
    WHERE pts >= 10 AND reb >= 10 AND ast >= 10
),
Identificacion_Rachas AS (
    -- Agrupado por diferencia de secuencias para identificar rachas consecutivas y calcular el promedio de PM
    SELECT 
        nombre_completo,
        codigo_temporada,
        COUNT(*) AS longitud_racha,
        MIN(fecha) AS fecha_inicio,
        MAX(fecha) AS fecha_fin,
        AVG(margen_victoria) AS plus_minus_promedio
    FROM Filtro_Triple_Doble
    GROUP BY nombre_completo, codigo_temporada, (seq_juego - seq_td)
    HAVING COUNT(*) >= 3
),
Ranking_Por_Jugador AS (
    -- Clasificación de las rachas de cada jugador para tener únicamente aquella con mayor cantidad de partidos consecutivos
    SELECT *,
        ROW_NUMBER() OVER(PARTITION BY nombre_completo ORDER BY longitud_racha DESC, fecha_inicio DESC) AS rnk
    FROM Identificacion_Rachas
)
-- Conclusión con los items solicitados
SELECT 
    nombre_completo AS "Nombre de Jugador",
    codigo_temporada AS "Temporada",
    longitud_racha AS "Cantidad de Partidos",
    fecha_inicio AS "Fecha de Inicio",
    fecha_fin AS "Fecha de Fin",
    ROUND(plus_minus_promedio, 2) AS "Margen de Victoria Promedio"
FROM Ranking_Por_Jugador
WHERE rnk = 1
ORDER BY "Partidos Consecutivos" DESC, "Jugador" ASC;