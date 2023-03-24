import random
from datetime import date
from random import randint, choice

from Domain.add_operation import AddOperation
from Domain.delete_operation import DeleteOperation
from Domain.masina import Masina
from Domain.masina_validator import MasinaValidator
from Domain.modify_operation import ModifyOperation
from Domain.multi_modify_operation import MultiModifyOperation
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService


class MasinaService:
    """
    Service pentru o masina
    """

    def __init__(self, masina_repository: Repository,
                 masina_validator: MasinaValidator,
                 undo_redo_service: UndoRedoService):
        self.__masina_repository = masina_repository
        self.__masina_validator = masina_validator
        self.__undo_redo_service = undo_redo_service

    def get_all(self):
        """
        Indica toate masinile
        :return:
        """
        return self.__masina_repository.read()

    def adauga(self, id_masina: str, model: str, an_achizitie: int,
               nr_km: float, garantie: str):
        """
        Adauga o masina
        :param id_masina: string
        :param model: string
        :param an_achizitie: int
        :param nr_km: float
        :param garantie: string
        :return:
        """
        masina = Masina(id_masina, model, an_achizitie,
                        nr_km, garantie)
        self.__masina_validator.valideaza(masina)
        self.__masina_repository.adauga(masina)
        self.__undo_redo_service.adauga_undo_operation(AddOperation(
            self.__masina_repository, masina))

    def sterge(self, id_masina):
        """
        Sterge masina cu id-ul dat
        :param id_masina: string
        :return:
        """
        masina = self.__masina_repository.read(id_masina)
        self.__masina_repository.sterge(id_masina)
        self.__undo_redo_service.adauga_undo_operation(DeleteOperation(
            self.__masina_repository, masina))

    def modifica(self, id_masina: str, model: str, an_achizitie: int,
                 nr_km: float, garantie: str):
        """
        Modifica o masina
        :param id_masina: string
        :param model: string
        :param an_achizitie: int
        :param nr_km: float
        :param garantie: string
        :return:
        """
        masina_veche = self.__masina_repository.read(id_masina)
        masina = Masina(id_masina, model, an_achizitie,
                        nr_km, garantie)
        self.__masina_validator.valideaza(masina)
        self.__masina_repository.modifica(masina)
        self.__undo_redo_service.adauga_undo_operation(ModifyOperation(
            self.__masina_repository, masina_veche, masina))

    def masini_random(self, n: int):
        """
        Genereaza n masini random
        :param n: int
        :return:
        """
        nr_masini_generate = 0
        while True:
            id_masina = str(randint(1, 10000))
            modele = ["Tesla", "Fiat", "BMW", "Audi", "Toyota", "Ford"]
            model = choice(modele)
            an_achizitie = randint(1500, 2030)
            nr_km = random.uniform(0.0, 500000.0)
            garantii = ["da", "nu"]
            garantie = choice(garantii)
            masina = Masina(id_masina, model, an_achizitie,
                            nr_km, garantie)
            if self.__masina_repository.read(id_masina) is None:
                nr_masini_generate = nr_masini_generate + 1
                self.__masina_repository.adauga(masina)
                if nr_masini_generate == n:
                    break

    def actualizare_garantie(self):
        """
        Actualizarea garantiei la fiecare masina
        :return:
        """
        masini_vechi = {}
        masini_noi = {}

        for masina in self.__masina_repository.read():
            id_masina = masina.id_entitate
            model = masina.model
            an_achizitie = masina.an_achizitie
            nr_km = masina.nr_km
            current_year = date.today().year
            masini_vechi[id_masina] = masina
            if current_year - an_achizitie <= 3 and nr_km <= 60000:
                garantie = "da"
            else:
                garantie = "nu"
            masina_update = Masina(id_masina, model,
                                   an_achizitie, nr_km, garantie)
            self.__masina_repository.modifica(masina_update)
            masini_noi[id_masina] = masina_update

        self.__undo_redo_service.adauga_undo_operation(MultiModifyOperation(
            self.__masina_repository, masini_vechi, masini_noi))

    def cautare_full_text(self, text_cautat: str):
        """
        Cautare full text masini
        :param text_cautat: textul cautat
        :return:
        """
        for masina in self.__masina_repository.read():
            while True:
                text = str(masina.id_entitate)
                if text_cautat in text:
                    print(masina)
                    break
                text = str(masina.model)
                if text_cautat in text:
                    print(masina)
                    break
                text = str(masina.an_achizitie)
                if text_cautat in text:
                    print(masina)
                    break
                text = str(int(masina.nr_km))
                if text_cautat in text:
                    print(masina)
                    break
                text = str(masina.garantie)
                if text_cautat in text:
                    print(masina)
                    break
                break
