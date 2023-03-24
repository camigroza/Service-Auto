from Domain.entitate import Entitate
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class MultiModifyOperation(UndoRedoOperation):
    """
    Implementeaza undo si redo pentru multiple operatii de modificare
    """
    def __init__(self, repository: Repository, obiecte_vechi: dict,
                 obiecte_noi: dict):
        self.__repository = repository
        self.__obiecte_vechi = obiecte_vechi
        self.__obiecte_noi = obiecte_noi

    def do_undo(self):
        for id_entitate in self.__obiecte_noi:
            self.__repository.modifica(self.__obiecte_vechi[id_entitate])

    def do_redo(self):
        for id_entitate in self.__obiecte_vechi:
            self.__repository.modifica(self.__obiecte_noi[id_entitate])
