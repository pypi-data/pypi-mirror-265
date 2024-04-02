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

def test_unit_cpuawkward_NumpyArray_fill_toint8_fromint16_1():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    tooffset = 0
    fromptr = [0, 1, 3]
    fromptr = (ctypes.c_int16*len(fromptr))(*fromptr)
    length = 3
    funcC = getattr(lib, 'awkward_NumpyArray_fill_toint8_fromint16')
    ret_pass = funcC(toptr, tooffset, fromptr, length)
    pytest_toptr = [0, 1, 3]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_fill_toint8_fromint16_2():
    toptr = []
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    tooffset = 0
    fromptr = []
    fromptr = (ctypes.c_int16*len(fromptr))(*fromptr)
    length = 0
    funcC = getattr(lib, 'awkward_NumpyArray_fill_toint8_fromint16')
    ret_pass = funcC(toptr, tooffset, fromptr, length)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_fill_toint8_fromint16_3():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    tooffset = 0
    fromptr = [1, 3, 3, 5]
    fromptr = (ctypes.c_int16*len(fromptr))(*fromptr)
    length = 4
    funcC = getattr(lib, 'awkward_NumpyArray_fill_toint8_fromint16')
    ret_pass = funcC(toptr, tooffset, fromptr, length)
    pytest_toptr = [1, 3, 3, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_fill_toint8_fromint16_4():
    toptr = [123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    tooffset = 0
    fromptr = [3, 5]
    fromptr = (ctypes.c_int16*len(fromptr))(*fromptr)
    length = 2
    funcC = getattr(lib, 'awkward_NumpyArray_fill_toint8_fromint16')
    ret_pass = funcC(toptr, tooffset, fromptr, length)
    pytest_toptr = [3, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_fill_toint8_fromint16_5():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    tooffset = 0
    fromptr = [0, 3, 3, 5, 6]
    fromptr = (ctypes.c_int16*len(fromptr))(*fromptr)
    length = 5
    funcC = getattr(lib, 'awkward_NumpyArray_fill_toint8_fromint16')
    ret_pass = funcC(toptr, tooffset, fromptr, length)
    pytest_toptr = [0, 3, 3, 5, 6]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

