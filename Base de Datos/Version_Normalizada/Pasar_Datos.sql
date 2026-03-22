
INSERT INTO Equipos (abreviatura)
SELECT DISTINCT team FROM team_stats;

INSERT INTO Jugadores (nombre_completo)
SELECT DISTINCT player FROM player_stats;


INSERT INTO Temporadas (codigo_temporada)
SELECT DISTINCT season FROM game_info;


INSERT INTO Partidos (id_partido, id_temporada, fecha, id_local, id_visitante)
SELECT
    gi.game_id,
    t.id_temporada,
    gi.date,
    el.id_equipo,
    ev.id_equipo
FROM game_info gi
JOIN Temporadas t ON gi.season = t.codigo_temporada
JOIN Equipos el ON gi.home_team = el.abreviatura
JOIN Equipos ev ON gi.away_team = ev.abreviatura;


INSERT INTO Est_Equipos
SELECT
    ts.game_id, e.id_equipo, ts.MP, ts.FG, ts.FGA, ts."3P", ts."3PA",
    ts.FT, ts.FTA, ts.ORB, ts.DRB, ts.AST, ts.STL, ts.BLK, ts.TOV, ts.PF
FROM team_stats ts
JOIN Equipos e ON ts.team = e.abreviatura;


INSERT INTO Est_Jugadores
SELECT
    ps.game_id, j.id_jugador, e.id_equipo, ps.MP, ps.FG, ps.FGA, ps."3P", ps."3PA",
    ps.FT, ps.FTA, ps.ORB, ps.DRB, ps.AST, ps.STL, ps.BLK, ps.TOV, ps.PF, ps.PM
FROM player_stats ps
JOIN Jugadores j ON ps.player = j.nombre_completo
JOIN Equipos e ON ps.team = e.abreviatura;
