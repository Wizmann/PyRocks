#coding=utf-8

import six
import ctypes
from librocksdb import *
from Status import Status
from DBOptions import DBOptions
from ReadOptions import ReadOptions
from WriteOptions import WriteOptions

rocksdb_open = librocksdb.rocksdb_open
rocksdb_put = librocksdb.rocksdb_put
rocksdb_get = librocksdb.rocksdb_get

class DB(object):
    @staticmethod
    def Open(db_options, dbname):
        assert isinstance(db_options, DBOptions)
        assert isinstance(dbname, six.binary_type)

        status = Status()
        dbptr = rocksdb_open(
                db_options.to_rocksdb_internal(), 
                dbname,
                ctypes.byref(status.to_rocksdb_internal()))
        if dbptr:
            return DB(dbptr), status
        else:
            return None, status

    def __init__(self, dbptr):
        self.dbptr_internal = dbptr

    def to_rocksdb_internal(self):
        return self.dbptr_internal

    def Put(self, write_options, key, value):
        assert isinstance(write_options, WriteOptions)
        assert isinstance(key, six.binary_type)
        assert isinstance(value, six.binary_type)

        status = Status()
        rocksdb_put(
                self.dbptr_internal,
                write_options.to_rocksdb_internal(),
                key, len(key),
                value, len(value),
                ctypes.byref(status.to_rocksdb_internal()))
        return status

    def Get(self, read_options, key):
        assert isinstance(read_options, ReadOptions)
        assert isinstance(key, six.binary_type)

        status = Status()
        vallen = ctypes.c_size_t()
        valptr = rocksdb_get(
                self.dbptr_internal,
                read_options.to_rocksdb_internal(),
                key, len(key),
                ctypes.byref(vallen),
                ctypes.byref(status.to_rocksdb_internal()))

        if not status.OK or not valptr:
            return None, status
        else:
            vt = ctypes.c_char * (vallen.value)
            res = ctypes.cast(valptr, ctypes.POINTER(vt))
            return res.contents.value, status
