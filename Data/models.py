from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime

<<<<<<< HEAD
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
    

=======
# V tej datoteki definiramo vse podatkovne modele, ki jih bomo uporabljali v aplikaciji
# Pazi na vrstni red anotacij razredov!

@dataclass_json
@dataclass
class Oddelek:
    id_oddelka: int = field(default=0)
    ime_oddelka: str = field(default="")
    lokacija: str = field(default="")

@dataclass_json
@dataclass
class OddelekDto:
    id_oddelka: int = field(default=0)
    ime_oddelka: str = field(default="")
    lokacija: str = field(default="")

@dataclass_json
@dataclass
class Zdravnik:
    id_zdravnika: int = field(default=0)
    ime_zdravnika: str = field(default="")
    oddelek_id: int = field(default=0)

@dataclass_json
@dataclass
class ZdravnikDto:
    id_zdravnika: int = field(default=0)
    ime_zdravnika: str = field(default="")
    oddelek_id: int = field(default=0)   

@dataclass_json
@dataclass
class Pacient:
    ime_pacienta: str = field(default="")
    id_pacienta: int = field(default=0)
    email: str = field(default="")
    starost: int = field(default=0)
    spol: str = field(default="")
    redno: bool = field(default=False)

@dataclass_json
@dataclass
class PacientDto:
    ime_pacienta: str = field(default="")
    id_pacienta: int = field(default=0)
    emso : int = field(default = "")
    email: str = field(default="")
    geslo: str = field(default="")
    starost: int = field(default=0)
    spol: str = field(default="")
    redno: bool = field(default=False)

@dataclass_json
@dataclass
class Pregled:
    id_pregleda: int = field(default=0)
    datum_pregleda: datetime = field(default_factory=datetime.now)
    termin_pregleda: str = field(default="")  
    pacient_id: int = field(default=0)       
    zdravnik_id: int = field(default=0)       


@dataclass_json
@dataclass
class PregledDto:
    id_pregleda: int = field(default=0)
    ime_pacienta: str = field(default="")
    ime_zdravnika: str = field(default="")
    datum_pregleda: datetime = field(default_factory=datetime.now)
    opis_tezave: str = field(default="")
    termin_pregleda: str = field(default="")
>>>>>>> c67a7a0dd4bcccac875e22dc23175318251b8b0e
