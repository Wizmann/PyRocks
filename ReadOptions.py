#coding=utf-8

import ctypes
from librocksdb import *

rocksdb_readoptions_create = librocksdb.rocksdb_readoptions_create
rocksdb_readoptions_destroy = librocksdb.rocksdb_readoptions_destroy

class ReadOptions(object):
    def __init__(self):
        self.readoptions_internal = rocksdb_readoptions_create()

    def __del__(self):
        rocksdb_readoptions_destroy(self.readoptions_internal)

    def to_rocksdb_internal(self):
        return self.readoptions_internal
