WITH 
    -- Calculo de los puntos (PTS) y sumamos las asistencias (AST) por temporada
    Estadisticas_Base AS (
        SELECT 
            P.id_temporada, 
            EJ.id_equipo, 
            EJ.id_jugador, 
            SUM(EJ.AST) AS asistencias_totales, 
            -- Se aplica la formula: ((FG - 3P) * 2) + (3P * 3) + FT
            SUM(((EJ.FG - EJ."3P") * 2) + (EJ."3P" * 3) + EJ.FT) AS puntos_totales
        FROM Est_Jugadores EJ
        INNER JOIN Partidos P ON EJ.id_partido = P.id_partido 
        GROUP BY P.id_temporada, EJ.id_equipo, EJ.id_jugador
    ),

    -- Identificación del líder de asistencias de la liga por temporada
    Lider_Asistencias_Liga AS (
        SELECT 
            id_temporada, id_jugador, id_equipo, asistencias_totales
        FROM (
            SELECT 
                *, 
                RANK() OVER(PARTITION BY id_temporada ORDER BY asistencias_totales DESC) AS rango_ast
            FROM Estadisticas_Base
        ) 
        WHERE rango_ast = 1
    ),

    -- Identificación de los 10 máximos anotadores de la liga por temporada
    Top_10_Anotadores_Liga AS (
        SELECT 
            id_temporada, id_jugador, id_equipo, puntos_totales
        FROM (
            SELECT 
                *, 
                RANK() OVER(PARTITION BY id_temporada ORDER BY puntos_totales DESC) AS rango_pts
            FROM Estadisticas_Base
        ) 
        WHERE rango_pts <= 10
    )

-- Unión final para encontrar a los compañeros de equipo que cumplen ambos criterios
SELECT 
    -- Transformamos '1314' en '2013-2014'
    '20' || SUBSTR(T.codigo_temporada, 1, 2) || '-20' || SUBSTR(T.codigo_temporada, 3, 2) AS "Año",
    E.abreviatura AS "Nombre del Equipo",
    J_AST.nombre_completo AS "Armador (Asistencias)",
    J_PTS.nombre_completo AS "Anotador (Puntos)",
    (L.asistencias_totales + A.puntos_totales) AS "Total Combinado (Pts + Ast)"
FROM Lider_Asistencias_Liga L
INNER JOIN Top_10_Anotadores_Liga A 
    ON L.id_temporada = A.id_temporada 
    AND L.id_equipo = A.id_equipo
INNER JOIN Temporadas T ON L.id_temporada = T.id_temporada
INNER JOIN Equipos E ON L.id_equipo = E.id_equipo
INNER JOIN Jugadores J_AST ON L.id_jugador = J_AST.id_jugador
INNER JOIN Jugadores J_PTS ON A.id_jugador = J_PTS.id_jugador
WHERE L.id_jugador <> A.id_jugador -- De esta forma se asegura que el dúo lo conformen dos personas distintas
ORDER BY T.codigo_temporada ASC;
