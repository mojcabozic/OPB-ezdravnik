import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki
import Data.auth_public as auth
import datetime
import os
from collections import defaultdict

from Data.models import *
from typing import List

# Preberemo port za bazo iz okoljskih spremenljivk
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

# V tej datoteki bomo implementirali razred Repo, ki bo vseboval metode za delo z bazo.

class Repo:
    def __init__(self):
        # Ko ustvarimo novo instanco, definiramo objekt za povezavo in cursor
        self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
        self.conn.set_client_encoding('UTF8')
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
            SELECT 
                p.id_pregleda, 
                p.datum, 
                p.cas, 
                p.opis,
                p.pacient,          
                p.zdravnik, 
                o.ime_oddelka
            FROM pregled p
            JOIN zdravnik z ON p.zdravnik = z.id_zdravnika
            JOIN oddelek o ON z.oddelek = o.id_oddelka
            WHERE p.id_pregleda = %s
        """, (id_pregleda,))
        
        return pregledDto.from_dict(self.cur.fetchone())
        
    
    def dobi_preglede_pacient_dto(self, id_pacienta: int) -> List[pregledDto]:
        self.cur.execute("""
            SELECT 
                p.id_pregleda, 
                p.datum, 
                p.cas, 
                p.opis,
                p.pacient,          
                p.zdravnik,
                z.ime_zdravnika AS ime_zdravnika, 
                o.ime_oddelka
            FROM pregled p
            JOIN zdravnik z ON p.zdravnik = z.id_zdravnika
            JOIN oddelek o ON z.oddelek = o.id_oddelka
            WHERE p.pacient = %s
            ORDER BY p.datum ASC
        """, (id_pacienta,))
        
        a = self.cur.fetchall()
        pregledi = [pregledDto.from_dict(t) for t in a]
        return pregledi
    
    def dobi_zdravnike(self) -> List[zdravnik]:
        self.cur.execute("""
            SELECT id_zdravnika, ime_zdravnika, oddelek
            FROM zdravnik
        """)
        
        # rezultate querya pretovrimo v python seznam objektov (zdravnikov)
       # tt = [t for t in self.cur.fetchall()]
        zdravniki = [zdravnik.from_dict(t) for t in self.cur.fetchall()]
        return zdravniki
    
    def dobi_zdravnika(self, id_zdravnika: str) -> zdravnik:
        self.cur.execute("""
            SELECT id_zdravnika, ime_zdravnika, oddelek
            FROM zdravnik
            WHERE id_zdravnika = %s
        """, (id_zdravnika,))
         
        z = zdravnik.from_dict(self.cur.fetchone())
        return z

    def dobi_zdravnike_dto(self) -> List[zdravnikDto]:
        self.cur.execute("""
            SELECT id_zdravnika, ime_zdravnika, oddelek
            FROM zdravnik 
                         
        """)
        
        # rezultate querya pretovrimo v python seznam objektov (transkacij)
       # tt = [t for t in self.cur.fetchall()]
        zdravniki = [zdravnikDto.from_dict(t) for t in self.cur.fetchall()]
        return zdravniki
    
    def dobi_pacienta(self, id_pacienta : str) -> pacient:
        self.cur.execute("""
            SELECT id_pacienta, ime_pacienta, datum_rojstva, spol, reden
            FROM pacient
            WHERE id_pacienta = %s
        """, (id_pacienta,))
         
        p = pacient.from_dict(self.cur.fetchone())
        return p
    
    def dobi_id_pacienta(self, uporabnisko_ime : str) -> str: # iz uporabniskega imena paceinta dobimo njegov id
        self.cur.execute("""
            SELECT id_pacienta
            FROM pacient
            WHERE uporabnisko_ime = %s
        """, (uporabnisko_ime,))

        return self.cur.fetchone()[0]


    def dobi_preglede_pacient(self, id_pacienta : int) -> List[pregled]:
        
        self.cur.execute("""
            SELECT id_pregleda, datum, cas, opis, pacient, zdravnik
            FROM pregled
            WHERE pacient = %s
            ORDER BY datum ASC
        """, (id_pacienta,))
        
        # rezultate querya pretovrimo v python seznam objektov (pregledov)
        a = self.cur.fetchall()
        pregledi = [pregled.from_dict(t) for t in a]
        return pregledi
    
    def dodaj_pregled(self, t : pregled):
        self.cur.execute("""
            INSERT into pregled(id_pregleda, datum, cas, opis, pacient, zdravnik)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (t.id_pregleda, t.datum, t.cas, t.opis, t.pacient, t.zdravnik))
        self.conn.commit()

    def dobi_oddelke(self) -> oddelek:
        self.cur.execute("""
            SELECT id_oddelka, ime_oddelka, lokacija
            FROM oddelek
        """)
         
        oddelki = [oddelek.from_dict(t) for t in self.cur.fetchall()]
        return oddelki
    
    def dobi_oddelek(self, id_oddelka: str) -> oddelek:
        self.cur.execute("""
            SELECT id_oddelka, ime_oddelka, lokacija
            FROM oddelek
            WHERE id_oddelka = %s
        """, (id_oddelka,))
         
        o = oddelek.from_dict(self.cur.fetchone())
        return o

    def dobi_uporabnika(self, uporabnisko_ime : str) -> pacient:
        self.cur.execute("""
            SELECT uporabnisko_ime, geslo_hash
            FROM pacient
            WHERE uporabnisko_ime = %s
        """, (uporabnisko_ime,))

        p = pacient.from_dict(self.cur.fetchone())
        return p
    
    def dobi_zdravnike_po_oddelkih(self) -> dict[str, List[zdravnikDto]]:
        self.cur.execute("""
            SELECT o.id_oddelka, z.id_zdravnika, z.ime_zdravnika
            FROM oddelek o
            LEFT JOIN zdravnik z ON o.id_oddelka = z.oddelek
            
        """)
        
        slovar = defaultdict(list)
        for row in self.cur.fetchall():
            id_oddelka, id_zdravnika, ime_zdravnika = row
            zdravnik_dto = zdravnikDto(id_zdravnika=id_zdravnika, ime_zdravnika=ime_zdravnika, oddelek=id_oddelka)
            slovar[id_oddelka].append(zdravnik_dto)
        
        return slovar
    
    def dobi_naslov(self, id_lokacije: str) -> str:
        self.cur.execute("""
            SELECT naslov
            FROM lokacija
            WHERE id_lokacije = %s
        """, (id_lokacije,))
        
        return self.cur.fetchone()[0]  # vrne naslov kot string
    
