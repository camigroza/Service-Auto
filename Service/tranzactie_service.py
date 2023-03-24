from datetime import date

from Domain.add_operation import AddOperation
from Domain.card_client_validator import CardClientValidator
from Domain.delete_operation import DeleteOperation
from Domain.masina_validator import MasinaValidator
from Domain.modify_operation import ModifyOperation
from Domain.multi_delete_operation import MultiDeleteOperation
from Domain.my_sort import my_sort
from Domain.tranzactie import Tranzactie
from Domain.tranzactie_validator import TranzactieValidator
from Repository.repository import Repository
from Repository.repository_reduceri_json import RepositoryReduceriJson
from Service.undo_redo_service import UndoRedoService
from view_models.card_reduceri_manopera_view_model import \
    CardReduceriManoperaViewModel


class TranzactieService:
    """
    Service pentru o tranzactie
    """

    def __init__(self,
                 tranzactie_repository: Repository,
                 tranzactie_validator: TranzactieValidator,
                 card_client_validator: CardClientValidator,
                 masina_validator: MasinaValidator,
                 masina_repository: Repository,
                 repository_reduceri: RepositoryReduceriJson,
                 card_client_repository: Repository,
                 undo_redo_service: UndoRedoService):
        self.__tranzactie_repository = tranzactie_repository
        self.__tranzactie_validator = tranzactie_validator
        self.__card_client_validator = card_client_validator
        self.__masina_validator = masina_validator
        self.__masina_repository = masina_repository
        self.__repository_reduceri = repository_reduceri
        self.__card_client_repository = card_client_repository
        self.__undo_redo_service = undo_redo_service

    def get_all(self):
        """
        Indica toate tranzactiile
        :return:
        """
        return self.__tranzactie_repository.read()

    def adauga(self, id_tranzactie: str, id_masina: str,
               id_card_client: str,
               suma_piese: float, suma_manopera: float,
               data: str, ora: str, reduceri: list):
        """
        Adauga o tranzactie
        :param id_tranzactie: string
        :param id_masina: string
        :param id_card_client: string
        :param suma_piese: float
        :param suma_manopera: float
        :param data: string
        :param ora: string
        :param reduceri: o lista
        :return:
        """
        if self.__card_client_validator.exist_id_card(id_card_client) \
                is True:
            reduceri.append(1)
            reducere = 10 / 100 * suma_manopera
            suma_manopera = suma_manopera - reducere
        if self.__masina_validator.are_garantie(id_masina) is True:
            reduceri.append(2)
            suma_piese = 0
        tranzactie = Tranzactie(id_tranzactie, id_masina, id_card_client,
                                suma_piese, suma_manopera, data, ora)
        self.__tranzactie_validator.valideaza(tranzactie)
        self.__tranzactie_repository.adauga(tranzactie)
        self.__undo_redo_service.adauga_undo_operation(AddOperation(
            self.__tranzactie_repository, tranzactie))

    def sterge(self, id_tranzactie: str):
        """
        Sterge tranzactia cu id-ul dat
        :param id_tranzactie: string
        :return:
        """
        tranzactie = self.__tranzactie_repository.read(id_tranzactie)
        self.__tranzactie_repository.sterge(id_tranzactie)
        self.__undo_redo_service.adauga_undo_operation(DeleteOperation(
            self.__tranzactie_repository, tranzactie))

    def modifica(self, id_tranzactie: str, id_masina: str,
                 id_card_client: str,
                 suma_piese: float, suma_manopera: float,
                 data: str, ora: str, reduceri: list):
        """
        Modifica o tranzactie
        :param id_tranzactie: string
        :param id_masina: string
        :param id_card_client: string
        :param suma_piese: float
        :param suma_manopera: float
        :param data: string
        :param ora: string
        :param reduceri: o lista
        :return:
        """
        tranzactie_veche = self.__tranzactie_repository.read(id_tranzactie)
        if self.__card_client_validator.exist_id_card(id_card_client) \
                is True:
            reduceri.append(1)
            reducere = 10 / 100 * suma_manopera
            suma_manopera = suma_manopera - reducere
        if self.__masina_validator.are_garantie(id_masina) is True:
            reduceri.append(2)
            suma_piese = 0
        tranzactie = Tranzactie(id_tranzactie, id_masina, id_card_client,
                                suma_piese, suma_manopera, data, ora)
        self.__tranzactie_validator.valideaza(tranzactie)
        self.__tranzactie_repository.modifica(tranzactie)
        self.__undo_redo_service.adauga_undo_operation(ModifyOperation(
            self.__tranzactie_repository, tranzactie_veche, tranzactie))

    def ordoneaza_desc_dupa_suma_manopera(self):
        """
        Ordoneaza masinile descrescator dupa suma obtinuta pe manopera
        :return: un dictionar in care cheia este suma manoperei, iar valoarea
        este masina
        """
        # tranzactii_ordonate = sorted(self.__tranzactie_repository.read(),
        #                              key=lambda tranzactie:
        #                              tranzactie.suma_manopera,
        #                              reverse=True)

        tranzactii_ordonate = my_sort(self.__tranzactie_repository.read(),
                                      key=lambda tranzactie:
                                      tranzactie.suma_manopera,
                                      reverse=True)

        rezultat = {}
        for tranzactie in tranzactii_ordonate:
            rezultat[tranzactie.suma_manopera] = \
                self.__masina_repository.read(tranzactie.id_masina)
        return rezultat

    def ordoneaza_carduri_desc_dupa_reduceri(self):
        """
        Ordoneaza cardurile client descrescator dupa valoarea
        reducerilor obtinute
        :return: CardReduceriManoperaViewModel
        """
        rezultat = []
        reduceri = self.__repository_reduceri.read()

        for id_tranzactie in reduceri:
            valoare_reducere = 0
            lista_reduceri_id_tranzactie = reduceri[id_tranzactie]
            for tip_reducere in lista_reduceri_id_tranzactie:
                if tip_reducere == "A fost aplicata o reducere de " \
                                   "10% pentru manopera.":
                    suma_manopera_dupa_reducere = \
                        self.__tranzactie_repository.read(id_tranzactie) \
                            .suma_manopera
                    suma_manopera_inital = \
                        (suma_manopera_dupa_reducere * 10) / 9
                    valoare_reducere = \
                        suma_manopera_inital - suma_manopera_dupa_reducere
            id_card_client_dorit = \
                self.__tranzactie_repository.read(id_tranzactie).id_card_client
            card_client = \
                self.__card_client_repository.read(id_card_client_dorit)
            if card_client is not None:
                rezultat.append(CardReduceriManoperaViewModel(
                    card_client,
                    valoare_reducere
                ))

        # return sorted(rezultat, key=lambda reduceri: reduceri.reducere,
        #               reverse=True)

        return my_sort(rezultat, key=lambda reduceri: reduceri.reducere,
                       reverse=True)

    def sterge_tranzactii_interval_zile(self, data1: str, data2: str):
        """
        Stergerea tuturor tranzactiilor dintr-un anumit interval de zile
        :param data1: prima data calendaristica
        :param data2: a doua data calendaristica
        :return:
        """
        ziua1 = int(data1[0] + data1[1])
        luna1 = int(data1[3] + data1[4])
        anul1 = int(data1[6] + data1[7] + data1[8] + data1[9])
        date1 = date(anul1, luna1, ziua1)

        ziua2 = int(data2[0] + data2[1])
        luna2 = int(data2[3] + data2[4])
        anul2 = int(data2[6] + data2[7] + data2[8] + data2[9])
        date2 = date(anul2, luna2, ziua2)

        if date2 < date1:
            date1, date2 = date2, date1

        tranzactii_sterse = []
        date_tranzactii = {}

        for tranzactie in self.__tranzactie_repository.read():
            data = tranzactie.data
            ziua = int(data[0] + data[1])
            luna = int(data[3] + data[4])
            anul = int(data[6] + data[7] + data[8] + data[9])
            date_tranzactie = date(anul, luna, ziua)
            date_tranzactii[tranzactie.id_entitate] = date_tranzactie
            # if date1 <= date_tranzactie <= date2:
            #     tranzactii_sterse.append(tranzactie)
            #     self.__repository_reduceri.sterge(tranzactie.id_entitate)
            #     self.__tranzactie_repository.sterge(tranzactie.id_entitate)

        tranzactii_sterse = list(filter(lambda tranzactie:
                                        date1 <= date_tranzactii[
                                            tranzactie.id_entitate] <= date2,
                                        self.__tranzactie_repository.read()))
        for tranzactie in tranzactii_sterse:
            self.__repository_reduceri.sterge(tranzactie.id_entitate)
            self.__tranzactie_repository.sterge(tranzactie.id_entitate)

        self.__undo_redo_service.adauga_undo_operation(MultiDeleteOperation(
            self.__tranzactie_repository, self.__repository_reduceri,
            tranzactii_sterse))

    def tranzactii_cu_suma_in_interval(self, inf_interval: float,
                                       sup_interval: float, tranzactii: list,
                                       rezultat: list):
        """
        Indica tranzactiile cu suma cuprinsa intr-un interval dat
        :param inf_interval: partea inferioara a intervalului
        :param sup_interval: partea superioara a intervalului
        :return: o lista cu toate tranzactiile care au suma cuprinsa in
        intervalul dat
        """
        # rezultat = []
        # for tranzactie in self.__tranzactie_repository.read():
        #     pret = tranzactie.suma_piese + tranzactie.suma_manopera
        #     if inf_interval <= pret <= sup_interval:
        #         rezultat.append(tranzactie)

        """rezultat = list(filter(lambda tranzactie:
                               inf_interval <= tranzactie.suma_piese +
                               tranzactie.suma_manopera <= sup_interval,
                               self.__tranzactie_repository.read()))"""

        if len(tranzactii) == 1:
            if inf_interval <= tranzactii[0].suma_piese + \
                    tranzactii[0].suma_manopera <= sup_interval:
                rezultat.append(tranzactii[0])
        else:
            if inf_interval <= tranzactii[0].suma_piese + \
                    tranzactii[0].suma_manopera <= sup_interval:
                rezultat.append(tranzactii[0])
            self.tranzactii_cu_suma_in_interval(inf_interval, sup_interval,
                                                tranzactii[1:], rezultat)

        return rezultat

    def sterge_tranzactie_id_masina(self, id_masina: str):
        """
        Sterge tranzactiile asociate masinii cu id-ul dat
        :param id_masina: id-ul masinii
        :return:
        """
        # for tranzactie in self.__tranzactie_repository.read():
        #     if tranzactie.id_masina == id_masina:
        #         self.__repository_reduceri.sterge(tranzactie.id_entitate)
        #         self.__tranzactie_repository.sterge(tranzactie.id_entitate)

        tranzactii_de_sters = list(filter(lambda tranzactie:
                                          tranzactie.id_masina == id_masina,
                                          self.__tranzactie_repository.read()))
        for tranzactie in tranzactii_de_sters:
            self.__repository_reduceri.sterge(tranzactie.id_entitate)
            self.__tranzactie_repository.sterge(tranzactie.id_entitate)

    def sterge_tranzactie_id_card_client(self, id_card_client: str):
        """
        Sterge tranzactiile asociate cardului client cu id-u dat
        :param id_card_client: id-ul cardului
        :return:
        """
        # for tranzactie in self.__tranzactie_repository.read():
        #     if tranzactie.id_card_client == id_card_client:
        #         self.__repository_reduceri.sterge(tranzactie.id_entitate)
        #         self.__tranzactie_repository.sterge(tranzactie.id_entitate)

        tranzactii_de_sters = list(filter(lambda tranzactie:
                                          tranzactie.id_card_client ==
                                          id_card_client,
                                          self.__tranzactie_repository.read()))
        for tranzactie in tranzactii_de_sters:
            self.__repository_reduceri.sterge(tranzactie.id_entitate)
            self.__tranzactie_repository.sterge(tranzactie.id_entitate)
