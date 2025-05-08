from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime

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
