DROP TABLE IF EXISTS Pregled;
DROP TABLE IF EXISTS Zdravnik;
DROP TABLE IF EXISTS Oddelek;
DROP TABLE IF EXISTS Lokacija;
DROP TABLE IF EXISTS Pacient;

CREATE TABLE Pacient (
    id_pacienta integer NOT NULL primary key,
    ime_pacienta varchar NOT NULL,
    uporabnisko_ime text NOT NULL,
    geslo_hash varchar NOT NULL,
    datum_rojstva date NOT NULL,
    spol varchar NOT NULL,
    reden boolean NOT NULL
);

CREATE TABLE Lokacija (
    id_lokacije integer NOT NULL primary key,
    naslov text NOT NULL
);

CREATE TABLE Oddelek (
    id_oddelka integer NOT NULL primary key,
    ime_oddelka varchar NOT NULL,
    lokacija int REFERENCES Lokacija(id_lokacije)
);

CREATE TABLE Zdravnik (
    id_zdravnika integer NOT NULL primary key,
    ime_zdravnika varchar NOT NULL,
    oddelek int REFERENCES Oddelek(id_oddelka) 
);

CREATE TABLE Pregled (
    id_pregleda integer NOT NULL primary key,
    datum date NOT NULL,
    cas time NOT NULL,
    opis text,
    pacient int REFERENCES Pacient(id_pacienta),
    zdravnik int REFERENCES Zdravnik(id_zdravnika)
);

-- give permission for everything to mokrole

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mokrole;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO mokrole;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO mokrole;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON TABLES TO mokrole;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON SEQUENCES TO mokrole;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON FUNCTIONS TO mokrole;