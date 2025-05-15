import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki
import Data.auth_public as auth
import datetime
import os

from Data.models import pacient, zdravnik, pacientDto, pregled, oddelek, oddelekDto, zdravnikDto, pregledDto
from typing import List

# Preberemo port za bazo iz okoljskih spremenljivk
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

## V tej datoteki bomo implementirali razred Repo, ki bo vseboval metode za delo z bazo.

class Repo:
    def __init__(self):
        # Ko ustvarimo novo instanco definiramo objekt za povezavo in cursor
        self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def dobi_preglede(self) -> List[pregled]:
        self.cur.execute("""
            SELECT id_pregleda, datum, cas, opis
            FROM pregled
            Order by datum desc
        """)
        
        # rezultate querya pretovrimo v python seznam objektov (transkacij)
        pregledi = [pregledi.from_dict(t) for t in self.cur.fetchall()]
        return pregledi
    
    def dobi_pregled(self, id_pregleda: str) -> pregled:
         self.cur.execute("""
            SELECT id_pregleda, datum, cas, opis
            FROM transakcija
            Where id_pregleda = %s
        """, (id_pregleda,))
         
         t = pregled.from_dict(self.cur.fetchone())
         return t

    
    def dobi_preglede_dto(self) -> List[pregledDto]:
        self.cur.execute("""
            SELECT t.id_pregleda, p.pacient as pacient, t.datum, t.cas, t.zdravnik, t.opis
            FROM pregled t 
            left join racun r on t.racun = r.stevilka
            left join oseba o on o.emso = r.lastnik
            Order by t.datum desc
        """)

        pregledi = [pregledDto.from_dict(t) for t in self.cur.fetchall()]
        return pregledi
    
    def dobi_zdravnike(self) -> List[zdravnik]:
        self.cur.execute("""
            SELECT id_zdravika, ime_zdravnika, oddelek
            FROM zdravnik
        """)
        
        # rezultate querya pretovrimo v python seznam objektov (zdravnikov)
       # tt = [t for t in self.cur.fetchall()]
        zdravniki = [zdravnik.from_dict(t) for t in self.cur.fetchall()]
        return zdravniki
    
    def dobi_zdravnika(self, id_zdravnika: str) -> zdravnik:
        self.cur.execute("""
            SELECT id_zdravika, ime_zdravnika, oddelek
            FROM zdravnik
            WHERE id_zdravnika = %s
        """)
         
        z = zdravnik.from_dict(self.cur.fetchone())
        return z

    def dobi_zdravnike_dto(self) -> List[zdravnikDto]:
        self.cur.execute("""
            SELECT id_zdravika, ime_zdravnika, oddelek
            FROM zdravnik 
                         
        """)
        
        # rezultate querya pretovrimo v python seznam objektov (transkacij)
       # tt = [t for t in self.cur.fetchall()]
        zdravniki = [zdravnikDto.from_dict(t) for t in self.cur.fetchall()]
        return zdravniki
    
    def dobi_pacienta(self, id_pacienta : str) -> pacient:
        self.cur.execute("""
            SELECT id_pacienta, ime_pacienta, starost, spol, reden
            FROM pacient
        """)
         
        p = pacient.from_dict(self.cur.fetchone())
        return p
    
    def dobi_preglede_pacient(self, pacient : str) -> List[pregled]:
        pregled = self.dobi_pregled(id)
        self.cur.execute("""
            SELECT id_pregleda, datum, cas, opis, pacient, zdravnik
            FROM pregled
            WHERE pacient = %s
        """, (pregled.id_pregleda,))
        
        # rezultate querya pretovrimo v python seznam objektov (transkacij)
        pregledi = [pregled.from_dict(t) for t in self.cur.fetchall()]
        return pregledi
    
    def dodaj_pregled(self, t : pregled):
        self.cur.execute("""
            INSERT into pregled(datum, cas, opis, pacient, zdravnik)
            VALUES (%s, %s, %s, %s, %s)
            """, (t.datum, t.cas, t.opis, t.pacient, t.zdravnik))
        self.conn.commit()

    def posodobi_pregled(self, t : pregled):
        self.cur.execute("""
            Update pregled set datum = %s,  cas=%s, opis = %s, pacient = %s, zdravnik = %s where id_pregleda = %s
            """, (t.datum, t.cas, t.opis, t.zdravnik, t.pacient, t.id_pregleda))
        self.conn.commit()

