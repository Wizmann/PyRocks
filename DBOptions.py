#coding=utf-8
import ctypes
from librocksdb import *

rocksdb_options_create = librocksdb.rocksdb_options_create
rocksdb_options_destroy = librocksdb.rocksdb_options_destroy
rocksdb_options_set_create_if_missing = librocksdb.rocksdb_options_set_create_if_missing

class DBOptions(object):
    def __init__(self):
        self.db_options_internal = rocksdb_options_create()
        self._create_if_missing = False

    def to_rocksdb_internal(self):
        rocksdb_options_set_create_if_missing(
                self.db_options_internal, self._create_if_missing)
        return self.db_options_internal

    def get_create_if_missing(self, v):
        return self._create_if_missing

    def set_create_if_missing(self, v):
        assert isinstance(v, bool)
        self._create_if_missing = v

    create_if_missing = property(get_create_if_missing, set_create_if_missing)

    def __del__(self):
        rocksdb_options_destroy(self.db_options_internal)
