from Data.repository import Repo
from Data.models import *
from typing import List
from random import randint

# datoteka za delo s pregledi

class PreglediService:
    def __init__(self) -> None:
        self.repo = Repo()

    def dobi_pacienta(self, id_pacienta) -> pacient:
        return self.repo.dobi_pacienta(id_pacienta)

    def dobi_zdravnika(self, id_zdravnika) -> zdravnik:
        return self.repo.dobi_zdravnika(id_zdravnika)
    
    def dobi_preglede(self) -> List[pregled]:
        return self.repo.dobi_preglede()
    
    def dobi_pregled(self, id_pregleda) -> pregled:
        return self.repo.dobi_pregled(id_pregleda)
    
    def dobi_preglede_pacient(self, id_pacienta) -> List[pregled]:
        return self.repo.dobi_preglede_pacient(id_pacienta)
    
    def dobi_preglede_pacient_dto(self, id_pacienta) -> List[pregled]:
        return self.repo.dobi_preglede_pacient_dto(id_pacienta)
    
    def dobi_preglede_dto(self) -> List[pregled]:
        return self.repo.dobi_preglede_dto()
    
    def dobi_oddelke(self) -> List[oddelek]:
        return self.repo.dobi_oddelke()

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
    
    def dobi_zdravnike_po_oddelkih(self) -> List[zdravnikDto]:
        return self.repo.dobi_zdravnike_po_oddelkih()
    
    def naredi_pregled(self, uporabnisko_ime: str, id_zdravnika: int, opis: str, datum: str, termin: str) -> None:
        # dobimo id pacienta
        id_pacienta = self.repo.dobi_id_pacienta(uporabnisko_ime)

        # naredimo pregled
        nov_pregled = pregled(
            id_pregleda=randint(10000000, 99999999),  # naključno generirano ID pregleda
            datum=datum,
            cas=termin,
            opis=opis,
            pacient=id_pacienta,
            zdravnik=id_zdravnika
        )

        self.repo.dodaj_pregled(nov_pregled)

    def dobi_oddelek(self, id_oddelka: int) -> str:
        oddelek = self.repo.dobi_oddelek(id_oddelka)
        return oddelek 
    
    def dobi_naslov(self, id_lokacije: int) -> str:
        return self.repo.dobi_naslov(id_lokacije)


        