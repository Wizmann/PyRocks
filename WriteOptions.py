#coding=utf-8

import ctypes
from librocksdb import *

rocksdb_writeoptions_create = librocksdb.rocksdb_writeoptions_create
rocksdb_writeoptions_destroy = librocksdb.rocksdb_writeoptions_destroy

class WriteOptions(object):
    def __init__(self):
        self.writeoptions_internal = rocksdb_writeoptions_create()

    def __del__(self):
        rocksdb_writeoptions_destroy(self.writeoptions_internal)

    def to_rocksdb_internal(self):
        return self.writeoptions_internal
