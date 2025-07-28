from functools import wraps
from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user

from Services.pregledi_service import PreglediService
from Services.auth_service import AuthService
import os
import json
import datetime

# Ustvarimo instance servisov, ki jih potrebujemo. 

service = PreglediService()
auth = AuthService()


# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)

def cookie_required(f):
    """
    Dekorator, ki zahteva veljaven piškotek. Če piškotka ni, uporabnika preusmeri na stran za prijavo.
    """
    @wraps(f)
    def decorated( *args, **kwargs):
        cookie = request.get_cookie("uporabnik")
        if cookie:
            return f(*args, **kwargs)
        redirect(url('/prijava'))
        
    return decorated

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='Presentation/static')


@get('/')
@cookie_required
def index():
    """
    Domača stran s pregledi uporabnika (profil).
    """   
    # iz piškotka dobimo uporabniško ime prijavljenega pacienta
    uporabnisko_ime = request.get_cookie("uporabnik")

    # iz uporabniškega imena dobimo id pacienta
    id_pacienta = service.dobi_id_pacienta(uporabnisko_ime)
   
    pregledi_dto = service.dobi_preglede_pacient_dto(id_pacienta) 

    ime_pacienta = service.dobi_pacienta(id_pacienta).ime_pacienta
    datum_rojstva = service.dobi_pacienta(id_pacienta).datum_rojstva
    spol = service.dobi_pacienta(id_pacienta).spol
    reden = service.dobi_pacienta(id_pacienta).reden 
    danes = datetime.date.today()
    prihajajoci_pregledi = [p for p in pregledi_dto if p.datum >= danes]
   
    return template_user('profil.html', pregledi = prihajajoci_pregledi, uporabnisko_ime=uporabnisko_ime, ime_pacienta=ime_pacienta, datum_rojstva=datum_rojstva, spol=spol, reden=reden)



@get('/pregled/<id_pregleda>')
@cookie_required
def pregled(id_pregleda):
    """
    Stran s podatki o posameznem pregledu
    """   
  
    pregled = service.dobi_pregled(id_pregleda)
    # pridobimo podatke o pacientu, zdravniku, oddelku, lokaciji
    id_pacienta = pregled.pacient
    id_zdravnika = pregled.zdravnik
  
    id_oddelka = service.dobi_zdravnika(id_zdravnika).oddelek

    ime_pacienta = service.dobi_pacienta(id_pacienta).ime_pacienta
    ime_zdravnika = service.dobi_zdravnika(id_zdravnika).ime_zdravnika
    id_lokacije = service.dobi_oddelek(id_oddelka).lokacija
    lokacija = service.dobi_naslov(id_lokacije)
    


    return template_user('pregled.html', pregled = pregled, ime_pacienta=ime_pacienta, ime_zdravnika=ime_zdravnika, lokacija=lokacija)


@get('/dodaj_pregled')
def dodaj_pregled():
    """
    Stran za dodajanje pregleda.  
    """
    oddelki = service.dobi_oddelke()
    # dobimo slovar oddelkov z zdravniki, ki so v teh oddelkih
    zdravniki_po_oddelkih = service.dobi_zdravnike_po_oddelkih()
    zdravniki_po_oddelkih_json = json.dumps({x:[y.to_dict() for y in zdravniki_po_oddelkih[x]] for x in zdravniki_po_oddelkih})
    return template_user('dodaj_pregled.html', oddelki=oddelki, zdravniki_po_oddelkih_json=zdravniki_po_oddelkih_json)


@post('/dodaj_pregled')
def dodaj_pregled_post():
    # Preberemo podatke iz forme (oddelek, zdravnik, datum, termin, opis)
    oddelek = request.forms.get('id_oddelka')
    zdravnik = float(request.forms.get('id_zdravnika'))
    opis = request.forms.opis
    datum = request.forms.get('datum')
    termin = request.forms.get('termin')

    # iz piškotka dobimo podatek o prijavljenem uporabniku
    uporabniško_ime = request.get_cookie("uporabnik")
    id_pacienta = service.dobi_id_pacienta(uporabniško_ime)
    print(f"{opis} v filu app.py")
    service.naredi_pregled(uporabniško_ime, zdravnik, opis, datum, termin)

    # pridobimo podatke o pacientu, zdravniku, oddelku, lokaciji
    ime_pacienta = service.dobi_pacienta(id_pacienta).ime_pacienta
    ime_zdravnika = service.dobi_zdravnika(zdravnik).ime_zdravnika
    id_lokacije = service.dobi_oddelek(oddelek).lokacija
    lokacija = service.dobi_naslov(id_lokacije)
    ime_oddelka = service.dobi_oddelek(oddelek).ime_oddelka
    datum_obj = datetime.datetime.strptime(datum, '%d.%m.%Y') # klicemo datetime.datetime, ker imamo namesto from datetime import datetime samo import datetime (prvo je module, drugo class)
    termin_obj = datetime.datetime.strptime(termin, '%H:%M') 
    
    return template_user('uspesno_narocanje.html', ime_pacienta=ime_pacienta, ime_zdravnika=ime_zdravnika, datum=datum_obj, termin=termin_obj, ime_oddelka=ime_oddelka, lokacija=lokacija)

@get('/opravljeni_pregledi')
def opravljeni_pregledi():
    """
    Stran, na kateri se nahajajo opravljeni pregledi.  
    """
    uporabniško_ime = request.get_cookie("uporabnik")
    id_pacienta = service.dobi_id_pacienta(uporabniško_ime)
    ime_pacienta = service.dobi_pacienta(id_pacienta).ime_pacienta

    preglediDto = service.dobi_preglede_pacient_dto(id_pacienta)
    pregledi = service.dobi_preglede_pacient(id_pacienta)
    danes = datetime.date.today()
    opravljeni_preglediDto = [p for p in preglediDto if p.datum < danes]
    opravljeni_pregledi = [p for p in pregledi if p.datum < danes]

    return template_user('opravljeni_pregledi.html', preglediDto=opravljeni_preglediDto, pregledi = opravljeni_pregledi, ime_pacienta=ime_pacienta)


@get('/prijava')
def get_prijava():
    """
    Prikaže stran za prijavo uporabnika.
    """
    # če je uporabnik že prijavljen, ga preusmeri na domačo stran
    if request.get_cookie("uporabnik"):
        redirect(url('/'))

    return template("prijava.html", uporabnik=None, napaka=None)



@post('/prijava')
def prijava():
    """
    Prijavi uporabnika v aplikacijo. Če je prijava uspešna, ustvari piškotke o uporabniku.
    Drugače sporoči, da je prijava neuspešna.
    """
    username = request.forms.get('username')
    password = request.forms.get('password')

    if not auth.obstaja_uporabnik(username):
        return template("prijava.html", napaka="Uporabnik s tem imenom ne obstaja.")

    prijava = auth.prijavi_uporabnika(username, password)
    if prijava:
        response.set_cookie("uporabnik", username)
        
        # redirect v večino primerov izgleda ne deluje
        redirect(url('/'))

        # Uporabimo kar template, kot v sami "index" funkciji
        
    else:
        return template("prijava.html", uporabnik=None, napaka="Neuspešna prijava. Napačno geslo ali uporabniško ime.")

@get('/odjava')
def odjava():
    """
    Odjavi uporabnika iz aplikacije. Pobriše piškotke o uporabniku.
    """
    
    response.delete_cookie("uporabnik")
    
    redirect(url('/'))


if __name__ == "__main__":
   
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)