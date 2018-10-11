#coding=utf-8
import ctypes
from six.moves import range
from librocksdb import *

rocksdb_options_create = librocksdb.rocksdb_options_create
rocksdb_options_destroy = librocksdb.rocksdb_options_destroy
rocksdb_options_set_create_if_missing = librocksdb.rocksdb_options_set_create_if_missing
rocksdb_options_set_db_paths = librocksdb.rocksdb_options_set_db_paths

rocksdb_dbpath_create = librocksdb.rocksdb_dbpath_create
rocksdb_dbpath_destroy = librocksdb.rocksdb_dbpath_destroy


class DBPath(object):
    def __init__(self, path, target_size):
        self.path = path
        self.target_size = target_size
        self.db_path_internal = None

    def to_rocksdb_internal(self):
        self.db_path_internal = rocksdb_dbpath_create(self.path, self.target_size)
        return self.db_path_internal

    def __del__(self):
        if self.db_path_internal is not None:
            rocksdb_dbpath_destroy(self.db_path_internal)

class DBOptions(object):
    def __init__(self):
        self.db_options_internal = rocksdb_options_create()
        self._create_if_missing = False
        self._dbpaths = []

    def to_rocksdb_internal(self):
        rocksdb_options_set_create_if_missing(
                self.db_options_internal, self._create_if_missing)
        rocksdb_options_set_db_paths(
                self.db_options_internal,
                self.get_db_paths_pointer(),
                len(self._dbpaths))
        return self.db_options_internal

    def get_create_if_missing(self, v):
        return self._create_if_missing

    def set_create_if_missing(self, v):
        assert isinstance(v, bool)
        self._create_if_missing = v

    def add_db_path(self, path, target_size):
        self._dbpaths.append(DBPath(path, target_size))

    def get_db_paths_pointer(self):
        size = len(self._dbpaths)
        paths = (ctypes.c_char_p * size)()
        for i in range(size):
            paths[i] = (ctypes.c_char_p)(self._dbpaths[i].to_rocksdb_internal())
        return ctypes.cast(paths, ctypes.POINTER(ctypes.c_char_p))

    create_if_missing = property(get_create_if_missing, set_create_if_missing)

    def __del__(self):
        rocksdb_options_destroy(self.db_options_internal)
