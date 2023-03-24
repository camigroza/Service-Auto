from Domain.tranzactie import Tranzactie


class TranzactieValidator:
    """
    Validator pentru o tranzactie
    """
    def valideaza(self, tranzactie: Tranzactie):
        """
        Indica erorile aparute la introducerea datelor
        :param tranzactie: o tranzactie
        :return: o lista cu erorile aparute la introducerea datelor
        """
        erori = []
        if tranzactie.data[2] != '.' \
                or tranzactie.data[5] != '.' \
                or len(tranzactie.data) != 10:
            erori.append("Data nu este corect specificata! "
                         "Aceasta trebuie sa fie de forma DD.MM.YYYY")
        ziua = tranzactie.data[0] + tranzactie.data[1]
        luna = tranzactie.data[3] + tranzactie.data[4]
        if int(ziua) > 31:
            erori.append("O luna nu poate avea mai mult de 31 zile!")
        if int(luna) > 12:
            erori.append("Un an nu poate avea mai mult de 12 luni!")
        if tranzactie.ora[2] != ":":
            erori.append("Ora nu este corect specificata! "
                         "Aceasta trebuie sa fie de forma HH:MM")
        ore = tranzactie.ora[0] + tranzactie.ora[1]
        minute = tranzactie.ora[3] + tranzactie.ora[4]
        if int(ore) > 24:
            erori.append("O zi nu poate avea mai mult de 24 ore!")
        if int(minute) > 59:
            erori.append("Ora nu poate fi precizata cu mai mult de 59 minute!")
        if len(erori) > 0:
            raise ValueError(erori)
