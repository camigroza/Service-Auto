from Tests.test_functionalitati import \
    test_ui_afisare_tranzactii_suma_interval, \
    test_ui_ordonare_masini_descrescator_manopera, \
    test_ui_afisare_carduri_descrescator_reduceri, \
    test_ui_sterge_tranzactii_interval_zile, \
    test_ui_actualizare_garantie_masini
from Tests.test_repository_in_memory import test_read_adauga, \
    test_sterge, test_modifica
from Tests.test_repository_json import test_read_adauga_j, \
    test_sterge_j, test_modifica_j
from Tests.test_service import test_get_all_adauga_s, \
    test_sterge_s, test_modifica_s
from Tests.test_undo_redo import test_undo_redo_CRUD, \
    test_undo_redo_functionalitati


def test_all():
    test_read_adauga()
    test_sterge()
    test_modifica()
    test_read_adauga_j()
    test_sterge_j()
    test_modifica_j()
    test_get_all_adauga_s()
    test_sterge_s()
    test_modifica_s()
    test_ui_afisare_tranzactii_suma_interval()
    test_ui_ordonare_masini_descrescator_manopera()
    test_ui_afisare_carduri_descrescator_reduceri()
    test_ui_sterge_tranzactii_interval_zile()
    test_ui_actualizare_garantie_masini()
    test_undo_redo_CRUD()
    test_undo_redo_functionalitati()
