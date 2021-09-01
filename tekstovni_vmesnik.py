import model

stanje = model.Stanje()

def tekstovni_vmesnik():
    pozdravi_uporabnika()
    while True:
        prikazi_osnovni_zaslon()

def prikazi_osnovni_zaslon():
    prikazi_trenutne_knjige()
    prikazi_knjige_cez_rok()
    prikazi_prebrane_knjige()
    ukaz = preberi_ukaz()
    if ukaz == "dodaj":
        dodaj_knjigo()
    elif ukaz == "odstrani":
        odstrani_knjigo()
    elif ukaz == "preberi":
        preberi_knjigo()
    else:
        print("Oprostite, tega ukaza pa ne razumem. Prosimo izberite enega od ponujenih ukazov.")
    print("\n" * 5)
def preberi_ukaz():
    return input("Novo knjigo dodate z ukazom 'dodaj', nezaželeno odstranite z ukazom 'odstrani', če pa ste katero knjigo prebrali, vpišite ukaz 'preberi'. \n Kaj želite storiti? ")

def dodaj_knjigo():
    knjiga = identifikacija_knjige()
    naslov = getattr(knjiga, "naslov")
    avtor = getattr(knjiga, "avtor")
    zvrst = getattr(knjiga, "zvrst")
    izposojena_ali_kupljena = getattr(knjiga, "izposojena_ali_kupljena")
    rok_vracila = getattr(knjiga, "rok_vracila")
    if knjiga not in stanje.trenutne_knjige:
        stanje.trenutne_knjige.append(knjiga) ####
        stanje.trenutne_knjige_prikaz.append((naslov, avtor, zvrst, izposojena_ali_kupljena, rok_vracila))
    else:
        print("To knjigo ste že dodali v seznam.")

def odstrani_knjigo():
    knjiga = identifikacija_knjige()
    naslov = getattr(knjiga, "naslov")
    avtor = getattr(knjiga, "avtor")
    zvrst = getattr(knjiga, "zvrst")
    izposojena_ali_kupljena = getattr(knjiga, "izposojena_ali_kupljena")
    rok_vracila = getattr(knjiga, "rok_vracila")
    if knjiga in stanje.trenutne_knjige:
            stanje.trenutne_knjige.remove(knjiga) ####
            stanje.trenutne_knjige_prikaz.remove((naslov, avtor, zvrst, izposojena_ali_kupljena, rok_vracila))
    else:
        print("Te knjige sploh ni v vašem trenutnem seznamu. Ali ste se morda kje zmotili? ")

def preberi_knjigo():
    knjiga = identifikacija_knjige()
    naslov = getattr(knjiga, "naslov")
    avtor = getattr(knjiga, "avtor")
    zvrst = getattr(knjiga, "zvrst")
    izposojena_ali_kupljena = getattr(knjiga, "izposojena_ali_kupljena")
    rok_vracila = getattr(knjiga, "rok_vracila")
    if knjiga in stanje.prebrane_knjige:
        print("To knjigo ste že prebrali.")
    elif knjiga in stanje.trenutne_knjige:
            stanje.trenutne_knjige.remove(knjiga) ####
            stanje.trenutne_knjige_prikaz.remove((naslov, avtor, zvrst, izposojena_ali_kupljena, rok_vracila))
            stanje.prebrane_knjige.append(knjiga)
            stanje.prebrane_knjige_prikaz.append((naslov, avtor, zvrst))
    else:
        print("Te knjige pa sploh niste brali. Ali ste se morda kje zmotili? ")
    

def prikazi_trenutne_knjige():
    print("Knjige, ki jih trenutno berete so:")
    for i in stanje.trenutne_knjige_prikaz:
        print(i)
    

def pozdravi_uporabnika():
    print("Pozdravljeni! To je vaš osebni dnevnik knjig.")

def identifikacija_knjige():
    naslov = input("Naslov knjige: ")
    avtor = input("Ime avtorja: ")
    zvrst = input("Zvrst: ")
    izposojena_ali_kupljena = input("Izposojena ali kupljena: ")
    if izposojena_ali_kupljena == "izposojena" or izposojena_ali_kupljena == "kupljena":
            pass
    else:
        raise ValueError("Knjiga mora biti izposojena ali kupljena.")
    if izposojena_ali_kupljena == "izposojena":
        rok_vracila = input("Rok vračila: ")
    else: 
        rok_vracila = None
    return model.Knjiga(naslov, avtor, zvrst, izposojena_ali_kupljena, rok_vracila)

def prikazi_knjige_cez_rok():
    knjige_cez_rok = []
    for knjiga in stanje.trenutne_knjige:
        if knjiga.cez_rok():
            naslov = getattr(knjiga, "naslov")
            avtor = getattr(knjiga, "avtor")
            zvrst = getattr(knjiga, "zvrst")
            izposojena_ali_kupljena = getattr(knjiga, "izposojena_ali_kupljena")
            rok_vracila = getattr(knjiga, "rok_vracila")
            knjige_cez_rok.append((naslov, avtor, zvrst, rok_vracila)) #vemo, da je knjiga izposojena
    if len(knjige_cez_rok) == 0:
        print("Nimate knjig, ki jih je nujno potrebno vrniti.")
    else:
        print("Naslednje knjige morate vrniti, saj zanje teče zamudnina: ")
        for i in knjige_cez_rok:
            print(i)

def prikazi_prebrane_knjige():
    if len(stanje.prebrane_knjige) == 0:
        print("Zaenkrat še niste prebrali nobene knjige.")
    else:
        print("To so knjige, ki ste jih prebrali do sedaj: ")
        for knjiga in stanje.prebrane_knjige_prikaz:
            print(knjiga)
        
tekstovni_vmesnik()