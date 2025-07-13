from Data.repository import Repo
from Data.models import *
from typing import List

# datoteka za delo s pregledi

class PreglediService:
    def __init__(self) -> None:
        self.repo = Repo()

    def dobi_pacienta(self) -> pacient:
        return self.repo.dobi_pacienta()
    
    def dobi_preglede(self) -> List[pregled]:
        return self.repo.dobi_preglede()
    
    def dobi_pregled(self, id_pregleda) -> pregled:
        return self.repo.dobi_pregled(id_pregleda)
    
    def dobi_preglede_pacient(self, id_pacienta) -> List[pregled]:
        return self.repo.dobi_preglede_pacient(id_pacienta)
    
    def dobi_preglede_dto(self) -> List[pregled]:
        return self.repo.dobi_preglede_dto()
    

    def dodaj_pregled_pacient(self, p: pacient, z: zdravnik, datum: str, cas: str, opis: str) -> None:
        # naredimo objekt za pregled; potrebujemo id pacienta in zdravnika

        pr = pregled(
            datum = datum,
            cas = cas,
            opis = opis,
            pacient = p.id_pacienta,
            zdravnik = z.id_zdravnika
        )

        self.repo.dodaj_pregled(pr)

    def dobi_id_pacienta(self, uporabnisko_ime: str) -> int:
        return self.repo.dobi_id_pacienta(uporabnisko_ime)


        