import pytest


@pytest.fixture
def info(twine):
    from twine import info

    return info


def get(mod, *names):
    for name in names:
        try:
            return getattr(mod, name)
        except AttributeError:
            pass
    return None


def test_renomeou_variáveis_do_módulo_info(info):

    names = set(vars(info))
    assert not {"nome", "matricula"}.issubset(
        names
    ), """Vamos usar nomes de variáveis em inglês! Renomeie:
   - nome      => name
   - matricula => school_id
"""
    assert {"name", "school_id"}.issubset(names)


def test_variáveis_não_possuem_valores_padrão(info):
    assert get(info, "name", "nome") != "Nome Completo", "Preencha com seu nome"
    assert (
        get(info, "school_id", "matricula") != "12/3456789"
    ), "Preencha com sua matrícula"
