import jsonpickle

from Domain.masina import Masina
from Repository.repository_json import RepositoryJson


def test_read_adauga_j():
    open("teste.json", 'w').close()
    with open("teste.json", "w") as f:
        f.write(jsonpickle.dumps({}))

    repository = RepositoryJson("teste.json")
    masina1 = Masina("1", "Tesla", 2021, 1000, "da")
    masina2 = Masina("2", "Tesla", 2021, 1000, "da")
    repository.adauga(masina1)
    repository.adauga(masina2)

    masini = repository.read()
    assert len(masini) == 2
    assert masini[0] == masina1
    assert masini[1] == masina2

    assert repository.read("1") == masina1
    assert repository.read("2") == masina2
    assert repository.read("3") is None


def test_sterge_j():
    open("teste.json", 'w').close()
    with open("teste.json", "w") as f:
        f.write(jsonpickle.dumps({}))

    repository = RepositoryJson("teste.json")
    masina1 = Masina("1", "Tesla", 2021, 1000, "da")
    masina2 = Masina("2", "Tesla", 2021, 1000, "da")
    repository.adauga(masina1)
    repository.adauga(masina2)

    repository.sterge("1")
    assert repository.read("1") is None
    assert repository.read("2") is not None

    repository.sterge("2")
    assert repository.read("1") is None
    assert repository.read("2") is None


def test_modifica_j():
    open("teste.json", 'w').close()
    with open("teste.json", "w") as f:
        f.write(jsonpickle.dumps({}))

    repository = RepositoryJson("teste.json")
    masina1 = Masina("1", "Tesla", 2021, 1000, "da")
    masina2 = Masina("2", "Tesla", 2021, 1000, "da")
    repository.adauga(masina1)
    repository.adauga(masina2)

    masina_noua = Masina("2", "BMW", 2020, 6000, "nu")
    repository.modifica(masina_noua)
    assert repository.read("1") == masina1
    assert repository.read("2") == masina_noua
