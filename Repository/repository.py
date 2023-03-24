from typing import Protocol

from Domain.entitate import Entitate


class Repository(Protocol):
    """
    Protocol pentru repository
    """
    def read(self, id_entitate=None):
        ...

    def adauga(self, entitate: Entitate):
        ...

    def sterge(self, id_entitate):
        ...

    def modifica(self, entitate: Entitate):
        ...
