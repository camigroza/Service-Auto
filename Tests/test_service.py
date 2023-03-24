from Domain.card_client import CardClient
from Domain.card_client_validator import CardClientValidator
from Domain.masina import Masina
from Domain.masina_validator import MasinaValidator
from Repository.repository_in_memory import RepositoryInMemory
from Service.card_client_service import CardClientService
from Service.masina_service import MasinaService
from Service.undo_redo_service import UndoRedoService


def test_get_all_adauga_s():
    repository = RepositoryInMemory()
    validator = MasinaValidator(repository)
    undo_redo_service = UndoRedoService()
    service = MasinaService(repository, validator, undo_redo_service)
    masina1 = Masina("1", "Tesla", 2021, 1000, "da")
    masina2 = Masina("2", "Tesla", 2021, 1000, "da")
    service.adauga("1", "Tesla", 2021, 1000, "da")
    service.adauga("2", "Tesla", 2021, 1000, "da")

    masini = service.get_all()
    assert len(masini) == 2
    assert masini[0] == masina1
    assert masini[1] == masina2

    repository_c = RepositoryInMemory()
    validator_c = CardClientValidator(repository_c)
    service_c = CardClientService(repository_c, validator_c, undo_redo_service)
    service_c.adauga("1", "Groza", "Camelia", "1231231231231",
                     "16.06.2002", "21.11.2021")
    service_c.adauga("2", "Groza", "Camelia", "1112223331112",
                     "16.06.2002", "21.11.2021")

    carduri = service_c.get_all()
    assert len(carduri) == 2

    service_c.adauga("3", "Groza", "Camelia", "1231231231231",
                     "16.06.2002", "21.11.2021")

    carduri = service_c.get_all()
    assert len(carduri) == 2


def test_sterge_s():
    repository = RepositoryInMemory()
    validator = MasinaValidator(repository)
    undo_redo_service = UndoRedoService()
    service = MasinaService(repository, validator, undo_redo_service)
    service.adauga("1", "Tesla", 2021, 1000, "da")
    service.adauga("2", "Tesla", 2021, 1000, "da")

    service.sterge("1")
    masini = service.get_all()
    assert len(masini) == 1
    assert masini[0] == Masina("2", "Tesla", 2021, 1000, "da")

    service.sterge("2")
    masini = service.get_all()
    assert len(masini) == 0


def test_modifica_s():
    repository = RepositoryInMemory()
    validator = MasinaValidator(repository)
    undo_redo_service = UndoRedoService()
    service = MasinaService(repository, validator, undo_redo_service)
    service.adauga("1", "Tesla", 2021, 1000, "da")
    service.adauga("2", "Tesla", 2021, 1000, "da")

    service.modifica("1", "BMW", 2020, 6000, "nu")
    masini = service.get_all()
    assert masini[0] == Masina("1", "BMW", 2020, 6000, "nu")
    assert masini[1] == Masina("2", "Tesla", 2021, 1000, "da")

    repository_c = RepositoryInMemory()
    validator_c = CardClientValidator(repository_c)
    service_c = CardClientService(repository_c, validator_c, undo_redo_service)
    service_c.adauga("1", "Groza", "Camelia", "1231231231231",
                     "16.06.2002", "21.11.2021")
    service_c.adauga("2", "Groza", "Camelia", "1112223331112",
                     "16.06.2002", "21.11.2021")

    service_c.modifica("2", "Marcu", "Ariana", "1231231231231",
                       "15.03.2002", "21.11.2021")
    carduri = service_c.get_all()
    assert carduri[0] == CardClient("1", "Groza", "Camelia", "1231231231231",
                                    "16.06.2002", "21.11.2021")
    assert carduri[1] == CardClient("2", "Groza", "Camelia", "1112223331112",
                                    "16.06.2002", "21.11.2021")

    service_c.modifica("2", "Marcu", "Ariana", "4564564564564", "15.03.2002",
                       "21.11.2021")
    carduri = service_c.get_all()
    assert carduri[0] == CardClient("1", "Groza", "Camelia", "1231231231231",
                                    "16.06.2002", "21.11.2021")
    assert carduri[1] == CardClient("2", "Marcu", "Ariana", "4564564564564",
                                    "15.03.2002", "21.11.2021")

    service_c.modifica("2", "Sirbu", "Iulia", "4564564564564",
                       "15.07.2002", "21.11.2021")
    carduri = service_c.get_all()
    assert carduri[0] == CardClient("1", "Groza", "Camelia", "1231231231231",
                                    "16.06.2002", "21.11.2021")
    assert carduri[1] == CardClient("2", "Sirbu", "Iulia", "4564564564564",
                                    "15.07.2002", "21.11.2021")
