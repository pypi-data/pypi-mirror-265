# AUTO GENERATED ON 2024-04-01 AT 18:26:47
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-tests.py
#

# fmt: off

import ctypes
import pytest

from awkward_cpp.cpu_kernels import lib

def test_unit_cpuawkward_BitMaskedArray_to_IndexedOptionArray64_1():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    bitmasklength = 0
    frombitmask = []
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    lsb_order = False
    validwhen = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_IndexedOptionArray64')
    ret_pass = funcC(toindex, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_BitMaskedArray_to_IndexedOptionArray64_2():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    bitmasklength = 2
    frombitmask = [58, 59]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    lsb_order = True
    validwhen = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_IndexedOptionArray64')
    ret_pass = funcC(toindex, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_toindex = [0, -1, 2, -1, -1, -1, 6, 7, -1, -1, 10, -1, -1, -1, 14, 15]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

