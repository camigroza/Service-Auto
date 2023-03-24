import jsonpickle

from Domain.card_client import CardClient
from Domain.card_client_validator import CardClientValidator
from Domain.masina import Masina
from Domain.masina_validator import MasinaValidator
from Domain.tranzactie import Tranzactie
from Domain.tranzactie_validator import TranzactieValidator
from Repository.repository_in_memory import RepositoryInMemory
from Repository.repository_reduceri_json import RepositoryReduceriJson
from Service.masina_service import MasinaService
from Service.tranzactie_service import TranzactieService
from Service.undo_redo_service import UndoRedoService


def test_ui_afisare_tranzactii_suma_interval():
    open("test_reduceri.json", 'w').close()
    with open("test_reduceri.json", "w") as f:
        f.write(jsonpickle.dumps({}))

    masina_repository = RepositoryInMemory()
    card_client_repository = RepositoryInMemory()
    tranzactie_repository = RepositoryInMemory()
    masina_validator = MasinaValidator(masina_repository)
    card_client_validator = CardClientValidator(card_client_repository)
    tranzactie_validator = TranzactieValidator()
    undo_redo_service = UndoRedoService()
    repository_reduceri = RepositoryReduceriJson("test_reduceri.json")
    tranzactie_service = TranzactieService(tranzactie_repository,
                                           tranzactie_validator,
                                           card_client_validator,
                                           masina_validator,
                                           masina_repository,
                                           repository_reduceri,
                                           card_client_repository,
                                           undo_redo_service)

    masina1 = Masina("1", "Tesla", 2021, 5000, "da")
    masina2 = Masina("2", "Tesla", 2021, 5000, "nu")
    card1 = CardClient("1", "Groza", "Camelia", "1231231231231",
                       "16.06.2002", "22.11.2021")
    card2 = CardClient("2", "Groza", "Camelia", "1231231231232",
                       "16.06.2002", "22.11.2021")
    tranzactie1 = Tranzactie("1", "1", "1", 500, 420, "22.11.2021", "01:17")
    tranzactie2 = Tranzactie("2", "2", "2", 500, 420, "22.11.2021", "01:17")

    masina_repository.adauga(masina1)
    masina_repository.adauga(masina2)
    card_client_repository.adauga(card1)
    card_client_repository.adauga(card2)
    tranzactie_repository.adauga(tranzactie1)
    tranzactie_repository.adauga(tranzactie2)

    ts = tranzactie_service

    rezultat = []
    rezultat = tranzactie_service.tranzactii_cu_suma_in_interval(0, 1000, ts.
                                                                 get_all(),
                                                                 rezultat)
    assert len(rezultat) == 2

    rezultat = []
    rezultat = tranzactie_service.tranzactii_cu_suma_in_interval(0, 1, ts.
                                                                 get_all(),
                                                                 rezultat)
    assert len(rezultat) == 0


def test_ui_ordonare_masini_descrescator_manopera():
    open("test_reduceri.json", 'w').close()
    with open("test_reduceri.json", "w") as f:
        f.write(jsonpickle.dumps({}))

    masina_repository = RepositoryInMemory()
    card_client_repository = RepositoryInMemory()
    tranzactie_repository = RepositoryInMemory()
    masina_validator = MasinaValidator(masina_repository)
    card_client_validator = CardClientValidator(card_client_repository)
    tranzactie_validator = TranzactieValidator()
    undo_redo_service = UndoRedoService()
    repository_reduceri = RepositoryReduceriJson("test_reduceri.json")
    tranzactie_service = TranzactieService(tranzactie_repository,
                                           tranzactie_validator,
                                           card_client_validator,
                                           masina_validator,
                                           masina_repository,
                                           repository_reduceri,
                                           card_client_repository,
                                           undo_redo_service)

    masina1 = Masina("1", "Tesla", 2021, 5000, "da")
    masina2 = Masina("2", "Tesla", 2021, 5000, "nu")
    card1 = CardClient("1", "Groza", "Camelia", "1231231231231",
                       "16.06.2002", "22.11.2021")
    card2 = CardClient("2", "Groza", "Camelia", "1231231231232",
                       "16.06.2002", "22.11.2021")
    tranzactie1 = Tranzactie("1", "1", "1", 500, 420, "22.11.2021", "01:17")
    tranzactie2 = Tranzactie("2", "2", "2", 500, 200, "22.11.2021", "01:17")

    masina_repository.adauga(masina1)
    masina_repository.adauga(masina2)
    card_client_repository.adauga(card1)
    card_client_repository.adauga(card2)
    tranzactie_repository.adauga(tranzactie1)
    tranzactie_repository.adauga(tranzactie2)

    rezultat = tranzactie_service.ordoneaza_desc_dupa_suma_manopera()
    assert len(rezultat) == 2


def test_ui_afisare_carduri_descrescator_reduceri():
    open("test_reduceri.json", 'w').close()
    with open("test_reduceri.json", "w") as f:
        f.write(jsonpickle.dumps({}))

    masina_repository = RepositoryInMemory()
    card_client_repository = RepositoryInMemory()
    tranzactie_repository = RepositoryInMemory()
    masina_validator = MasinaValidator(masina_repository)
    card_client_validator = CardClientValidator(card_client_repository)
    tranzactie_validator = TranzactieValidator()
    undo_redo_service = UndoRedoService()
    repository_reduceri = RepositoryReduceriJson("test_reduceri.json")
    tranzactie_service = TranzactieService(tranzactie_repository,
                                           tranzactie_validator,
                                           card_client_validator,
                                           masina_validator,
                                           masina_repository,
                                           repository_reduceri,
                                           card_client_repository,
                                           undo_redo_service)

    masina1 = Masina("1", "Tesla", 2021, 5000, "da")
    masina2 = Masina("2", "Tesla", 2021, 5000, "nu")
    card1 = CardClient("1", "Groza", "Camelia", "1231231231231",
                       "16.06.2002", "22.11.2021")
    card2 = CardClient("2", "Groza", "Camelia", "1231231231232",
                       "16.06.2002", "22.11.2021")

    masina_repository.adauga(masina1)
    masina_repository.adauga(masina2)
    card_client_repository.adauga(card1)
    card_client_repository.adauga(card2)

    reduceri = []
    tranzactie_service.adauga("1", "1", "1", 500, 420, "22.11.2021",
                              "01:17", reduceri)
    repository_reduceri.adauga("1", reduceri)
    reduceri = []
    tranzactie_service.adauga("2", "2", "2", 500, 200, "22.11.2021",
                              "01:17", reduceri)
    repository_reduceri.adauga("2", reduceri)

    rezultat = tranzactie_service.ordoneaza_carduri_desc_dupa_reduceri()
    assert len(rezultat) == 2


def test_ui_sterge_tranzactii_interval_zile():
    open("test_reduceri.json", 'w').close()
    with open("test_reduceri.json", "w") as f:
        f.write(jsonpickle.dumps({}))

    masina_repository = RepositoryInMemory()
    card_client_repository = RepositoryInMemory()
    tranzactie_repository = RepositoryInMemory()
    masina_validator = MasinaValidator(masina_repository)
    card_client_validator = CardClientValidator(card_client_repository)
    tranzactie_validator = TranzactieValidator()
    undo_redo_service = UndoRedoService()
    repository_reduceri = RepositoryReduceriJson("test_reduceri.json")
    tranzactie_service = TranzactieService(tranzactie_repository,
                                           tranzactie_validator,
                                           card_client_validator,
                                           masina_validator,
                                           masina_repository,
                                           repository_reduceri,
                                           card_client_repository,
                                           undo_redo_service)

    masina1 = Masina("1", "Tesla", 2021, 5000, "da")
    masina2 = Masina("2", "Tesla", 2021, 5000, "nu")
    card1 = CardClient("1", "Groza", "Camelia", "1231231231231",
                       "16.06.2002", "22.11.2021")
    card2 = CardClient("2", "Groza", "Camelia", "1231231231232",
                       "16.06.2002", "22.11.2021")
    tranzactie1 = Tranzactie("1", "1", "1", 500, 420, "22.11.2020", "01:17")
    tranzactie2 = Tranzactie("2", "2", "2", 500, 200, "22.11.2021", "01:17")

    masina_repository.adauga(masina1)
    masina_repository.adauga(masina2)
    card_client_repository.adauga(card1)
    card_client_repository.adauga(card2)
    tranzactie_repository.adauga(tranzactie1)
    tranzactie_repository.adauga(tranzactie2)

    data1 = "20.11.2020"
    data2 = "19.10.2021"
    tranzactie_service.sterge_tranzactii_interval_zile(data1, data2)
    assert tranzactie_repository.read("1") is None
    assert tranzactie_repository.read("2") is not None


def test_ui_actualizare_garantie_masini():
    open("test_reduceri.json", 'w').close()
    with open("test_reduceri.json", "w") as f:
        f.write(jsonpickle.dumps({}))

    masina_repository = RepositoryInMemory()
    card_client_repository = RepositoryInMemory()
    tranzactie_repository = RepositoryInMemory()
    masina_validator = MasinaValidator(masina_repository)
    undo_redo_service = UndoRedoService()
    masina_service = MasinaService(masina_repository, masina_validator,
                                   undo_redo_service)

    masina1 = Masina("1", "Tesla", 2021, 5000, "da")
    masina2 = Masina("2", "Tesla", 2021, 5000, "nu")
    card1 = CardClient("1", "Groza", "Camelia", "1231231231231",
                       "16.06.2002", "22.11.2021")
    card2 = CardClient("2", "Groza", "Camelia", "1231231231232",
                       "16.06.2002", "22.11.2021")
    tranzactie1 = Tranzactie("1", "1", "1", 500, 420, "22.11.2020", "01:17")
    tranzactie2 = Tranzactie("2", "2", "2", 500, 200, "22.11.2021", "01:17")

    masina_repository.adauga(masina1)
    masina_repository.adauga(masina2)
    card_client_repository.adauga(card1)
    card_client_repository.adauga(card2)
    tranzactie_repository.adauga(tranzactie1)
    tranzactie_repository.adauga(tranzactie2)

    masina_service.actualizare_garantie()
    assert masina_repository.read("1").garantie == "da"
    assert masina_repository.read("2").garantie == "da"
