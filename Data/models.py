from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime, time, date

# definiramo razrede / podatkovne modele

@dataclass_json
@dataclass
class pacient:
    id_pacienta : int = field(default=0)  # Za vsako polje povemo tip in privzeto vrednost
    ime_pacienta : str = field(default="")
    uporabnisko_ime : str = field(default="")
    geslo_hash: str = field(default="")
    datum_rojstva: date = field(default_factory=date.today)
    spol: str = field(default="")
    reden: str = field(default="")

# Za posamezno entiteto ponavadi ustvarimo tudi tako imenovan
# DTO (database transfer object) objekt. To izhaja predvsem iz tega,
# da v sami aplikaciji ponavadi želimo prikazati podatke drugače kot so v bazi.
# Dodatno bi recimo želeli narediti kakšen join in vzeti podatek oziroma stolpec iz druge tabele

@dataclass_json
@dataclass
class pacientDto:
    id_pacienta : int = field(default=0)
    ime_pacienta : str = field(default="")
    uporabnisko_ime : str = field(default="")
    pregled : int = field(default=0) # dodatno si shranimo se preglede pacienta
    datum_rojstva: str = field(default=0) 
    spol: str = field(default="")
    reden: str = field(default="")

@dataclass_json
@dataclass
class zdravnik:
    id_zdravnika : int = field(default=0)  
    ime_zdravnika : str = field(default="")
    oddelek : int = field(default=0)

@dataclass_json
@dataclass
class zdravnikDto:    
    id_zdravnika : int = field(default=0)  
    ime_zdravnika : str = field(default="")
    oddelek : int = field(default=0)

@dataclass_json
@dataclass
class oddelek:
    id_oddelka : int = field(default=0)  
    ime_oddelka : str = field(default="")
    lokacija : str = field(default="")

@dataclass_json
@dataclass
class oddelekDto:
    id_oddelka : int = field(default=0)  
    ime_oddelka : str = field(default="")
    lokacija : str = field(default="")

@dataclass_json
@dataclass
class pregledDto:
    id_pregleda : int = field(default=0)  
    datum : date = field(default_factory=date.today)
    cas : time = field(default_factory=date.today)
    opis : str = field(default="")
    pacient : int = field(default=0)
    zdravnik : int = field(default=0)
    ime_zdravnika: str = field(default="")
    ime_oddelka: str = field(default="")

@dataclass_json
@dataclass
class pregled:
    id_pregleda : int = field(default=0)  
    datum : date = field(default_factory=date.today)
    cas : time = field(default_factory=lambda: time(0, 0))
    opis : str = field(default="")
    pacient : int = field(default=0)
    zdravnik : int = field(default=0)
    

@dataclass_json
@dataclass
class Uporabnik:
    username: str = field(default="")
    password_hash: str = field(default="")

@dataclass
class UporabnikDto:
    username: str = field(default="")


@dataclass_json
@dataclass
class lokacija:
    id_lokacije: int = field(default=0)
    naslov: str = field(default="")
    