from dataclasses import dataclass

from Domain.entitate import Entitate


@dataclass
class CardClient(Entitate):
    """
    Descrie un card client
    """
    nume: str
    prenume: str
    CNP: str
    data_nasterii: str
    data_inregistrarii: str
