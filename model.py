from datetime import date, datetime
import json


class Uporabnik:
    def __init__(self, uporabnisko_ime, stanje):
        self.uporabnisko_ime = uporabnisko_ime
        self.stanje = stanje

    def v_slovar(self):
        return{
            "uporabnisko_ime": self.uporabnisko_ime,
            "stanje": self.stanje.v_slovar()
        }

    @staticmethod
    def iz_slovarja(slovar):
        uporabnisko_ime = slovar["uporabnisko_ime"]
        stanje = Stanje.iz_slovarja(slovar["stanje"])
        return Uporabnik(uporabnisko_ime, stanje)

    def shrani_v_datoteko(self):
        with open(Uporabnik.ime_uporabnikove_datoteke(self.uporabnisko_ime), 'w') as datoteka:
            slovar = self.v_slovar()
            json.dump(slovar, datoteka)

    @staticmethod
    def ime_uporabnikove_datoteke(uporabnisko_ime):
        return f"{uporabnisko_ime}.json"

    @staticmethod
    def preberi_iz_datoteke(uporabnisko_ime):
        with open(Uporabnik.ime_uporabnikove_datoteke(uporabnisko_ime)) as datoteka:
            slovar = json.load(datoteka)
            return Uporabnik.iz_slovarja(slovar)


class Stanje:

    def __init__(self):
        self.trenutne_knjige = []
        self.prebrane_knjige = []

    # dodajanje knjig v seznam trenutnih knjig
    def dodaj_knjigo(self, knjiga):
        self.trenutne_knjige.append(knjiga)

    # odstranjevanje knjig iz seznama trenutnih knjig
    def odstrani_knjigo(self, knjiga):
        self.trenutne_knjige.remove(knjiga)

    # preverimo, če je knjiga v seznamu trenutnih knjig
    def vsebuje_knjigo(self, knjiga):
        return True if knjiga in self.trenutne_knjige else False

    # preverimo, če je knjiga v seznamu prebranih knjig
    def vsebuje_knjigo_prebrane(self, knjiga):
        return True if knjiga in self.prebrane_knjige else False

    # preberemo knjigo(dodamo v seznam prebranih, odstranimo iz trenutnega seznama)
    def preberi_knjigo(self, knjiga):
        self.prebrane_knjige.append(knjiga)
        self.trenutne_knjige.remove(knjiga)

    # ugotovimo število knjig, ki jih trenutno beremo
    def stevilo_trenutnih(self):
        return len(self.trenutne_knjige)

    # ugotovimo število knjig, ki smo jih prebrali
    def stevilo_prebranih(self):
        return len(self.prebrane_knjige)

    # dobimo seznam knjig, katerim je pretekel rok vračila
    def seznam_cez_rok(self):
        seznam = []
        for knjiga in self.trenutne_knjige:
            if knjiga.cez_rok():
                seznam.append(knjiga)
            else:
                pass
        return seznam

    # dobimo število knjig, katerim je pretekel rok vračila
    def stevilo_cez_rok(self):
        return len(self.seznam_cez_rok())

    # dobimo število leposlovnih knjig, ki smo jih prebrali
    def stevilo_leposlovnih(self):
        stevilo = 0
        for knjiga in self.prebrane_knjige:
            zvrst_knjige = getattr(knjiga, "zvrst")
            if zvrst_knjige == "leposlovje":
                stevilo += 1
        return stevilo

    # dobimo število neleposlovnih knjig, ki smo jih prebrali
    def stevilo_neleposlovnih(self):
        stevilo = 0
        for knjiga in self.prebrane_knjige:
            zvrst_knjige = getattr(knjiga, "zvrst")
            if zvrst_knjige == "neleposlovje":
                stevilo += 1
        return stevilo

    # ocenimo prebrano knjigo
    def dodaj_oceno_prebrani(self, knjiga, ocena):
        knjiga.dodaj_oceno(ocena)

    def v_slovar(self):
        return{
            "trenutne_knjige": [knjiga.v_slovar() for knjiga in self.trenutne_knjige],
            "prebrane_knjige": [knjiga.v_slovar() for knjiga in self.prebrane_knjige],
        }

    def shrani_v_datoteko(self, ime_datoteke):
        with open(ime_datoteke, 'w') as datoteka:
            slovar = self.v_slovar()
            json.dump(slovar, datoteka)

    @staticmethod
    def iz_slovarja(slovar):
        stanje = Stanje()
        stanje.trenutne_knjige = [
            Knjiga.iz_slovarja(knjiga_slovar) for knjiga_slovar in slovar["trenutne_knjige"]
        ]
        stanje.prebrane_knjige = [
            Knjiga.iz_slovarja(knjiga_slovar) for knjiga_slovar in slovar["prebrane_knjige"]
        ]
        return stanje

    @staticmethod
    def preberi_iz_datoteke(ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar = json.load(datoteka)
            return Stanje.iz_slovarja(slovar)


class Knjiga:

    def __init__(self, naslov, avtor, zvrst, izposojena_ali_kupljena, rok_vracila="/", ocena=None):
        self.naslov = naslov
        self.avtor = avtor
        if zvrst == "leposlovje" or zvrst == "neleposlovje":
            self.zvrst = zvrst
        else:
            raise ValueError(
                "Zvrst knjige je 'leposlovje' ali 'neleposlovje'.")
        if izposojena_ali_kupljena == "izposojena" or izposojena_ali_kupljena == "kupljena":
            self.izposojena_ali_kupljena = izposojena_ali_kupljena
        else:
            raise ValueError("Knjiga mora biti 'izposojena' ali 'kupljena'.")
        self.rok_vracila = rok_vracila
        self.ocena = ocena

    # knjigi sta enaki če se ujemata v naslovu, avtorju in zvrsti
    def __eq__(self, other):
        naslov_TF = (self.naslov == other.naslov)
        avtor_TF = (self.avtor == other.avtor)
        zvrst_TF = (self.zvrst == other.zvrst)
        return naslov_TF and avtor_TF and zvrst_TF

    # ugotovimo, ali je knjigi pretekel rok vračila
    def cez_rok(self):
        rok_vracila = self.rok_vracila
        if rok_vracila != "/":
            danes = datetime.now()
            datum = datetime.strptime(rok_vracila, "%d.%m.%Y")
            return datum < danes
        else:
            return False

    # knjigi dodamo oceno
    def dodaj_oceno(self, ocena):
        self.ocena = ocena

    def v_slovar(self):
        return {
            "naslov": self.naslov,
            "avtor": self.avtor,
            "zvrst": self.zvrst,
            "izposojena_ali_kupljena": self.izposojena_ali_kupljena,
            "rok_vracila": self.rok_vracila,
            "ocena": self.ocena
        }

    @staticmethod
    def iz_slovarja(slovar):
        return Knjiga(
            slovar["naslov"],
            slovar["avtor"],
            slovar["zvrst"],
            slovar["izposojena_ali_kupljena"],
            slovar["rok_vracila"],
            slovar["ocena"]
        )
