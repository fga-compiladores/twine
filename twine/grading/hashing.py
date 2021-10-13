from base64 import b64encode
from hashlib import md5
from functools import singledispatch


def check_value(value, typ=object, hash=None, check=(), name="var"):
    if not isinstance(value, typ):
        raise ValueError(
            f"Esperava que {name} fosse um(a) {typ.__name__}, "
            f"mas obtive {type(value).__name__}."
        )

    for fn in check:
        fn(value)

    if hash is not None:
        computed = human_hash(value)
        assert (
            computed == hash
        ), f"""
hash inválida para {name} = {value!r}!
  - obtida   : {computed}
  - esperada : {hash}

O valor obtido não corresponde ao registrado no banco de respostas.
"""


def human_hash(x):
    """
    Return a human-readable hash of the given content.
    """
    h = special_hash(x)
    return b64encode(h).decode("ascii")


@singledispatch
def special_hash(x) -> bytes:
    raise NotImplementedError


@special_hash.register(int)
def _int(x):
    return b64encode(x.to_bytes(32, "").lstrip("\x00"))


@special_hash.register(str)
def _str(x):
    hasher = md5(x.encode("utf8"))
    return hasher.digest()


@special_hash.register(tuple)
@special_hash.register(list)
def _seq(xs):
    hasher = md5()
    for x in xs:
        hasher.update(special_hash(x))
    return f"{len(xs)}:".encode("ascii") + hasher.digest()
