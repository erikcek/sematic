# Standard Library
from abc import ABC, ABCMeta, abstractmethod
from dataclasses import dataclass
from sematic.types.serialization import _is_dataclass, \
    binary_to_string, binary_from_string, type_from_json_encodable, type_to_json_encodable, _get_key, _type_repr
import base64
from typing import Dict

# Third-party
import pytest


######################################################
# _id_dataclass tests
######################################################
def test_is_dataclass_on_dataclass_instance():
    @dataclass
    class A:
        pass

    assert _is_dataclass(A) == True


def test_is_dataclass_on_non_dataclass_instance():
    class B:
        pass

    assert _is_dataclass(B) == False


def test_is_dataclass_on_instance_with_parent_dataclass():
    @dataclass
    class C:
        pass

    class D(C):
        pass
    assert _is_dataclass(C) == True
    assert _is_dataclass(D) == False

######################################################
# binary serialization tests
######################################################


def test_decode_string_valid_base64():
    assert binary_to_string(base64.b64decode("test".encode("ascii"))) == "test"

# def test_decode_string_special_chars_base64():
#     assert binary_to_string(binary_from_string("šččťžô")) == "šččťžô"

def test_encode_decode_series():
    assert binary_to_string(binary_from_string("test")) == "test"


######################################################
# binary serialization tests
######################################################

GET_KEY_EXAMPLES = [(float, "float"), (int, "int"), (str, 'str'), (bool, "bool")]


@pytest.mark.parametrize("type, key", GET_KEY_EXAMPLES)
def test_get_key(type, key):
    assert _get_key(type) == key