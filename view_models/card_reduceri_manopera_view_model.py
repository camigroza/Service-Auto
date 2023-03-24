from dataclasses import dataclass

from Domain.card_client import CardClient


@dataclass
class CardReduceriManoperaViewModel:
    card_client: CardClient
    reducere: float

    def __str__(self):
        return f'Cardul client: {self.card_client} \n\tbeneficiaza ' \
               f'de reduceri in valoare totala de {self.reducere} ron'
