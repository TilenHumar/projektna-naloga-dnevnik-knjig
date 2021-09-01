from datetime import date, datetime
class Stanje:
    
    def __init__(self):
        self.trenutne_knjige = []
        self.trenutne_knjige_prikaz = []
        
    def dodaj_knjigo(self, knjiga):
        self.trenutne_knjige.append(knjiga)

    def odstrani_knjigo(self, knjiga):
        self.trenutne_knjige.remove(knjiga)

    def vsebuje_knjigo(self, knjiga):
        return True if knjiga in self.trenutne_knjige else False

class Knjiga:

    def __init__(self, naslov, avtor, zvrst, izposojena_ali_kupljena, rok_vracila, prebrana=False, ocena=None):
        self.naslov = naslov
        self.avtor = avtor
        self.zvrst = zvrst
        if izposojena_ali_kupljena == "izposojena" or izposojena_ali_kupljena == "kupljena":
            self.izposojena_ali_kupljena = izposojena_ali_kupljena
        else:
            raise ValueError("Knjiga mora biti 'izposojena' ali 'kupljena'.")
        self.rok_vracila = rok_vracila
        self.prebrana = prebrana
        self.ocena = ocena

    def __eq__(self, other):
        naslov_TF = (self.naslov == other.naslov)
        avtor_TF = (self.avtor == other.avtor)
        zvrst_TF = (self.zvrst == other.zvrst)
        izposojena_ali_kupljena_TF = (self.izposojena_ali_kupljena == other.izposojena_ali_kupljena)
        rok_vracila_TF = (self.rok_vracila == other.rok_vracila)
        return naslov_TF and avtor_TF and zvrst_TF and izposojena_ali_kupljena_TF and rok_vracila_TF

    def preberi(self):
        self.prebrana = True

    def kupi(self):
        self.izposojena_ali_kupljena = "kupljena"
        self.rok_vracila = None
    
    def cez_rok(self):
        if self.rok_vracila != None:
            danes = datetime.now()
            datum = datetime.strptime(self.rok_vracila, "%d.%m.%Y")
            return datum <= danes
