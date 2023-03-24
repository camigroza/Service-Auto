from Domain.entitate import Entitate
from Repository.repository import Repository


class RepositoryInMemory(Repository):
    """
    Repository in memorie pentru entitati
    """
    def __init__(self):
        self.entitati = {}

    def read(self, id_entitate=None):
        """
        Functie de indicare entitati
        :param id_entitate: str
        :return: intreaga lista de entitati,
                daca nu se specifica un id entitate anume
                sau entitatea cu id-ul dat
                sau None, daca aceasta nu exista
        """
        if id_entitate is None:
            return list(self.entitati.values())

        if id_entitate in self.entitati:
            return self.entitati[id_entitate]
        else:
            return None

    def adauga(self, entitate: Entitate):
        """
        Adauga o entitate
        :param entitate: o entitate
        :return:
        """
        if self.read(entitate.id_entitate) is not None:
            raise KeyError("Exista deja o entitate cu id-ul dat!")
        self.entitati[entitate.id_entitate] = entitate

    def sterge(self, id_entitate):
        """
        Sterge o entitate
        :param id_entitate: str
        :return:
        """
        if self.read(id_entitate) is None:
            raise KeyError("Nu exista o entitate cu id-ul dat!")
        del self.entitati[id_entitate]

    def modifica(self, entitate: Entitate):
        """
        Modifica o entitate
        :param entitate: o entitate
        :return:
        """
        if self.read(entitate.id_entitate) is None:
            raise KeyError("Nu exista o entitate cu id-ul dat!")
        self.entitati[entitate.id_entitate] = entitate
