
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