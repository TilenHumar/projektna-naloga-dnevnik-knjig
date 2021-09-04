from sys import api_version
import bottle
from datetime import date
from model import Stanje, Knjiga



IME_DATOTEKE = 'stanje.json'
try:
    moj_model = Stanje.preberi_iz_datoteke(IME_DATOTEKE)
except FileNotFoundError:
    moj_model = Stanje()

@bottle.get("/")
def osnovna_stran():
    return bottle.template(
        "osnovna_stran.html",
        trenutne_knjige = moj_model.trenutne_knjige,
        prebrane_knjige = moj_model.prebrane_knjige,
        stevilo_trenutnih = len(moj_model.trenutne_knjige),
        stevilo_prebranih = len(moj_model.prebrane_knjige),
        stevilo_leposlovnih = moj_model.stevilo_leposlovnih(),
        stevilo_neleposlovnih = moj_model.stevilo_neleposlovnih(),
        stevilo_cez_rok = moj_model.stevilo_cez_rok()
        )

@bottle.get("/dodaj_knjigo/")
def dodaj_knjigo_get():
    return bottle.template("dodaj_knjigo.html", napake={}, polja={})


@bottle.post("/dodaj_knjigo/")
def dodaj_knjigo_post():
    naslov = bottle.request.forms.getunicode("naslov")
    avtor = bottle.request.forms.getunicode("avtor")
    zvrst = bottle.request.forms.getunicode("zvrst")
    izposojena_ali_kupljena = bottle.request.forms.getunicode("izposojena_ali_kupljena")
    if izposojena_ali_kupljena == "izposojena":
        rok_vracila = bottle.request.forms.getunicode("rok_vracila")
    if izposojena_ali_kupljena == "kupljena":
        rok_vracila = "/"
    knjiga = Knjiga(naslov, avtor, zvrst, izposojena_ali_kupljena, rok_vracila)
    moj_model.dodaj_knjigo(knjiga)
    moj_model.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect("/")

@bottle.post("/odstrani_knjigo/")
def odstrani_knjigo():
    indeks = int(bottle.request.forms.getunicode("indeks"))
    knjiga = moj_model.trenutne_knjige[indeks]
    moj_model.odstrani_knjigo(knjiga)
    moj_model.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect("/")

@bottle.get("/oceni_knjigo/")
def dodaj_knjigo_get():
    return bottle.template("oceni_knjigo.html", napake={}, polja={})

@bottle.post("/preberi_knjigo/")
def preberi_knjigo():
    indeks = int(bottle.request.forms.getunicode("indeks"))
    knjiga = moj_model.trenutne_knjige[indeks]
    moj_model.preberi_knjigo(knjiga)
    moj_model.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect("/")

@bottle.error(404)
def error_404(error):
    return "Ta stran ne obstaja!"

bottle.run(reloader=True, debug=True)