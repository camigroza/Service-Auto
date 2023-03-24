from dataclasses import dataclass

from Domain.entitate import Entitate


@dataclass
class Tranzactie(Entitate):
    """
    Descrie o tranzactie
    """
    id_masina: str
    id_card_client: str
    suma_piese: float
    suma_manopera: float
    data: str
    ora: str
