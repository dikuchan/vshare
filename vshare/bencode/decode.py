import typing as tp

from .common import END, END_CODE, INTEGER_BEGIN, MAPPING_BEGIN, SEPARATOR, SEQUENCE_BEGIN
from .exceptions import ParseError

# TODO: Write proper decoder.


def decode_mapping(data: bytes) -> tuple[dict, bytes]:
    data = data[1:]
    values = {}
    while True:
        key, data = decode_impl(data)
        value, data = decode_impl(data)
        values[key] = value
        if not data:
            raise ParseError(f"Expected `{END!s}` at the end of mapping, got nothing")
        if data[0] == END_CODE:
            data = data[1:]
            break
    return values, data


def decode_sequence(data: bytes) -> tuple[list, bytes]:
    data = data[1:]
    values = []
    while True:
        value, data = decode_impl(data)
        values.append(value)
        if not data:
            raise ParseError(f"Expected `{END!s}` at the end of sequence, got nothing")
        if data[0] == END_CODE:
            data = data[1:]
            break
    return values, data


def decode_integer(data: bytes) -> tuple[int, bytes]:
    data = data[1:]
    try:
        index = data.index(END)
    except ValueError:
        raise ParseError(f"No `{END!s}` found when decoding integer")
    try:
        value = int(data[:index])
    except ValueError:
        raise ParseError("Declared size is not an integer")
    return value, data[index + 1:]  # fmt: skip


def decode_bytes(data: bytes) -> tuple[bytes, bytes]:
    try:
        index = data.index(SEPARATOR)
    except ValueError:
        raise ParseError(f"No `{SEPARATOR!s}` found when decoding bytes")
    try:
        size = int(data[:index])
    except ValueError:
        raise ParseError("Declared size is not an integer")
    data = data[index + 1:]  # fmt: skip
    if len(data) < size:
        raise ParseError("Not enough data for declared size")
    value = data[:size]
    return value, data[size:]


def decode_impl(data: bytes) -> tuple[tp.Any, bytes]:
    if data.startswith(MAPPING_BEGIN):
        return decode_mapping(data)
    if data.startswith(SEQUENCE_BEGIN):
        return decode_sequence(data)
    if data.startswith(INTEGER_BEGIN):
        return decode_integer(data)
    return decode_bytes(data)


def decode(data: bytes) -> tp.Any:
    if not isinstance(data, bytes):
        raise TypeError(f"Expected bytes to decode, got: `{type(data)}`")
    obj, _ = decode_impl(data)
    return obj


def decode_from_file(fp: tp.BinaryIO) -> tp.Any:
    return decode(fp.read())
