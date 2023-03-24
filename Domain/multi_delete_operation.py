from Domain.entitate import Entitate
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository
from Repository.repository_reduceri_json import RepositoryReduceriJson


class MultiDeleteOperation(UndoRedoOperation):
    """
    Implementeaza undo si redo pentru multiple operatii de stergere
    """
    def __init__(self, repository: Repository,
                 repository_reduceri: RepositoryReduceriJson,
                 obiecte_sterse: list[Entitate]):
        self.__repository = repository
        self.__repository_reduceri = repository_reduceri
        self.__obiecte_sterse = obiecte_sterse

    def do_undo(self):
        for entitate in self.__obiecte_sterse:
            self.__repository.adauga(entitate)
            self.__repository_reduceri.adauga(entitate.id_entitate,
                                              self.__repository_reduceri.read(
                                                  entitate.id_entitate))

    def do_redo(self):
        for entitate in self.__obiecte_sterse:
            self.__repository.sterge(entitate.id_entitate)
            self.__repository_reduceri.sterge(entitate.id_entitate)
