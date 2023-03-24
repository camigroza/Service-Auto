import termcolor as termcolor

from Repository.repository_reduceri_json import RepositoryReduceriJson
from Service.card_client_service import CardClientService
from Service.masina_service import MasinaService
from Service.tranzactie_service import TranzactieService
from Service.undo_redo_service import UndoRedoService


class Consola:
    def __init__(self, masina_service: MasinaService,
                 card_client_service: CardClientService,
                 tranzactie_service: TranzactieService,
                 repository_reduceri: RepositoryReduceriJson,
                 undo_redo_service: UndoRedoService):
        self.__masina_service = masina_service
        self.__card_client_service = card_client_service
        self.__tranzactie_service = tranzactie_service
        self.__repository_reduceri = repository_reduceri
        self.__undo_redo_service = undo_redo_service

    def run_menu(self):
        while True:
            print("1. CRUD masina")
            print("2. CRUD card client")
            print("3. CRUD tranzactie")
            print("4. Cautare masini si clienti. Cautare full text")
            print("5. Afisarea tuturor tranzactiilor cu "
                  "suma cuprinsa intr-un interval dat")
            print("6. Afisarea masinilor ordonate descrescator "
                  "dupa suma obtinuta pe manopera")
            print("7. Afisarea cardurilor client ordonate descrescator "
                  "dupa valoarea reducerilor obtinute")
            print("8. Stergerea tuturor tranzactiilor dintr-un "
                  "anumit interval de zile")
            print("9. Actualizarea garantiei la fiecare masina")
            print("u. Undo")
            print("r. Redo")
            print("R. Generare random")
            print("x. Iesire")
            optiune = input("Dati optiunea: ")
            if optiune == "1":
                self.run_menu_CRUD_masina()
            elif optiune == "2":
                self.run_menu_CRUD_card_client()
            elif optiune == "3":
                self.run_menu_CRUD_tranzactie()
            elif optiune == "4":
                self.cautare_full_text()
            elif optiune == "5":
                self.ui_afisare_tranzactii_suma_interval()
            elif optiune == "6":
                self.ui_ordonare_masini_descrescator_manopera()
            elif optiune == "7":
                self.ui_afisare_carduri_descrescator_reduceri()
            elif optiune == "8":
                self.ui_sterge_tranzactii_interval_zile()
            elif optiune == "9":
                self.ui_actualizare_garantie_masini()
            elif optiune == "u":
                self.__undo_redo_service.undo()
            elif optiune == "r":
                self.__undo_redo_service.redo()
            elif optiune == "R":
                self.generate_random()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati: ")

    def run_menu_CRUD_masina(self):
        while True:
            print("1. Adauga masina")
            print("2. Sterge masina")
            print("3. Modifica masina")
            print("a. Afiseaza toate masinile")
            print("x. Iesire")
            optiune = input("Dati optiunea: ")
            if optiune == "1":
                self.ui_adauga_masina()
            elif optiune == "2":
                self.ui_sterge_masina()
            elif optiune == "3":
                self.ui_modifica_masina()
            elif optiune == "a":
                self.show_all_masini()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati: ")

    def run_menu_CRUD_card_client(self):
        while True:
            print("1. Adauga card client")
            print("2. Sterge card client")
            print("3. Modifica card client")
            print("a. Afiseaza toate cardurile")
            print("x. Iesire")
            optiune = input("Dati optiunea: ")
            if optiune == "1":
                self.ui_adauga_card_client()
            elif optiune == "2":
                self.ui_sterge_card_client()
            elif optiune == "3":
                self.ui_modifica_card_client()
            elif optiune == "a":
                self.show_all_carduri()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reinercati: ")

    def run_menu_CRUD_tranzactie(self):
        while True:
            print("1. Adauga tranzactie")
            print("2. Sterge tranzactie")
            print("3. Modifica tranzactie")
            print("a. Afiseaza toate tranzactiile")
            print("x. Iesire")
            optiune = input("Dati optiunea: ")
            if optiune == "1":
                self.ui_adauga_tranzactie()
            elif optiune == "2":
                self.ui_sterge_tranzactie()
            elif optiune == "3":
                self.ui_modifica_tranzactie()
            elif optiune == "a":
                self.show_all_tranzactii()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati: ")

    def ui_adauga_masina(self):
        try:
            id_masina = input("Dati id-ul masinii: ")
            model = input("Dati modelul masinii: ")
            an_achizitie = int(input("Dati anul achizitiei masinii: "))
            nr_km = float(input("Dati numarul de km ai masinii: "))
            garantie = input("Spuneti daca masina este in garantie (da/nu): ")
            self.__masina_service.adauga(id_masina, model,
                                         an_achizitie, nr_km, garantie)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_sterge_masina(self):
        try:
            id_masina = input("Dati id-ul masinii de sters: ")
            self.__masina_service.sterge(id_masina)

            self.__tranzactie_service.sterge_tranzactie_id_masina(id_masina)

        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_modifica_masina(self):
        try:
            id_masina = input("Dati id-ul masinii de modificat: ")
            model = input("Dati noul model al masinii: ")
            an_achizitie = int(input("Dati noul an al achizitiei masinii: "))
            nr_km = float(input("Dati noul numar de km ai masinii: "))
            garantie = input("Spuneti daca masina este in garantie (da/nu): ")
            self.__masina_service.modifica(id_masina, model,
                                           an_achizitie, nr_km, garantie)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def show_all_masini(self):
        masini = self.__masina_service.get_all()
        if len(masini) > 0:
            for masina in masini:
                print(masina)
        else:
            mesaj = termcolor.colored("Nu exista masini in fisier!", 'magenta')
            print(mesaj)

    def ui_adauga_card_client(self):
        try:
            id_card_client = input("Dati id-ul cardului: ")
            nume = input("Dati numele: ")
            prenume = input("Dati prenumele: ")
            CNP = input("Dati CNP-ul: ")
            data_nasterii = input("Dati data nasterii (DD.MM.YYYY): ")
            data_inregistrarii = \
                input("Dati data inregistrarii (DD.MM.YYYY): ")
            self.__card_client_service.adauga(id_card_client, nume,
                                              prenume, CNP, data_nasterii,
                                              data_inregistrarii)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_sterge_card_client(self):
        try:
            id_card_client = input("Dati id-ul cardului de sters: ")
            self.__card_client_service.sterge(id_card_client)

            self.__tranzactie_service.\
                sterge_tranzactie_id_card_client(id_card_client)

        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_modifica_card_client(self):
        try:
            id_card_client = input("Dati id-ul cardului de modificat: ")
            nume = input("Dati noul nume: ")
            prenume = input("Dati noul prenume: ")
            CNP = input("Dati noul CNP: ")
            data_nasterii = input("Dati noua data a nasterii (DD.MM.YYYY): ")
            data_inregistrarii = \
                input("Dati noua data a inregistrarii (DD.MM.YYYY): ")
            self.__card_client_service.modifica(id_card_client,
                                                nume, prenume,
                                                CNP, data_nasterii,
                                                data_inregistrarii)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def show_all_carduri(self):
        carduri = self.__card_client_service.get_all()
        if len(carduri) > 0:
            for card in carduri:
                print(card)
        else:
            mesaj = termcolor.colored("Nu exista carduri "
                                      "in fisier!", 'magenta')
            print(mesaj)

    def ui_adauga_tranzactie(self):
        try:
            id_tranzactie = input("Dati id-ul tranzactiei: ")
            id_masina = input("Dati id-ul masinii: ")
            id_card_client = input("Dati id-ul cardului client: ")
            suma_piese = float(input("Dati valoarea pieselor: "))
            suma_manopera = float(input("Dati valoarea manoperei: "))
            data = input("Dati data (DD.MM.YYYY): ")
            ora = input("Dati ora (HH:MM): ")
            reduceri = []
            self.__tranzactie_service.adauga(id_tranzactie, id_masina,
                                             id_card_client, suma_piese,
                                             suma_manopera, data,
                                             ora, reduceri)
            self.__repository_reduceri.adauga(id_tranzactie, reduceri)

        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_sterge_tranzactie(self):
        try:
            id_tranzactie = input("Dati id-ul tranzactiei de sters: ")
            self.__tranzactie_service.sterge(id_tranzactie)
            self.__repository_reduceri.sterge(id_tranzactie)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_modifica_tranzactie(self):
        try:
            id_tranzactie = input("Dati id-ul tranzactiei de modificat: ")
            id_masina = input("Dati noul id al masinii: ")
            id_card_client = input("Dati noul id al cardului client: ")
            suma_piese = float(input("Dati noua valoare a pieselor: "))
            suma_manopera = float(input("Dati noua valoare a manoperei: "))
            data = input("Dati noua data (DD.MM.YYYY): ")
            ora = input("Dati noua ora (HH:MM): ")
            self.__repository_reduceri.sterge(id_tranzactie)
            reduceri = []
            self.__tranzactie_service.modifica(id_tranzactie, id_masina,
                                               id_card_client, suma_piese,
                                               suma_manopera, data,
                                               ora, reduceri)
            self.__repository_reduceri.adauga(id_tranzactie, reduceri)

        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def show_all_tranzactii(self):
        tranzactii = self.__tranzactie_service.get_all()
        if len(tranzactii) > 0:
            for tranzactie in tranzactii:
                print(tranzactie)
                pret = tranzactie.suma_piese + tranzactie.suma_manopera
                print(f'\tPretul platit este de {pret} ron')
                x = self.__repository_reduceri.read(tranzactie.id_entitate)
                for reducere in x:
                    print('\t', reducere)
        else:
            mesaj = termcolor.colored("Nu exista tranzactii in fisier!",
                                      'magenta')
            print(mesaj)

    def ui_afisare_tranzactii_suma_interval(self):
        inf_interval = float(input("Dati marginea inferioara a "
                                   "intervalului: "))
        sup_interval = float(input("Dati marginea superioara a "
                                   "intervalului: "))
        tranzactii = self.__tranzactie_service. \
            tranzactii_cu_suma_in_interval(inf_interval, sup_interval,
                                           self.__tranzactie_service.get_all(),
                                           [])
        if len(tranzactii) > 0:
            for tranzactie in tranzactii:
                print(tranzactie)
                print(f'\tPretul platit este de '
                      f'{tranzactie.suma_manopera + tranzactie.suma_piese} '
                      f'ron')
        else:
            print("Nu exista tranzactii cu suma cuprinsa in intervalul dat.")

    def generate_random(self):
        while True:
            print("1. Genereaza random masini")
            print("2. Genereaza random carduri client")
            optiune = input("Dati optiunea: ")
            if optiune == "1":
                n = int(input("Dati numarul de masini pe care doriti "
                              "sa le generati random: "))
                self.__masina_service.masini_random(n)
                self.show_all_masini()
            elif optiune == "2":
                n = int(input("Dati numarul de carduri client pe care doriti "
                              "sa le generati random: "))
                self.__card_client_service.carduri_random(n)
                self.show_all_carduri()

    def cautare_full_text(self):
        text_cautat = input("Dati textul pe care doriti sa il cautati: ")
        self.__masina_service.cautare_full_text(text_cautat)
        self.__card_client_service.cautare_full_text(text_cautat)

    def ui_ordonare_masini_descrescator_manopera(self):
        rezultat = self.__tranzactie_service. \
            ordoneaza_desc_dupa_suma_manopera()
        for suma_manopera in rezultat:
            if rezultat[suma_manopera] is not None:
                print(rezultat[suma_manopera])
                print(f'\tSuma obtinuta pe manopera este '
                      f'de {suma_manopera} ron')

    def ui_afisare_carduri_descrescator_reduceri(self):
        for card in self.__tranzactie_service. \
                ordoneaza_carduri_desc_dupa_reduceri():
            print(card)

    def ui_sterge_tranzactii_interval_zile(self):
        data1 = input("Dati prima data a intervalului: ")
        data2 = input("Dati a doua data a intervalului: ")
        self.__tranzactie_service.sterge_tranzactii_interval_zile(data1, data2)

    def ui_actualizare_garantie_masini(self):
        self.__masina_service.actualizare_garantie()
