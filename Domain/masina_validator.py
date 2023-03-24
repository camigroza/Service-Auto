from Domain.masina import Masina
from Domain.masina_error import MasinaError
from Repository.repository import Repository


class MasinaValidator:
    """
    Validator pentru o masina
    """
    def __init__(self, masina_repository: Repository):
        self.masina_repository = masina_repository

    def valideaza(self, masina: Masina):
        """
        Indica erorile aparute la introducerea datelor
        :param masina: o masina
        :return: o lista cu toate erorile aparute la introducerea datelor
        """
        erori = []
        if masina.an_achizitie <= 0:
            erori.append("Anul achizitiei trebuie sa fie strict pozitiv!")
        if masina.nr_km <= 0:
            erori.append("Numarul de km trebuie sa fie strict pozitiv!")
        if masina.garantie not in ["da", "nu"]:
            erori.append("Garantia trebuie specificata prin 'da' sau 'nu'!")
        if len(erori) > 0:
            raise MasinaError(erori)

    def are_garantie(self, id: str):
        """
        Verifica daca masina cu id-ul dat are garantie
        :param id: string
        :return: True, daca masina cu id-ul dat are garantie,
                False in caz contrar
        """
        if self.masina_repository.read() is None:
            masini = []
        else:
            masini = self.masina_repository.read()
        for masina in masini:
            if masina.id_entitate == id:
                if masina.garantie == "da":
                    return True
        return False
