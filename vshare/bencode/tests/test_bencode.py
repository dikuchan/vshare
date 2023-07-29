import pathlib
import typing as tp

import pytest

from ..decode import decode, decode_from_file
from ..encode import encode, encode_to_file
from ..exceptions import ParseError

TEST_DATA = [
    1,
    b"abc",
    [b"a", 1],
    [b"Hello, world!", 1024],
    {b"a": 1},
    {b"a": 1, b"b": b"abc", b"c": [1, 2, 3]},
    {
        b"file": {
            b"name": b"testfile.txt",
            b"size": 1024,
            b"tags": [b"movie", b"action"],
        },
        b"peer": {
            b"username": b"testuser",
            b"ports": [22, 443],
        },
    },
]


@pytest.mark.parametrize("data", TEST_DATA)
def test_encode_and_decode(data: tp.Any) -> None:
    encoded_data = encode(data)
    decoded_data = decode(encoded_data)
    assert data == decoded_data


def test_decode_error() -> None:
    data = {"a": 1, "b": 2}
    encoded_data = encode(data)
    encoded_data = encoded_data[:-1]
    with pytest.raises(ParseError):
        decode(encoded_data)


def test_decode_sample_file(sample_file: tp.BinaryIO) -> None:
    decoded_data = decode_from_file(sample_file)
    encode(decoded_data)


def test_decode_debian_file(debian_file: tp.BinaryIO) -> None:
    decoded_data = decode_from_file(debian_file)
    encode(decoded_data)


def test_encode_to_file(tmp_file: tp.BinaryIO) -> None:
    obj = TEST_DATA[-1]
    encode_to_file(obj, tmp_file)


@pytest.fixture
def sample_file() -> tp.Iterator[tp.BinaryIO]:
    with open("./bencode/tests/data/sample", "rb") as file:
        yield file


@pytest.fixture
def debian_file() -> tp.Iterator[tp.BinaryIO]:
    with open("./bencode/tests/data/debian", "rb") as file:
        yield file


@pytest.fixture
def tmp_file(tmp_path: pathlib.Path) -> tp.Iterator[tp.BinaryIO]:
    filepath = tmp_path / "testfile"
    with filepath.open("wb") as file:
        yield file
