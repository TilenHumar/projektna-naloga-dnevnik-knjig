from io import SEEK_CUR
from sys import api_version, path
import bottle
from datetime import date
from model import Stanje, Knjiga, Uporabnik



IME_DATOTEKE = 'stanje.json'
PISKOTEK_UPORABNISKO_IME = "uporabnisko_ime"
SKRIVNOST ="moja_skrivnost"


@bottle.get("/")
def osnovna_stran():
    uporabnik = trenutni_uporabnik()
    return bottle.template(
        "osnovna_stran.html",
        trenutne_knjige = uporabnik.stanje.trenutne_knjige,
        prebrane_knjige = uporabnik.stanje.prebrane_knjige,
        stevilo_trenutnih = uporabnik.stanje.stevilo_trenutnih(),
        stevilo_prebranih = uporabnik.stanje.stevilo_prebranih(),
        stevilo_leposlovnih = uporabnik.stanje.stevilo_leposlovnih(),
        stevilo_neleposlovnih = uporabnik.stanje.stevilo_neleposlovnih(),
        stevilo_cez_rok = uporabnik.stanje.stevilo_cez_rok(),
        seznam_cez_rok = uporabnik.stanje.seznam_cez_rok(),
        uporabnik = uporabnik
        )

@bottle.get("/dodaj_knjigo/")
def dodaj_knjigo_get():
    trenutni_uporabnik()
    return bottle.template("dodaj_knjigo.html", napake={}, polja={})


@bottle.post("/dodaj_knjigo/")
def dodaj_knjigo_post():
    uporabnik = trenutni_uporabnik()
    naslov = bottle.request.forms.getunicode("naslov")
    avtor = bottle.request.forms.getunicode("avtor")
    zvrst = bottle.request.forms.getunicode("zvrst")
    izposojena_ali_kupljena = bottle.request.forms.getunicode("izposojena_ali_kupljena")
    rok_vracila = bottle.request.forms.getunicode("rok_vracila")
    if izposojena_ali_kupljena == "kupljena":
        rok_vracila = "/"
    knjiga = Knjiga(naslov, avtor, zvrst, izposojena_ali_kupljena, rok_vracila)
    uporabnik.stanje.dodaj_knjigo(knjiga)
    shrani_stanje(uporabnik)
    bottle.redirect("/")

@bottle.post("/odstrani_knjigo/")
def odstrani_knjigo():
    uporabnik = trenutni_uporabnik()
    indeks = int(bottle.request.forms.getunicode("indeks"))
    knjiga = uporabnik.stanje.trenutne_knjige[indeks]
    uporabnik.stanje.odstrani_knjigo(knjiga)
    shrani_stanje(uporabnik)
    bottle.redirect("/")

@bottle.get("/oceni_knjigo/")
def dodaj_knjigo_get():
    trenutni_uporabnik()
    return bottle.template("oceni_knjigo.html", napake={}, polja={})

@bottle.post("/preberi_knjigo/")
def preberi_knjigo():
    uporabnik = trenutni_uporabnik()
    indeks = int(bottle.request.forms.getunicode("indeks"))
    knjiga = uporabnik.stanje.trenutne_knjige[indeks]
    uporabnik.stanje.preberi_knjigo(knjiga)
    shrani_stanje(uporabnik)
    bottle.redirect("/")

def shrani_stanje(uporabnik):
    uporabnik.shrani_v_datoteko()

def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie(PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST)
    if uporabnisko_ime:
        try:
            return Uporabnik.preberi_iz_datoteke(uporabnisko_ime)
        except FileNotFoundError:
            return Uporabnik(uporabnisko_ime, Stanje())
    else:
        bottle.redirect("/prijava/")

@bottle.get("/prijava/")
def prijava_get():
    return bottle.template("prijava.html", napaka=None)

@bottle.post("/odjava/")
def odjava_post():
    bottle.response.delete_cookie(PISKOTEK_UPORABNISKO_IME, path="/")
    bottle.redirect("/")

@bottle.post("/prijava/")
def prijava_post():
    geslo = bottle.request.forms.getunicode("geslo")
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    if geslo == "geslo":
        bottle.response.set_cookie(PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST)
        bottle.redirect("/")
    else:
        return bottle.template("prijava.html", napaka="Vnesli ste napačno geslo, prosimo poskusite še enkrat.")


@bottle.error(404)
def error_404(error):
    return "Ta stran ne obstaja!"

bottle.run(reloader=True, debug=True)