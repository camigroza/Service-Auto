import jsonpickle


class RepositoryReduceriJson:
    """
    Repository pentru reducerile acordate tranzactiilor
    """
    def __init__(self, filename):
        self.reduceri = {}
        self.filename = filename

    def __read_file(self):
        """
        Citeste din fisier
        :return: dictionar gol daca nu exista date in fisier,
                dictionarul cu reducerile in caz contrar
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
            f.write(jsonpickle.dumps(self.reduceri, indent=2))

    def read(self, id_tranzactie=None):
        """
        Indica reducerile acordate unei tranzactii
        :param id_tranzactie: string
        :return:
        """
        if id_tranzactie is None:
            self.reduceri = self.__read_file()
            return self.reduceri
        else:
            self.reduceri = self.__read_file()
            if id_tranzactie in self.reduceri:
                return self.reduceri[id_tranzactie]
            else:
                return []

    def adauga(self, id_tranzactie: str, lista_reduceri: list):
        """
        Adauga reducerile acordate unei tranzactii
        :param id_tranzactie: string
        :param lista_reduceri: o lista
        :return:
        """
        self.reduceri[id_tranzactie] = []
        if len(lista_reduceri) > 0:
            for i in range(len(lista_reduceri)):
                if lista_reduceri[i] == 1:
                    self.reduceri[id_tranzactie].append("A fost aplicata "
                                                        "o reducere de 10% "
                                                        "pentru manopera.")
                elif lista_reduceri[i] == 2:
                    self.reduceri[id_tranzactie].append("Piesele sunt gratis.")
        else:
            self.reduceri[id_tranzactie].append("Nu a fost aplicata nici "
                                                "o reducere.")
        self.__write_file()

    def sterge(self, id_tranzactie: str):
        """
        Sterge reducerile asociate unei tranzactii
        :param id_tranzactie:
        :return:
        """
        self.reduceri = self.__read_file()
        if id_tranzactie in self.reduceri:
            del self.reduceri[id_tranzactie]
        self.__write_file()
