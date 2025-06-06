from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime

# definiramo razrede / podatkovne modele

@dataclass_json
@dataclass
class pacient:
    id_pacienta : int = field(default=0)  # Za vsako polje povemo tip in privzeto vrednost
    ime_pacienta : str = field(default="")
    uporabnisko_ime : str = field(default="")
    starost: int = field(default=0) 
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
    starost: int = field(default=0) 
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
class pregled:
    id_pregleda : int = field(default=0)  
    datum : datetime = field(default=datetime.now)
    cas : str = field(default="")
    opis : str = field(default="")

@dataclass_json
@dataclass
class pregledDto:
    id_pregleda : int = field(default=0)  
    datum : datetime = field(default=datetime.now)
    cas : str = field(default="")
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