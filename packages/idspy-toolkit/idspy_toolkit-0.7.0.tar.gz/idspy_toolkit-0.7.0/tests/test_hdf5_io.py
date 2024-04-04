import pytest
import h5py
from tests.classes_skels import *
from idspy_toolkit.converter import ids_to_hdf5, hdf5_to_ids
from random import randrange
from typing import Union
from idspy_dictionaries import ids_gyrokinetics_local as gkids
import idspy_toolkit
import numpy as np


@pytest.fixture(scope="function")
def hdf5_file(tmp_path_factory):
    fn = tmp_path_factory.mktemp("data") / "class_ids_{0:04d}.h5".format(randrange(0, 9999))
    return fn


def test_eigenmode_write(hdf5_file):
    ids = gkids.Eigenmode()
    idspy_toolkit.fill_default_values_ids(new_ids=ids)
    ids.code.parameters = '{"a":2}'
    ids.code.output_flag = 2
    assert ids_to_hdf5(ids, hdf5_file) == (2, 2)
    ids_read = gkids.Eigenmode()
    idspy_toolkit.fill_default_values_ids(new_ids=ids_read)
    hdf5_to_ids(hdf5_file, ids_read, todict=False)
    assert ids_read.code.parameters == ids.code.parameters
    assert ids_read.code.output_flag == ids.code.output_flag


def test_eigenmode_overwrite(hdf5_file):
    ids = gkids.Eigenmode()
    idspy_toolkit.fill_default_values_ids(new_ids=ids)
    ids.code.parameters = '{"a":2}'
    ids.code.output_flag = 2
    assert ids_to_hdf5(ids, hdf5_file, overwrite=True) == (2, 2)
    ids_read = gkids.Eigenmode()
    idspy_toolkit.fill_default_values_ids(new_ids=ids_read)
    hdf5_to_ids(hdf5_file, ids_read, todict=False)
    assert ids_read.code.parameters == ids.code.parameters
    assert ids_read.code.output_flag == ids.code.output_flag
    ids.code.output_flag = 42
    ids.code.parameters = '{"a":3}'
    assert ids_to_hdf5(ids, hdf5_file, overwrite=True) == (2, 2)
    ids_read = gkids.Eigenmode()
    idspy_toolkit.fill_default_values_ids(new_ids=ids_read)
    hdf5_to_ids(hdf5_file, ids_read, todict=False)
    assert ids_read.code.parameters == ids.code.parameters
    assert ids_read.code.output_flag == ids.code.output_flag


def test_eigenmode_write_wrong_type(hdf5_file):
    ids = gkids.Eigenmode()
    idspy_toolkit.fill_default_values_ids(new_ids=ids)
    ids.code.parameters = '{"a":2}'
    ids.code.output_flag = 2
    assert ids_to_hdf5(ids, hdf5_file) == (2, 2)
    ids_read = gkids.Eigenmode()
    idspy_toolkit.fill_default_values_ids(new_ids=ids_read)
    hdf5_to_ids(hdf5_file, ids_read, todict=False)
    assert ids_read.code.parameters == ids.code.parameters
    np.testing.assert_array_equal(ids_read.code.output_flag, ids.code.output_flag)


def test_class_dict_conversion(hdf5_file):
    ids = gkids.Eigenmode()
    idspy_toolkit.fill_default_values_ids(new_ids=ids)
    ids.code.parameters = '{"a":2}'
    ids.code.output_flag = 2
    assert ids_to_hdf5(ids, hdf5_file) == (2, 2)
    ids_read = gkids.Eigenmode()
    idspy_toolkit.fill_default_values_ids(new_ids=ids_read)
    hdf5_to_ids(hdf5_file, ids_read, todict=True)
    assert isinstance(ids_read.code.parameters, dict) is True
    assert ids_read.code.parameters == {"a": 2}
    np.testing.assert_array_equal(ids_read.code.output_flag, ids.code.output_flag)


def test_class_dict_no_conversion(hdf5_file):
    ids = gkids.Eigenmode()
    idspy_toolkit.fill_default_values_ids(new_ids=ids)
    ids.code.parameters = {"a": 2}
    ids.code.output_flag = 2
    assert ids_to_hdf5(ids, hdf5_file) == (2, 2)
    ids_read = gkids.Eigenmode()
    idspy_toolkit.fill_default_values_ids(new_ids=ids_read)
    hdf5_to_ids(hdf5_file, ids_read, todict=False)
    assert isinstance(ids_read.code.parameters, dict) is False
    assert isinstance(ids_read.code.parameters, str) is True
    assert ids_read.code.parameters == '<root><a type="int">2</a></root>'


def test_class_dict_conversion_in_list(hdf5_file):
    ids = gkids.Eigenmode()
    idspy_toolkit.fill_default_values_ids(new_ids=ids)
    ids.code.parameters = {"a": 2, "b": {"c": 4}}
    ids.code.output_flag = 2

    ids_wavevector = gkids.Wavevector()
    ids_wavevector.radial_wavevector_norm = 4.
    ids_wavevector.binormal_wavevector_norm = 2.
    ids_wavevector.eigenmode.append(ids)
    assert ids_to_hdf5(ids_wavevector, hdf5_file) == (3, 4)
    ids_read = gkids.Wavevector()
    idspy_toolkit.fill_default_values_ids(new_ids=ids_read)
    hdf5_to_ids(hdf5_file, ids_read, todict=True)
    assert isinstance(ids_read.eigenmode[0].code.parameters, dict) is True
    assert ids_read.eigenmode[0].code.parameters.get("a") == 2
    assert ids_read.eigenmode[0].code.parameters.get("b").get("c") == 4


def test_class_dict_no_conversion_in_list(hdf5_file):
    ids = gkids.Eigenmode()
    idspy_toolkit.fill_default_values_ids(new_ids=ids)
    ids.code.parameters = {"a": 2, "b": {"c": 4}}
    ids.code.output_flag = 2

    ids_wavevector = gkids.Wavevector()
    ids_wavevector.radial_wavevector_norm = 4.
    ids_wavevector.binormal_wavevector_norm = 2.
    ids_wavevector.eigenmode.append(ids)
    assert ids_to_hdf5(ids_wavevector, hdf5_file) == (3, 4)
    ids_read = gkids.Wavevector()
    idspy_toolkit.fill_default_values_ids(new_ids=ids_read)
    hdf5_to_ids(hdf5_file, ids_read, todict=False)
    assert isinstance(ids_read.eigenmode[0].code.parameters, dict) is False
    assert isinstance(ids_read.eigenmode[0].code.parameters, str) is True
    assert ids_read.eigenmode[
               0].code.parameters == '<root><a type="int">2</a><b type="dict"><c type="int">4</c></b></root>'


def test_class_dict_format(hdf5_file):
    test = ClassListMixDict()
    assert ids_to_hdf5(test, hdf5_file) == (1, 4)
    ids_read = ClassListMixDict([], -999, "", {})
    hdf5_to_ids(hdf5_file, ids_read, todict=True)
    #   print("output", ids_read)
    assert test.space == ids_read.space
    assert test.name == ids_read.name
    assert all([a == b for a, b in zip(sorted(test.time), sorted(ids_read.time))])


def test_empty_array(hdf5_file):
    test = ArrayClass()
    assert ids_to_hdf5(test, hdf5_file) == (1, 2)
    ids_read = ArrayClass()
    hdf5_to_ids(hdf5_file, ids_read, fill=True, todict=True)
    assert ids_read.val_0d == 999.999
    assert isinstance(ids_read.val_array_1d, np.ndarray) is True
    assert hasattr(ids_read, "val_array_1d") is True
    assert ids_read.val_array_1d.shape == (0,)
    with h5py.File(hdf5_file, "r") as f:
        assert tuple(f.keys()) == ('ArrayClass', 'metadata')
        assert f['ArrayClass'].get('val_array_1d') is None


