import jsonpickle

from Domain.card_client_validator import CardClientValidator
from Domain.masina_validator import MasinaValidator
from Domain.tranzactie_validator import TranzactieValidator
from Repository.repository_in_memory import RepositoryInMemory
from Repository.repository_reduceri_json import RepositoryReduceriJson
from Service.card_client_service import CardClientService
from Service.masina_service import MasinaService
from Service.tranzactie_service import TranzactieService
from Service.undo_redo_service import UndoRedoService


def test_undo_redo_CRUD():
    repository = RepositoryInMemory()
    validator = MasinaValidator(repository)
    undo_redo_service = UndoRedoService()
    service = MasinaService(repository, validator, undo_redo_service)

    service.adauga("1", "Tesla", 2021, 5000, "da")
    service.adauga("2", "Tesla", 2021, 5000, "nu")

    masini = service.get_all()
    assert len(masini) == 2
    assert repository.read("1") is not None
    assert repository.read("2") is not None

    undo_redo_service.undo()
    masini = service.get_all()
    assert len(masini) == 1
    assert repository.read("1") is not None
    assert repository.read("2") is None

    undo_redo_service.undo()
    masini = service.get_all()
    assert len(masini) == 0
    assert repository.read("1") is None
    assert repository.read("2") is None

    undo_redo_service.redo()
    masini = service.get_all()
    assert len(masini) == 1
    assert repository.read("1") is not None
    assert repository.read("2") is None

    undo_redo_service.redo()
    masini = service.get_all()
    assert len(masini) == 2
    assert repository.read("1") is not None
    assert repository.read("2") is not None

    service.sterge("1")

    undo_redo_service.undo()
    masini = service.get_all()
    assert len(masini) == 2
    assert repository.read("1") is not None
    assert repository.read("2") is not None

    undo_redo_service.redo()
    masini = service.get_all()
    assert len(masini) == 1
    assert repository.read("1") is None
    assert repository.read("2") is not None

    undo_redo_service.undo()
    service.modifica("1", "Audi", 2021, 5000, "da")

    undo_redo_service.undo()
    assert repository.read("1").model == "Tesla"

    undo_redo_service.redo()
    assert repository.read("1").model == "Audi"


def test_undo_redo_functionalitati():
    open("test_reduceri.json", 'w').close()
    with open("test_reduceri.json", "w") as f:
        f.write(jsonpickle.dumps({}))

    undo_redo_service = UndoRedoService()
    repository_reduceri = RepositoryReduceriJson("test_reduceri.json")

    masina_repository = RepositoryInMemory()
    masina_validator = MasinaValidator(masina_repository)
    masina_service = MasinaService(masina_repository, masina_validator,
                                   undo_redo_service)

    card_client_repository = RepositoryInMemory()
    card_client_validator = CardClientValidator(card_client_repository)
    card_client_service = CardClientService(card_client_repository,
                                            card_client_validator,
                                            undo_redo_service)

    tranzactie_repository = RepositoryInMemory()
    tranzactie_validator = TranzactieValidator()
    tranzactie_service = TranzactieService(tranzactie_repository,
                                           tranzactie_validator,
                                           card_client_validator,
                                           masina_validator, masina_repository,
                                           repository_reduceri,
                                           card_client_repository,
                                           undo_redo_service)

    tranzactie_service.adauga("1", "1", "1", 150, 450, "12.12.2021",
                              "01:08", [])
    tranzactie_service.adauga("2", "2", "2", 150, 450, "13.12.2021",
                              "01:08", [])
    tranzactie_service.adauga("3", "3", "3", 150, 450, "10.12.2020",
                              "01:08", [])

    tranzactie_service.sterge_tranzactii_interval_zile("12.12.2021",
                                                       "13.12.2021")

    undo_redo_service.undo()
    tranzactii = tranzactie_service.get_all()
    assert len(tranzactii) == 3
    assert tranzactie_repository.read("1") is not None
    assert tranzactie_repository.read("2") is not None
    assert tranzactie_repository.read("3") is not None

    undo_redo_service.redo()
    tranzactii = tranzactie_service.get_all()
    assert len(tranzactii) == 1
    assert tranzactie_repository.read("1") is None
    assert tranzactie_repository.read("2") is None
    assert tranzactie_repository.read("3") is not None

    masina_service.adauga("1", "Tesla", 2021, 100, "nu")

    masina_service.actualizare_garantie()

    undo_redo_service.undo()
    assert masina_repository.read("1").garantie == "nu"

    undo_redo_service.redo()
    assert masina_repository.read("1").garantie == "da"
