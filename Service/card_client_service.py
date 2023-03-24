from random import randint, choice

from Domain.add_operation import AddOperation
from Domain.card_client import CardClient
from Domain.card_client_validator import CardClientValidator
from Domain.delete_operation import DeleteOperation
from Domain.modify_operation import ModifyOperation
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService


class CardClientService:
    """
    Service pentru un card client
    """

    def __init__(self,
                 card_client_repository: Repository,
                 card_client_validator: CardClientValidator,
                 undo_redo_service: UndoRedoService):
        self.__card_client_repository = card_client_repository
        self.__card_client_validator = card_client_validator
        self.__undo_redo_service = undo_redo_service

    def get_all(self):
        """
        Indica toate cardurile
        :return:
        """
        return self.__card_client_repository.read()

    def adauga(self, id_card_client: str, nume: str, prenume: str,
               CNP: str, data_nasterii: str, data_inregistrarii: str):
        """
        Adauga un card
        :param id_card_client: string
        :param nume: string
        :param prenume: string
        :param CNP: string
        :param data_nasterii: string
        :param data_inregistrarii: string
        :return:
        """
        card_client = CardClient(id_card_client, nume, prenume,
                                 CNP, data_nasterii, data_inregistrarii)
        self.__card_client_validator.valideaza(card_client)
        if self.__card_client_validator.exist_cnp(CNP) is False:
            self.__card_client_repository.adauga(card_client)
        self.__undo_redo_service.adauga_undo_operation(AddOperation(
            self.__card_client_repository, card_client))

    def sterge(self, id_card_client: str):
        """
        Sterge cardul cu id-ul dat
        :param id_card_client: string
        :return:
        """
        card_client = self.__card_client_repository.read(id_card_client)
        self.__card_client_repository.sterge(id_card_client)
        self.__undo_redo_service.adauga_undo_operation(DeleteOperation(
            self.__card_client_repository, card_client))

    def modifica(self, id_card_client: str, nume: str, prenume: str,
                 CNP: str, data_nasterii: str, data_inregistrarii: str):
        """
        Modifica un card
        :param id_card_client: string
        :param nume: string
        :param prenume: string
        :param CNP: string
        :param data_nasterii: string
        :param data_inregistrarii: string
        :return:
        """
        card_client_vechi = self.__card_client_repository.read(id_card_client)
        card_client = CardClient(id_card_client, nume, prenume,
                                 CNP, data_nasterii, data_inregistrarii)
        self.__card_client_validator.valideaza(card_client)
        if self.__card_client_validator.exist_cnp(CNP, id_card_client) \
                is False:
            self.__card_client_repository.modifica(card_client)
        self.__undo_redo_service.adauga_undo_operation(ModifyOperation(
            self.__card_client_repository, card_client_vechi, card_client))

    def randomDigits(self):
        lower = 10 ** (13 - 1)
        upper = 10 ** 13 - 1
        return randint(lower, upper)

    def carduri_random(self, n: int):
        """
        Genereaza n carduri client random
        :param n: int
        :return:
        """
        nr_carduri_generate = 0
        while True:
            id_card_client = str(randint(1, 10000))
            name = ["Groza", "Marcu", "Sirbu", "Deac",
                    "Stavar", "Hociung", "Horoi", "Gherasim"]
            nume = choice(name)
            first_name = ["Camelia", "Ariana", "Iulia", "Cristian",
                          "Sebastian", "Iustin", "Vasile", "Gabriel"]
            prenume = choice(first_name)
            CNP = str(self.randomDigits())
            date_nastere = ["16.06.2002", "22.02.2002",
                            "15.03.2002", "12.07.1967", "02.04.1969"]
            data_nasterii = choice(date_nastere)
            date_inregistrari = ["15.11.2021", "16.11.2021",
                                 "17.11.2021", "18.11.2021"]
            data_inregistrarii = choice(date_inregistrari)
            card_client = CardClient(id_card_client, nume, prenume,
                                     CNP, data_nasterii,
                                     data_inregistrarii)
            if self.__card_client_repository.read(id_card_client) is None:
                nr_carduri_generate = nr_carduri_generate + 1
                self.__card_client_repository.adauga(card_client)
                if nr_carduri_generate == n:
                    break

    def cautare_full_text(self, text_cautat: str):
        """
        Cautare full text carduri
        :param text_cautat:
        :return:
        """
        for card in self.__card_client_repository.read():
            while True:
                text = str(card.id_entitate)
                if text_cautat in text:
                    print(card)
                    break
                text = str(card.nume)
                if text_cautat in text:
                    print(card)
                    break
                text = str(card.prenume)
                if text_cautat in text:
                    print(card)
                    break
                text = str(card.CNP)
                if text_cautat in text:
                    print(card)
                    break
                text = str(card.data_nasterii)
                if text_cautat in text:
                    print(card)
                    break
                text = str(card.data_inregistrarii)
                if text_cautat in text:
                    print(card)
                    break
                break
