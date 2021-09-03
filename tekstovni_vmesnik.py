from model import Stanje, Knjiga

trenutne_knjige_prikaz = []
prebrane_knjige_prikaz = []

IME_DATOTEKE = 'stanje.json'
try:
    moj_model = Stanje.preberi_iz_datoteke(IME_DATOTEKE)
except FileNotFoundError:
    moj_model = Stanje()

class Izgled_pisave:

    ZELENA = "\033[92m"
    RDECA = "\033[91m"
    KREPKO = "\033[1m"
    KONEC = "\033[0m"


def zelena_pisava(niz):
    return Izgled_pisave.ZELENA + str(niz) + Izgled_pisave.KONEC


def rdeca_pisava(niz):
    return Izgled_pisave.RDECA + str(niz) + Izgled_pisave.KONEC


def krepka_pisava(niz):
    return Izgled_pisave.KREPKO + str(niz) + Izgled_pisave.KONEC


def nova_vrstica():
    print("\n")


def tekstovni_vmesnik():
    global konec
    konec = False
    nova_vrstica()
    pozdravi_uporabnika()
    posodobi_prebrane_knjige()
    posodobi_trenutne_knjige()
    nova_vrstica()
    while konec != True:
        prikazi_osnovni_zaslon()


def prikazi_osnovni_zaslon():
    global konec
    ukaz = True
    while ukaz:
        nova_vrstica()
        prikazi_trenutne_knjige()
        nova_vrstica()
        prikazi_knjige_cez_rok()
        nova_vrstica()
        prikazi_prebrane_knjige()
        nova_vrstica()
        print("""
        1) dodaj novo knjigo
        2) odstrani knjigo
        3) preberi knjigo
        4)izhod
        """)
        print("Izberite eno od ponujenih možnosti.")
        ukaz = input(">")
        if ukaz == "1":
            dodaj_knjigo()
        elif ukaz == "2":
            odstrani_knjigo()
        elif ukaz == "3":
            preberi_knjigo()
        elif ukaz == "4":
            moj_model.shrani_v_datoteko(IME_DATOTEKE)
            print("Hvala za uporabo programa, nasvidenje.")
            konec = True
            ukaz = None
        else:
            print("Izberite število med 1 in 4.")


def dodaj_knjigo():
    knjiga = identifikacija_knjige()
    naslov = getattr(knjiga, "naslov")
    avtor = getattr(knjiga, "avtor")
    zvrst = getattr(knjiga, "zvrst")
    izposojena_ali_kupljena = getattr(knjiga, "izposojena_ali_kupljena")
    rok_vracila = getattr(knjiga, "rok_vracila")
    if not moj_model.vsebuje_knjigo(knjiga):
        moj_model.dodaj_knjigo(knjiga)
        trenutne_knjige_prikaz.append(
            (naslov, avtor, zvrst, izposojena_ali_kupljena, rok_vracila)
            )
    else:
        print("To knjigo ste že dodali v seznam.")


def odstrani_knjigo():
    knjiga = identifikacija_knjige()
    naslov = getattr(knjiga, "naslov")
    avtor = getattr(knjiga, "avtor")
    zvrst = getattr(knjiga, "zvrst")
    izposojena_ali_kupljena = getattr(knjiga, "izposojena_ali_kupljena")
    rok_vracila = getattr(knjiga, "rok_vracila")
    if moj_model.vsebuje_knjigo(knjiga):
        moj_model.odstrani_knjigo(knjiga)
        trenutne_knjige_prikaz.remove(
            (naslov, avtor, zvrst, izposojena_ali_kupljena, rok_vracila)
            )
    else:
        print(
            "Te knjige sploh ni v vašem trenutnem seznamu. Ali ste se morda kje zmotili? ")


def preberi_knjigo():
    
    knjiga = identifikacija_knjige()
    naslov = getattr(knjiga, "naslov")
    avtor = getattr(knjiga, "avtor")
    zvrst = getattr(knjiga, "zvrst")
    izposojena_ali_kupljena = getattr(knjiga, "izposojena_ali_kupljena")
    rok_vracila = getattr(knjiga, "rok_vracila")
    if moj_model.vsebuje_knjigo_prebrane(knjiga):
        print("To knjigo ste že prebrali. Odstranjena je z vašega trenutnega seznama in jo lahko vrnete.")
        moj_model.odstrani_knjigo(knjiga)
        trenutne_knjige_prikaz.remove(
            (naslov, avtor, zvrst, izposojena_ali_kupljena, rok_vracila)
            )
    elif moj_model.vsebuje_knjigo(knjiga):
        ocena = input("Ocenite prebrano knjigo, izbirajte med števili med 1 in 5: ")
        moj_model.dodaj_oceno_prebrani(knjiga, ocena)
        moj_model.preberi_knjigo(knjiga)
        trenutne_knjige_prikaz.remove(
            (naslov, avtor, zvrst, izposojena_ali_kupljena, rok_vracila)
            )
        prebrane_knjige_prikaz.append((naslov, avtor, zvrst, ocena)
        )
    else:
        print("Te knjige pa sploh niste brali. Ali ste se morda kje zmotili? ")


def prikazi_trenutne_knjige():
    if moj_model.trenutne_knjige == []:
        print("Trenutno ne berete nobene knjige. Začnite z branjem in svojemu napredku sledite s tem programom.")
    else:
        print("Knjige, ki jih trenutno berete so:")
        for i in trenutne_knjige_prikaz:
            print(i)
        print("Skupno število knjig, ki jih trenutno berete: " +
              str(len(trenutne_knjige_prikaz)))


def pozdravi_uporabnika():
    print("Pozdravljeni! To je vaš osebni dnevnik knjig.")

def identifikacija_knjige():
    naslov = input("Naslov knjige: ")
    avtor = input("Ime avtorja: ")
    zvrst = input("Zvrst: ")
    if zvrst == "leposlovje" or zvrst == "neleposlovje":
        pass
    else:
        while zvrst != "leposlovje" and zvrst != "neleposlovje":
            print(
                "Zvrst knjige mora biti 'leposlovje' ali 'neleposlovje'! Poskusite še enkrat.")
            zvrst = input("Zvrst: ")
    izposojena_ali_kupljena = input("Izposojena ali kupljena: ")
    if izposojena_ali_kupljena == "izposojena" or izposojena_ali_kupljena == "kupljena":
        pass
    else:
        while izposojena_ali_kupljena != "izposojena" and izposojena_ali_kupljena != "kupljena":
            print("Knjiga mora biti 'izposojena' ali 'kupljena'. Poskusite še enkrat.")
            izposojena_ali_kupljena = input("Izposojena ali kupljena: ")
    if izposojena_ali_kupljena == "izposojena":
        rok_vracila = input("Rok vračila: ")
    else:
        rok_vracila = "/"
    return Knjiga(naslov, avtor, zvrst, izposojena_ali_kupljena, rok_vracila, None)


def prikazi_knjige_cez_rok():
    knjige_cez_rok = []
    for knjiga in moj_model.trenutne_knjige:
        if knjiga.cez_rok():
            naslov = getattr(knjiga, "naslov")
            avtor = getattr(knjiga, "avtor")
            zvrst = getattr(knjiga, "zvrst")
            rok_vracila = getattr(knjiga, "rok_vracila")
            # vemo, da je knjiga izposojena
            knjige_cez_rok.append((naslov, avtor, zvrst, rok_vracila))
    if len(knjige_cez_rok) == 0:
        print("Nimate knjig, ki jih je nujno potrebno vrniti.")
    else:
        print("Naslednje knjige morate vrniti, saj zanje teče zamudnina: ")
        for i in knjige_cez_rok:
            print(rdeca_pisava(i))
        print("Skupno število knjig čez rok: " + str(len(knjige_cez_rok)))


def prikazi_prebrane_knjige():
    if len(moj_model.prebrane_knjige) == 0:
        print("Zaenkrat še niste prebrali nobene knjige.")
    else:
        print("To so knjige, ki ste jih prebrali do sedaj: ")
        for knjiga in prebrane_knjige_prikaz:
            print(zelena_pisava(knjiga))
        if moj_model.stevilo_leposlovnih() == 0 and moj_model.stevilo_neleposlovnih() != 0:
            print("Zaenkrat niste prebrali nobene leposlovne knjige in toliko neleposlovnih: " +
                  str(moj_model.stevilo_neleposlovnih()))
        elif moj_model.stevilo_leposlovnih() != 0 and moj_model.stevilo_neleposlovnih() == 0:
            print("Zaenkrat niste prebrali nobene neleposlovne knjige in toliko leposlovnih: " +
                  str(moj_model.stevilo_leposlovnih()))
        else:
            print("Prebrali ste toliko leposlovnih knjig: " +
                  str(moj_model.stevilo_leposlovnih()))
            nova_vrstica()
            print("Prebrali ste toliko neleposlovnih knjig: " +
                  str(moj_model.stevilo_neleposlovnih()))

def posodobi_trenutne_knjige():
    for knjiga in moj_model.trenutne_knjige:
        naslov = getattr(knjiga, "naslov")
        avtor = getattr(knjiga, "avtor")
        zvrst = getattr(knjiga, "zvrst")
        izposojena_ali_kupljena = getattr(knjiga, "izposojena_ali_kupljena")
        rok_vracila = getattr(knjiga, "rok_vracila")
        trenutne_knjige_prikaz.append((naslov, avtor, zvrst, izposojena_ali_kupljena, rok_vracila))

def posodobi_prebrane_knjige():
    for knjiga in moj_model.prebrane_knjige:
        naslov = getattr(knjiga, "naslov")
        avtor = getattr(knjiga, "avtor")
        zvrst = getattr(knjiga, "zvrst")
        ocena = getattr(knjiga, "ocena")
        prebrane_knjige_prikaz.append((naslov, avtor, zvrst, ocena))

tekstovni_vmesnik()
