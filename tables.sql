CREATE TABLE Pacient (
    id_pacienta serial NOT NULL primary key,
    ime_pacienta varchar NOT NULL,
    uporabnisko_ime text NOT NULL,
    geslo varchar NOT NULL, 
    -- geslo hash
    starost int NOT NULL,
    CHECK (starost >= 0),
    spol varchar NOT NULL,
    reden boolean NOT NULL
);

CREATE TABLE Oddelek (
    id_oddelka serial NOT NULL primary key,
    ime_oddelka varchar NOT NULL,
    lokacija varchar NOT NULL
);

CREATE TABLE Zdravnik (
    id_zdravnika serial NOT NULL primary key,
    ime_zdravnika varchar NOT NULL,
    oddelek int REFERENCES Oddelek(id_oddelka) 
);

CREATE TABLE Pregled (
    id_pregleda serial NOT NULL primary key,
    datum time NOT NULL,
    cas text NOT NULL,
    opis text,
    pacient int REFERENCES Pacient(id_pacienta),
    zdravnik int REFERENCES Zdravnik(id_zdravnika)
);

CREATE TABLE Lokacija (
    id_lokacije integer NOT NULL primary key,
    naslov text
)

