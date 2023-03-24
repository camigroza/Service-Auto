from dataclasses import dataclass

from Domain.entitate import Entitate


@dataclass
class Masina(Entitate):
    """
    Descrie o masina
    """
    model: str
    an_achizitie: int
    nr_km: float
    garantie: str
