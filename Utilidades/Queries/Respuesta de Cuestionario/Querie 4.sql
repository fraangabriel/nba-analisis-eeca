WITH Partidos2223 AS (
    --Filtramos por el código de temporada '2223' 
    SELECT P.id_partido 
    FROM Partidos P
    JOIN Temporadas T ON P.id_temporada = T.id_temporada
    WHERE T.codigo_temporada = '2223'
),
Estadisticas_Filtradas AS (
    -- Obtenemos métricas base y procesamos la columna MP para tener minutos enteros
    SELECT 
        EJ.id_partido, 
        EJ.id_equipo, 
        ((EJ.FG - EJ."3P") * 2 + EJ."3P" * 3 + EJ.FT) AS pts, 
        EJ.AST AS ast, 
        (EJ.ORB + EJ.DRB) AS treb,
        CAST(SUBSTR(IFNULL(EJ.MP, '0:0'), 1, INSTR(IFNULL(EJ.MP, '0:0'), ':') - 1) AS INTEGER) AS minutos
    FROM Est_Jugadores EJ
    INNER JOIN Partidos2223 P ON EJ.id_partido = P.id_partido
),
Clasificacion_Roles AS (
    -- Definición de que los 5 con más minutos por partido/equipo son titulares
    SELECT 
        pts, ast, treb,
        CASE WHEN ROW_NUMBER() OVER(PARTITION BY id_partido, id_equipo ORDER BY minutos DESC) <= 5 
             THEN 'Titular' ELSE 'Suplente' END AS rol
    FROM Estadisticas_Filtradas
),
Promedios_Por_Rol AS (
    -- Cálculo de promedios para cada grupo
    SELECT 
        rol, 
        AVG(pts) AS mPTS, 
        AVG(ast) AS mAST, 
        AVG(treb) AS mTREB
    FROM Clasificacion_Roles 
    GROUP BY rol
),
Brechas_Calculadas AS (
    -- Cálculo la disparidad porcentual entre titulares y suplentes
    SELECT 'Puntos (PTS)' AS Metrica, t.mPTS AS Tit, s.mPTS AS Sup, (t.mPTS/s.mPTS - 1) * 100 AS Brecha 
    FROM Promedios_Por_Rol t, Promedios_Por_Rol s WHERE t.rol='Titular' AND s.rol='Suplente'
    UNION ALL
    SELECT 'Asistencias (AST)', t.mAST, s.mAST, (t.mAST/s.mAST - 1) * 100 
    FROM Promedios_Por_Rol t, Promedios_Por_Rol s WHERE t.rol='Titular' AND s.rol='Suplente'
    UNION ALL
    SELECT 'Rebotes Totales (TREB)', t.mTREB, s.mTREB, (t.mTREB/s.mTREB - 1) * 100 
    FROM Promedios_Por_Rol t, Promedios_Por_Rol s WHERE t.rol='Titular' AND s.rol='Suplente'
)
--Reporte final con la estadística de mayor brecha porcentual
SELECT 
    Metrica AS "Nombre de la Estadística", 
    ROUND(Tit, 2) AS "Promedio Grupo Titular", 
    ROUND(Sup, 2) AS "Promedio Grupo Suplente", 
    ROUND(Brecha, 2) || '%' AS "Brecha Porcentual"
FROM Brechas_Calculadas 
ORDER BY Brecha DESC 
LIMIT 1;
