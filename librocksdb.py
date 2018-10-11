#coding=utf-8
import os
import ctypes

librocksdb = ctypes.cdll.LoadLibrary("./librocksdb.so.5.16.0")
