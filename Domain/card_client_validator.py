from Domain.card_client import CardClient
from Domain.card_client_error import CardClientError
from Repository.repository import Repository


class CardClientValidator:
    """
    Validator pentru un card client
    """
    def __init__(self,
                 card_client_repository: Repository):
        self.card_client_repository = card_client_repository

    def valideaza(self, card_client: CardClient):
        """
        Indica toate erorile aparute la introducerea datelor
        :param card_client: un card client
        :return: o lista cu toate erorile aparute la introducerea datelor
        """
        erori = []
        if len(card_client.CNP) != 13:
            erori.append("CNP-ul nu este corect scris!")
        if card_client.data_nasterii[2] != '.' or \
                card_client.data_nasterii[5] != '.' or \
                len(card_client.data_nasterii) != 10:
            erori.append("Data nasterii nu este corect specificata. "
                         "Aceasta trebuie sa fie de forma DD.MM.YYYY")
        ziua = card_client.data_nasterii[0] + card_client.data_nasterii[1]
        luna = card_client.data_nasterii[3] + card_client.data_nasterii[4]
        if int(ziua) > 31:
            erori.append("Nu exista mai mult de 31 zile intr-o luna!")
        if int(luna) > 12:
            erori.append("Nu exista mai mult de 12 luni intr-un an!")
        if card_client.data_inregistrarii[2] != '.' or \
                card_client.data_inregistrarii[5] != '.' or \
                len(card_client.data_inregistrarii) != 10:
            erori.append("Data inregistrarii nu este corect specificata. "
                         "Aceasta trebuie sa fie de forma DD.MM.YYYY")
        z1 = card_client.data_inregistrarii[0]
        z2 = card_client.data_inregistrarii[1]
        ziua = z1 + z2
        l1 = card_client.data_inregistrarii[3]
        l2 = card_client.data_inregistrarii[4]
        luna = l1 + l2
        if int(ziua) > 31:
            erori.append("Nu exista mai mult de 31 zile intr-o luna!")
        if int(luna) > 12:
            erori.append("Nu exista mai mult de 12 luni intr-un an!")
        if len(erori) > 0:
            raise CardClientError(erori)

    def exist_id_card(self, id_card_client: str):
        """
        Verifica daca exista un card client cu id-ul dat
        :param id_card_client: string
        :return: True, daca exista un card cu id-ul dat, False in caz contrar
        """
        carduri = self.card_client_repository.read()
        for card in carduri:
            if card.id_entitate == id_card_client:
                return True
        return False

    def exist_cnp(self, cnp: str, id_card=None):
        """
        Verifica daca exista un card cu CNP-ul dat
        :param cnp: string
        :return: --> cand nu este specificat id_ul :
                True, daca exista un card cu CNP-ul dat, False in caz contrar
                 --> cand este specificat id-ul:
                True, daca mai exista un card cu CNP-ul dat inafara de cel cu
                 id-ul dat, False in caz contrar
        """
        carduri = self.card_client_repository.read()
        if id_card is None:
            for card in carduri:
                if card.CNP == cnp:
                    return True
            return False
        else:
            for card in carduri:
                if card.CNP == cnp and card.id_entitate != id_card:
                    return True
            return False
