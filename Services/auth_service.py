from Data.repository import Repo
from Data.models import *
import bcrypt
from typing import Union


class AuthService:
    repo : Repo
    def __init__(self):
        self.repo = Repo()

    def obstaja_uporabnik(self, uporabnik: str) -> bool:
        try:
            user = self.repo.dobi_uporabnika(uporabnik)
            return True
        except:
            return False
        
    def prijavi_uporabnika(self, uporabnik: str, geslo: str) -> Union[UporabnikDto, bool]:

        # dobimo uporabnika (pacienta) iz baze
        pacient = self.repo.dobi_uporabnika(uporabnik)
        # ustvarimo hash iz gesla, ki ga je vpisal uporabnik
        geslo_bytes = geslo.encode('utf-8')
        # preverimo, če je geslo pravilno
        success = bcrypt.checkpw(geslo_bytes, pacient.geslo_hash.encode('utf-8'))

        if success:
            return UporabnikDto(username=pacient.uporabnisko_ime)
        
        return False
        

       

       

        
