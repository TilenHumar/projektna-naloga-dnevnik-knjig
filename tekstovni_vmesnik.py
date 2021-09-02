import model
stanje = model.Stanje()

class Izgled_pisave:

    ZELENA = "\033[92m"
    RDECA = "\033[91m"
    KREPKO = "\033[1m"
    KONEC = "\033[0m"

def zelena_pisava(niz):
    return Izgled_pisave.ZELENA + str(niz) +Izgled_pisave.KONEC

def rdeca_pisava(niz):
    return Izgled_pisave.RDECA + str(niz) +Izgled_pisave.KONEC

def krepka_pisava(niz):
    return Izgled_pisave.KREPKO + str(niz) +Izgled_pisave.KONEC

def nova_vrstica():
    print("\n")

def tekstovni_vmesnik():
    nova_vrstica()
    pozdravi_uporabnika()
    nova_vrstica()
    while True:
        prikazi_osnovni_zaslon()

def prikazi_osnovni_zaslon():
    prikazi_trenutne_knjige()
    nova_vrstica()
    prikazi_knjige_cez_rok()
    nova_vrstica()
    prikazi_prebrane_knjige()
    nova_vrstica()
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
    return input("Novo knjigo dodate z ukazom " + krepka_pisava('dodaj') + ", nezaželeno odstranite z ukazom " + krepka_pisava('odstrani') + ", če pa ste katero knjigo prebrali, vpišite ukaz " + krepka_pisava('preberi') + ". \n" + "Kaj želite storiti? ")

def dodaj_knjigo():
    knjiga = identifikacija_knjige()
    naslov = getattr(knjiga, "naslov")
    avtor = getattr(knjiga, "avtor")
    zvrst = getattr(knjiga, "zvrst")
    izposojena_ali_kupljena = getattr(knjiga, "izposojena_ali_kupljena")
    rok_vracila = getattr(knjiga, "rok_vracila")
    if not stanje.vsebuje_knjigo(knjiga):
        stanje.dodaj_knjigo(knjiga)
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
    if stanje.vsebuje_knjigo(knjiga):
            stanje.odstrani_knjigo(knjiga)
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
    if stanje.vsebuje_knjigo_prebrane(knjiga):
        print("To knjigo ste že prebrali. Odstranjena je z vašega trenutnega seznama in jo lahko vrnete.")
        stanje.odstrani_knjigo(knjiga)
        stanje.trenutne_knjige_prikaz.remove((naslov, avtor, zvrst, izposojena_ali_kupljena, rok_vracila))
    elif stanje.vsebuje_knjigo(knjiga):
        stanje.odstrani_knjigo(knjiga)
        stanje.trenutne_knjige_prikaz.remove((naslov, avtor, zvrst, izposojena_ali_kupljena, rok_vracila))
        stanje.preberi_knjigo(knjiga)
        stanje.prebrane_knjige_prikaz.append((naslov, avtor, zvrst))
    else:
        print("Te knjige pa sploh niste brali. Ali ste se morda kje zmotili? ")


def prikazi_trenutne_knjige():
    if stanje.trenutne_knjige == []:
        print("Trenutno ne berete nobene knjige. Začnite z branjem in svojemu napredku sledite s tem programom.")
    else:
        print("Knjige, ki jih trenutno berete so:")
        for i in stanje.trenutne_knjige_prikaz:
            print(i)
        print("Skupno število knjig, ki jih trenutno berete: " + str(len(stanje.trenutne_knjige_prikaz)))
    

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
            print("Zvrst knjige mora biti 'leposlovje' ali 'neleposlovje'! Poskusite še enkrat.")
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
    return model.Knjiga(naslov, avtor, zvrst, izposojena_ali_kupljena, rok_vracila)
    
def prikazi_knjige_cez_rok():
    knjige_cez_rok = []
    for knjiga in stanje.trenutne_knjige:
        if knjiga.cez_rok():
            naslov = getattr(knjiga, "naslov")
            avtor = getattr(knjiga, "avtor")
            zvrst = getattr(knjiga, "zvrst")
            rok_vracila = getattr(knjiga, "rok_vracila")
            knjige_cez_rok.append((naslov, avtor, zvrst, rok_vracila)) #vemo, da je knjiga izposojena
    if len(knjige_cez_rok) == 0:
        print("Nimate knjig, ki jih je nujno potrebno vrniti.")
    else:
        print("Naslednje knjige morate vrniti, saj zanje teče zamudnina: ")
        for i in knjige_cez_rok:
            print( rdeca_pisava(i))
        print("Skupno število knjig čez rok: " + str(len(knjige_cez_rok)))

def prikazi_prebrane_knjige():
    if len(stanje.prebrane_knjige) == 0:
        print("Zaenkrat še niste prebrali nobene knjige.")
    else:
        print("To so knjige, ki ste jih prebrali do sedaj: ")
        for knjiga in stanje.prebrane_knjige_prikaz:
            print(zelena_pisava(knjiga))
  
tekstovni_vmesnik()