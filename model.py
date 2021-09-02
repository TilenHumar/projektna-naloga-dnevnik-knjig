from datetime import date, datetime
class Stanje:
    
    def __init__(self):
        self.trenutne_knjige = []
        self.trenutne_knjige_prikaz = []
        self.prebrane_knjige = []
        self.prebrane_knjige_prikaz = []

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
    
    def stevilo_zamujenih(self):
        stevilo = 0
        for knjiga in self.trenutne_knjige:
            if knjiga.cez_rok:
                stevilo += 1
        return stevilo

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
        if knjiga in self.prebrane_knjige:
            knjiga.dodaj_oceno(ocena)
    
class Knjiga:

    def __init__(self, naslov, avtor, zvrst, izposojena_ali_kupljena, rok_vracila="/", ocena=None):
        self.naslov = naslov
        self.avtor = avtor
        if zvrst == "leposlovje" or zvrst == "neleposlovje":
            self.zvrst = zvrst
        else:
            raise ValueError("Zvrst knjige je 'leposlovje' ali 'neleposlovje'.")
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