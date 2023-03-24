import jsonpickle

from Domain.card_client import CardClient
from Domain.entitate import Entitate
from Repository.repository_in_memory import RepositoryInMemory


class RepositoryJson(RepositoryInMemory):
    """
    Repository cu fisiere json pentru entitati
    """
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def __read_file(self):
        """
        Citeste din fisier
        :return: dictionar gol daca nu exista date in fisier,
                dictionarul cu entitati in caz contrar
        """
        try:
            with open(self.filename, "r") as f:
                return jsonpickle.loads(f.read())
        except Exception:
            return {}

    def __write_file(self):
        """
        Scrie in fisier
        :return:
        """
        with open(self.filename, "w") as f:
            f.write(jsonpickle.dumps(self.entitati, indent=2))

    def read(self, id_entitate=None):
        """
        Functie de indicare entitati
        :param id_entitate: str
        :return: intreaga lista de entitati,
                daca nu se specifica un id entitate anume
                sau entitatea cu id-ul dat
                sau None, daca aceasta nu exista
        """
        self.entitati = self.__read_file()
        return super().read(id_entitate)

    def adauga(self, entitate: Entitate):
        """
        Adauga o entitate
        :param entitate: o entitate
        :return:
        """
        self.entitati = self.__read_file()
        super().adauga(entitate)
        self.__write_file()

    def sterge(self, id_entitate):
        """
        Sterge o entitate
        :param id_entitate: str
        :return:
        """
        self.entitati = self.__read_file()
        super().sterge(id_entitate)
        self.__write_file()

    def modifica(self, entitate: Entitate):
        """
        Modifica o entitate
        :param entitate: o entitate
        :return:
        """
        self.entitati = self.__read_file()
        super().modifica(entitate)
        self.__write_file()
