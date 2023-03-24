from Domain.card_client_validator import CardClientValidator
from Domain.masina_validator import MasinaValidator
from Domain.tranzactie_validator import TranzactieValidator

from Repository.repository_json import RepositoryJson
from Repository.repository_reduceri_json import RepositoryReduceriJson
from Service.card_client_service import CardClientService
from Service.masina_service import MasinaService
from Service.tranzactie_service import TranzactieService
from Service.undo_redo_service import UndoRedoService
from Tests.test_all import test_all
from UI.consola import Consola


def main():
    test_all()

    undo_redo_service = UndoRedoService()

    masina_repository_json = RepositoryJson("masini.json")
    masina_validator = MasinaValidator(masina_repository_json)
    masina_service = MasinaService(masina_repository_json, masina_validator,
                                   undo_redo_service)

    card_client_repository_json = RepositoryJson("carduri.json")
    card_client_validator = CardClientValidator(card_client_repository_json)
    card_client_service = CardClientService(card_client_repository_json,
                                            card_client_validator,
                                            undo_redo_service)

    repository_reduceri = RepositoryReduceriJson("reduceri.json")

    tranzactie_validator = TranzactieValidator()
    tranzactie_repository_json = RepositoryJson("tranzactii.json")
    tranzactie_service = TranzactieService(tranzactie_repository_json,
                                           tranzactie_validator,
                                           card_client_validator,
                                           masina_validator,
                                           masina_repository_json,
                                           repository_reduceri,
                                           card_client_repository_json,
                                           undo_redo_service)

    consola = Consola(masina_service, card_client_service,
                      tranzactie_service, repository_reduceri,
                      undo_redo_service)

    consola.run_menu()


if __name__ == "__main__":
    main()
