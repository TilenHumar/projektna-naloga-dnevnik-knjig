import bottle
from datetime import date
from model import Stanje, Knjiga, Uporabnik

PISKOTEK_UPORABNISKO_IME = "uporabnisko_ime"
SKRIVNOST ="moja_skrivnost"

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

#prikaz prijavne strani
@bottle.get("/prijava/")
def prijava_get():
    return bottle.template("prijava.html")

#prijava uporabnika
@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    bottle.response.set_cookie(PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST)
    bottle.redirect("/")

#odjava uporabnika
@bottle.post("/odjava/")
def odjava_post():
    bottle.response.delete_cookie(PISKOTEK_UPORABNISKO_IME, path="/")
    bottle.redirect("/")

@bottle.error(404)
def error_404(error):
    return "Ta stran ne obstaja!"

#osnovna stran
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
        uporabnik = uporabnik,
        uporabnisko_ime = uporabnik.uporabnisko_ime
        )

#prikaži stran za dodajanje knjig
@bottle.get("/dodaj_knjigo/")
def dodaj_knjigo_get():
    uporabnik = trenutni_uporabnik()
    return bottle.template("dodaj_knjigo.html", polja={}, uporabnik = uporabnik)

#dodajanje knjig
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
    if naslov:
        if avtor:
            if zvrst == "leposlovje" or zvrst == "neleposlovje":
                if izposojena_ali_kupljena == "izposojena" or izposojena_ali_kupljena == "kupljena":
                    if (izposojena_ali_kupljena == "izposojena" and rok_vracila != None) or izposojena_ali_kupljena == "kupljena":
                        knjiga = Knjiga(naslov, avtor, zvrst, izposojena_ali_kupljena, rok_vracila)
                        uporabnik.stanje.dodaj_knjigo(knjiga)
                        shrani_stanje(uporabnik)
                        bottle.redirect("/")
                    else:
                        return bottle.template("opozorilo_datum_vracila.html", uporabnik = uporabnik)
                else:
                    return bottle.template("opozorilo_kupljena_ali_izposojena.html", uporabnik = uporabnik)
            else:
                return bottle.template("opozorilo_zvrst.html", uporabnik = uporabnik)
        else:
            return bottle.template("opozorilo_avtor.html", uporabnik = uporabnik)
    else:
        return bottle.template("opozorilo_naslov.html", uporabnik = uporabnik)

#odstranjevanje knjig
@bottle.post("/odstrani_knjigo/")
def odstrani_knjigo():
    uporabnik = trenutni_uporabnik()
    indeks = int(bottle.request.forms.getunicode("indeks"))
    knjiga = uporabnik.stanje.trenutne_knjige[indeks]
    uporabnik.stanje.odstrani_knjigo(knjiga)
    shrani_stanje(uporabnik)
    bottle.redirect("/")

#prebiranje knjig
@bottle.post("/preberi_knjigo/")
def preberi_knjigo():
    uporabnik = trenutni_uporabnik()
    indeks = int(bottle.request.forms.getunicode("indeks"))
    knjiga = uporabnik.stanje.trenutne_knjige[indeks]
    uporabnik.stanje.preberi_knjigo(knjiga)
    shrani_stanje(uporabnik)
    bottle.redirect("/")

bottle.run()