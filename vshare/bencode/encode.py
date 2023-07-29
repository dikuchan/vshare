import collections.abc
import typing as tp

from .common import END, INTEGER_BEGIN, MAPPING_BEGIN, SEPARATOR, SEQUENCE_BEGIN

# TODO: Write proper encoder.


def concat_bytes(*chunks: bytes) -> bytes:
    return b"".join(chunks)


def encode_mapping(obj: collections.abc.Mapping) -> bytes:
    values = []
    obj = {key: value for key, value in obj.items()}
    for key, value in sorted(obj.items()):
        values.append(encode(key))
        values.append(encode(value))
    return concat_bytes(MAPPING_BEGIN, *values, END)


def encode_sequence(obj: collections.abc.Sequence) -> bytes:
    values = (encode(value) for value in obj)
    return concat_bytes(SEQUENCE_BEGIN, *values, END)


def encode_integer(obj: int) -> bytes:
    value = str(obj).encode()
    return concat_bytes(INTEGER_BEGIN, value, END)


def encode_string(obj: str) -> bytes:
    return encode_bytes(obj.encode())


def encode_bytes(obj: bytes) -> bytes:
    size = str(len(obj)).encode()
    return concat_bytes(size, SEPARATOR, obj)


def encode(obj: tp.Any) -> bytes:
    if isinstance(obj, bytes):
        return encode_bytes(obj)
    if isinstance(obj, str):
        return encode_string(obj)
    if isinstance(obj, int):
        return encode_integer(obj)
    if isinstance(obj, collections.abc.Sequence):
        return encode_sequence(obj)
    if isinstance(obj, collections.abc.Mapping):
        return encode_mapping(obj)
    raise TypeError(f"Unsupported type to encode: `{type(obj)}`")


def encode_to_file(obj: tp.Any, fp: tp.BinaryIO) -> None:
    fp.write(encode(obj))
