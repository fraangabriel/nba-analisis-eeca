--Creación de la base de datos normalizada

CREATE TABLE Equipos (
    id_equipo INTEGER PRIMARY KEY AUTOINCREMENT,
    abreviatura TEXT UNIQUE
);

CREATE TABLE Jugadores (
    id_jugador INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_completo TEXT UNIQUE
);

CREATE TABLE Temporadas (
    id_temporada INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_temporada INTEGER UNIQUE
);


CREATE TABLE Partidos (
    id_partido INTEGER PRIMARY KEY,
    id_temporada INTEGER,
    fecha TEXT,
    id_local INTEGER,
    id_visitante INTEGER,
    FOREIGN KEY (id_temporada) REFERENCES Temporadas(id_temporada),
    FOREIGN KEY (id_local) REFERENCES Equipos(id_equipo),
    FOREIGN KEY (id_visitante) REFERENCES Equipos(id_equipo)
);


CREATE TABLE Est_Equipos (
    id_partido INTEGER,
    id_equipo INTEGER,
    MP TEXT, FG REAL, FGA REAL, "3P" REAL, "3PA" REAL, 
    FT REAL, FTA REAL, ORB REAL, DRB REAL, AST REAL, 
    STL REAL, BLK REAL, TOV REAL, PF REAL,
    PRIMARY KEY (id_partido, id_equipo),
    FOREIGN KEY (id_partido) REFERENCES Partidos(id_partido),
    FOREIGN KEY (id_equipo) REFERENCES Equipos(id_equipo)
);

CREATE TABLE Est_Jugadores (
    id_partido INTEGER,
    id_jugador INTEGER,
    id_equipo INTEGER,
    MP TEXT, FG REAL, FGA REAL, "3P" REAL, "3PA" REAL, 
    FT REAL, FTA REAL, ORB REAL, DRB REAL, AST REAL, 
    STL REAL, BLK REAL, TOV REAL, PF REAL, PM REAL,
    PRIMARY KEY (id_partido, id_jugador),
    FOREIGN KEY (id_partido) REFERENCES Partidos(id_partido),
    FOREIGN KEY (id_jugador) REFERENCES Jugadores(id_jugador),
    FOREIGN KEY (id_equipo) REFERENCES Equipos(id_equipo)
);


-- Pasar datos a las tablas normalizadas

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


-- Borrar tablas originales

DROP TABLE IF EXISTS game_info;

DROP TABLE IF EXISTS player_stats;

DROP TABLE IF EXISTS team_stats;


-- Tratamiento de NULL en Estadistica de Jugadores 

SELECT 
    'Est_Jugadores' AS tabla,
    COUNT(*) AS total_registros,
    -- Validacion de llaves foranas
    SUM(CASE WHEN id_jugador IS NULL THEN 1 ELSE 0 END) AS nulos_id_jugador,
    SUM(CASE WHEN id_equipo IS NULL THEN 1 ELSE 0 END) AS nulos_id_equipo,
    SUM(CASE WHEN id_partido IS NULL THEN 1 ELSE 0 END) AS nulos_id_partido,
    -- Validacion de tiempo 
    SUM(CASE WHEN MP IS NULL OR MP = '' THEN 1 ELSE 0 END) AS nulos_o_vacios_MP,
    SUM(CASE WHEN FG IS NULL THEN 1 ELSE 0 END) AS nulos_tiros_campo,
    SUM(CASE WHEN FGA IS NULL THEN 1 ELSE 0 END) AS nulos_intentos_campo,
    SUM(CASE WHEN "3P" IS NULL THEN 1 ELSE 0 END) AS nulos_triples,
    SUM(CASE WHEN AST IS NULL THEN 1 ELSE 0 END) AS nulos_asistencias,
    SUM(CASE WHEN PM IS NULL THEN 1 ELSE 0 END) AS nulos_plus_minus
FROM Est_Jugadores;


SELECT 
    MP AS texto_detectado, -- Muestra la etiqueta (ej. 'Did Not Dress')
    COUNT(*) AS cantidad_filas -- Cuantos jugadores están en este estado
FROM Est_Jugadores 
WHERE MP LIKE '%Did Not%' 
   OR MP LIKE '%Not With%'
   OR MP LIKE '%Suspended%'
GROUP BY MP;


SELECT 
    'Est_Equipos' AS tabla,
    COUNT(*) AS total_filas,
    SUM(CASE WHEN id_partido IS NULL THEN 1 ELSE 0 END) AS nulos_fk_partido,
    SUM(CASE WHEN id_equipo IS NULL THEN 1 ELSE 0 END) AS nulos_fk_equipo,
    SUM(CASE WHEN MP IS NULL THEN 1 ELSE 0 END) AS nulos_minutos,
    SUM(CASE WHEN FG IS NULL THEN 1 ELSE 0 END) AS nulos_fg,
    SUM(CASE WHEN FGA IS NULL THEN 1 ELSE 0 END) AS nulos_fga
FROM Est_Equipos;

SELECT 
    'Partidos' AS tabla,
    COUNT(*) AS total_partidos,
    SUM(CASE WHEN id_temporada IS NULL THEN 1 ELSE 0 END) AS nulos_temporada,
    SUM(CASE WHEN id_local IS NULL THEN 1 ELSE 0 END) AS nulos_local,
    SUM(CASE WHEN id_visitante IS NULL THEN 1 ELSE 0 END) AS nulos_visitante,
    SUM(CASE WHEN fecha IS NULL THEN 1 ELSE 0 END) AS nulos_fecha
FROM Partidos;

-- Revision de Jugadores
SELECT 'Jugadores' AS tabla, COUNT(*) AS total, 
       SUM(CASE WHEN nombre_completo IS NULL THEN 1 ELSE 0 END) AS nulos_nombre 
FROM Jugadores;

-- Revision de Equipos
SELECT 'Equipos' AS tabla, COUNT(*) AS total, 
       SUM(CASE WHEN abreviatura IS NULL THEN 1 ELSE 0 END) AS nulos_abrevia 
FROM Equipos;

-- Revision de Temporadas
SELECT 'Temporadas' AS tabla, COUNT(*) AS total, 
       SUM(CASE WHEN codigo_temporada IS NULL THEN 1 ELSE 0 END) AS nulos_codigo 
FROM Temporadas;


-- Tratamiento estadistica de Jugadores

-- Paso 1, convertir mensajes en 00:00:
UPDATE Est_Jugadores 
SET MP = '00:00' 
WHERE MP LIKE '%Did Not%' 
   OR MP LIKE '%Not With%' 
   OR MP LIKE '%Suspended%'
   OR MP IS NULL 
   OR MP = '';

-- Paso 2, rellenar con ceros (0):
UPDATE Est_Jugadores 
SET 
    FG = 0, FGA = 0, 
    "3P" = 0, "3PA" = 0, 
    FT = 0, FTA = 0, 
    ORB = 0, DRB = 0, 
    AST = 0, STL = 0, 
    BLK = 0, TOV = 0, 
    PF = 0, PM = 0
WHERE MP = '00:00';

VACUUM;
