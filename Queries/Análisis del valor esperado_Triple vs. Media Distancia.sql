SELECT 
    T.codigo_temporada AS "Temporada",
    ROUND(SUM(EE."3P" * 3.0) / SUM(EE."3PA"), 3) AS "Valor Esperado (Triple)",
    ROUND(SUM((EE.FG - EE."3P") * 2.0) / SUM(EE.FGA - EE."3PA"), 3) AS "Valor Esperado (Doble)",
    ROUND((SUM(EE."3P" * 3.0) / SUM(EE."3PA")) - (SUM((EE.FG - EE."3P") * 2.0) / SUM(EE.FGA - EE."3PA")), 3) AS "Diferencia de Eficiencia"
FROM Est_Equipos EE
JOIN Partidos P ON EE.id_partido = P.id_partido
JOIN Temporadas T ON P.id_temporada = T.id_temporada
GROUP BY T.id_temporada
ORDER BY T.codigo_temporada ASC;