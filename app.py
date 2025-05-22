from functools import wraps
from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user

from Services.transakcije_service import TransakcijeService
from Services.auth_service import AuthService
import os

# Ustvarimo instance servisov, ki jih potrebujemo. 
# Če je število servisov veliko, potem je service bolj smiselno inicializirati v metodi in na
# začetku datoteke (saj ne rabimo vseh servisov v vseh metodah!)

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
        return template("prijava.html",uporabnik=None, napaka="Potrebna je prijava!")
        
    return decorated

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='Presentation/static')


@get('/')
@cookie_required
def index():
    """
    Domača stran s pregledi uporabnika (profil)
    """   
  
    pregledi_dto = service.dobi_preglede_pacient()  
        
    return template_user('profil.html', pregledi = pregledi_dto)

@get('/pregled')
@cookie_required
def index():
    """
    Stran s podatki o pregledu
    """   
  
    pregled = service.dobi_pregled()
    return template_user('pregled.html', pregled = pregled)



@get('/dodaj_pregled')
def dodaj_pregled():
    """
    Stran za dodajanje pregleda.  """
    oddelki = service.dobi_oddelke()
    return template_user('dodaj_pregled.html', oddelki=oddelki)


@post('/dodaj_pregled')
def dodaj_pregled_post():
    # Preberemo podatke iz forme (oddelek, zdravnik, datum, termin, opis)

    oddelek = int(request.forms.get('oddelek'))
    zdravnik = float(request.forms.get('zdravnik'))
    opis = request.forms.get('opis')
    datum = request.forms.get('datum')
    termin = request.forms.get('termin')

    service.naredi_pregled(oddelek, zdravnik, opis, datum, termin)
    
    
    redirect(url('/'))



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
    
    return template('prijava.html', uporabnik=None, napaka=None)


if __name__ == "__main__":
   
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)