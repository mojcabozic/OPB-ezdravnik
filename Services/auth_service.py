from Data.repository import Repo
from Data.models import *
import bcrypt
from typing import Union


class AuthService:
    repo : Repo
    def __init__(self):
        self.repo = Repo()

    def dodaj_uporabnika(self, uporabnik: str, rola: str, geslo: str) -> UporabnikDto:

        # zgradimo hash za geslo od uporabnika

        # Najprej geslo zakodiramo kot seznam bajtov
        bytes = geslo.encode('utf-8')
  
        # Nato ustvarimo salt
        salt = bcrypt.gensalt()
        
        # In na koncu ustvarimo hash gesla
        password_hash = bcrypt.hashpw(bytes, salt)

        # Sedaj ustvarimo objekt Uporabnik in ga zapišemo bazo

        u = Uporabnik(
            username=uporabnik,
            role=rola,
            password_hash=password_hash.decode(),
            last_login= date.today().isoformat()
        )

        self.repo.dodaj_uporabnika(u)

        return UporabnikDto(username=uporabnik, role=rola)

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