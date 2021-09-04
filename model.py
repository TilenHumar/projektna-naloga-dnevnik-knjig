from datetime import date, datetime
import re
import time
import json
from os import strerror


class Stanje:

    def __init__(self):
        self.trenutne_knjige = []
        self.prebrane_knjige = []

    def dodaj_knjigo(self, knjiga):
        self.trenutne_knjige.append(knjiga)

    def odstrani_knjigo(self, knjiga):
        self.trenutne_knjige.remove(knjiga)

    def vsebuje_knjigo(self, knjiga):
        return True if knjiga in self.trenutne_knjige else False

    def vsebuje_knjigo_prebrane(self, knjiga):
        return True if knjiga in self.prebrane_knjige else False

    def preberi_knjigo(self, knjiga):
        self.prebrane_knjige.append(knjiga)
        self.trenutne_knjige.remove(knjiga)

    def stevilo_trenutnih(self):
        return len(self.trenutne_knjige)

    def stevilo_prebranih(self):
        return len(self.prebrane_knjige)
    
    def seznam_cez_rok(self):
        seznam = []
        for knjiga in self.trenutne_knjige:
            if knjiga.cez_rok:
                seznam.append(knjiga)
        return seznam
###
    def stevilo_cez_rok(self):
        stevilo = 0
        for knjiga in self.trenutne_knjige:
            rok_vracila = getattr(knjiga, "rok_vracila")
            if rok_vracila == "/":
                pass
            else:
                danes = datetime.now()
                datum = datetime.strptime(rok_vracila, "%d.%m.%Y")
                if datum < danes:
                    stevilo += 1
        return stevilo

###

    def stevilo_leposlovnih(self):
        stevilo = 0
        for knjiga in self.prebrane_knjige:
            zvrst_knjige = getattr(knjiga, "zvrst")
            if zvrst_knjige == "leposlovje":
                stevilo += 1
        return stevilo

    def stevilo_neleposlovnih(self):
        stevilo = 0
        for knjiga in self.prebrane_knjige:
            zvrst_knjige = getattr(knjiga, "zvrst")
            if zvrst_knjige == "neleposlovje":
                stevilo += 1
        return stevilo

    def dodaj_oceno_prebrani(self, knjiga, ocena):
            knjiga.dodaj_oceno(ocena)

    def v_slovar(self):
        return{
            "trenutne_knjige": [knjiga.v_slovar() for knjiga in self.trenutne_knjige],
            "prebrane_knjige": [knjiga.v_slovar() for knjiga in self.prebrane_knjige],
        }

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

    def shrani_v_datoteko(self, ime_datoteke):
        with open(ime_datoteke, 'w') as datoteka:
            slovar = self.v_slovar()
            json.dump(slovar, datoteka)

    @staticmethod
    def preberi_iz_datoteke(ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar = json.load(datoteka)
            return Stanje.iz_slovarja(slovar)

    def preveri_podatke_nove_knjige(self, naslov, avtor, zvrst, izposojena_ali_kupljena, rok_vracila):
            napake = {}
            if not naslov:
                napake["naslov"] = "Prosimo, vnesite naslov knjige."
            if not avtor:
                napake["avtor"] = "Prosimo, vnesite avtorja-ico knjige."
            if zvrst != "leposlovje" or zvrst != "neleposlovje":
                napake[zvrst] = "Zvrst mora biti 'leposlovje' ali 'neleposlovje'."
            if izposojena_ali_kupljena != "izposojena" or izposojena_ali_kupljena != "kupljena":
                napake[izposojena_ali_kupljena] = "Knjiga mora biti 'izposojena' ali 'kupljena'."
            if izposojena_ali_kupljena == "izposojena" and not rok_vracila:
                napake[rok_vracila] = "Izposojena knjiga mora imeti datum vračila."
            knjiga = Knjiga(naslov, avtor, zvrst, izposojena_ali_kupljena, rok_vracila)
            if self.vsebuje_knjigo(knjiga):
                napake["naslov"] = "Ta knjiga je že v vašem trenutnem seznamu."
            return napake

    def preveri_podatke_ocena(self, ocena):
        napake = {}
        if ocena not in range(1,6):
            napake["ocena"] = "Ocena mora biti med 1 in 5."
        return napake

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

    def __eq__(self, other):
        naslov_TF = (self.naslov == other.naslov)
        avtor_TF = (self.avtor == other.avtor)
        zvrst_TF = (self.zvrst == other.zvrst)
        return naslov_TF and avtor_TF and zvrst_TF

    def cez_rok(self):
        if self.rok_vracila != "/":
            danes = datetime.now()
            datum = datetime.strptime(self.rok_vracila, "%d.%m.%Y")
            return datum <= danes

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

    