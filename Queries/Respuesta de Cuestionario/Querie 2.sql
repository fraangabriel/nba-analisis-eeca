WITH Calculo_Puntos AS (
    SELECT 
        EE.id_partido, 
        EE.id_equipo, 
        P.fecha,
        SUM(((EE.FG - EE."3P") * 2) + (EE."3P" * 3) + EE.FT) AS pts_equipo
    FROM Est_Equipos EE
    JOIN Partidos P ON EE.id_partido = P.id_partido
    GROUP BY EE.id_partido, EE.id_equipo
),
Detalle_Resultados AS (
    --Resultado del partido y el tiempo de recuperación entre encuentros
    SELECT 
        C1.id_equipo, 
        C1.fecha, 
        C1.pts_equipo,
        --Identifica de victoria (1) o derrota (0) comparando puntos contra el rival
        CASE WHEN C1.pts_equipo > C2.pts_equipo THEN 1 ELSE 0 END AS es_victoria,
        --Recupera la fecha anterior del mismo equipo y la convierte a número para calcular el descanso
        JULIANDAY(C1.fecha) - JULIANDAY(LAG(C1.fecha) OVER (PARTITION BY C1.id_equipo ORDER BY C1.fecha)) AS dias_descanso
    FROM Calculo_Puntos C1
    JOIN Calculo_Puntos C2 ON C1.id_partido = C2.id_partido AND C1.id_equipo <> C2.id_equipo
),
Agrupado_Por_Descanso AS (
    --Cálculo del éxito y los puntos promedio según los días que tuvo el equipo para recuperarse
    SELECT 
        id_equipo,
      -- Métricas de rendimiento con recuperación completa (2 o más días)
        AVG(CASE WHEN dias_descanso >= 2 THEN es_victoria ELSE NULL END) * 100 AS pct_victoria_descanso,
        AVG(CASE WHEN dias_descanso >= 2 THEN pts_equipo ELSE NULL END) AS pts_promedio_descanso,
      -- Métricas de rendimiento en noches consecutivas o Back-to-Back (1 día)
        AVG(CASE WHEN dias_descanso = 1 THEN es_victoria ELSE NULL END) * 100 AS pct_victoria_b2b,
        AVG(CASE WHEN dias_descanso = 1 THEN pts_equipo ELSE NULL END) AS pts_promedio_b2b
    FROM Detalle_Resultados
    GROUP BY id_equipo
)
--Seleccionón de los 5 equipos cuya probabilidad de victoria se ve mayor afectada por la falta de descanso
SELECT 
    E.abreviatura AS "Equipo",
    ROUND(A.pct_victoria_descanso, 2) AS "Victorias % (Descanso)",
    ROUND(A.pct_victoria_b2b, 2) AS "Victorias % (Back-to-Back)",
    ROUND(A.pts_promedio_descanso, 1) AS "Promedio PTS (Descanso)",
    ROUND(A.pts_promedio_b2b, 1) AS "Promedio PTS (Back-to-Back)",
    ROUND(ABS(A.pct_victoria_descanso - A.pct_victoria_b2b), 2) AS "Diferencia Absoluta %"
FROM Agrupado_Por_Descanso A
JOIN Equipos E ON A.id_equipo = E.id_equipo
WHERE A.pct_victoria_descanso IS NOT NULL 
  AND A.pct_victoria_b2b IS NOT NULL
ORDER BY (A.pct_victoria_descanso - A.pct_victoria_b2b) DESC
LIMIT 5;