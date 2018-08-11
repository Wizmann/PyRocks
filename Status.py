import ctypes
from librocksdb import *

class Status(object):
    def __init__(self):
        self.ptr_internal = ctypes.POINTER(ctypes.c_ubyte)()

    def to_rocksdb_internal(self):
        return self.ptr_internal

    def OK(self):
        msg = ctypes.cast(self.ptr_internal, ctypes.c_char_p)
        return not msg.value

    def GetMessage(self):
        msg = ctypes.cast(self.ptr_internal, ctypes.c_char_p)
        if not msg.value:
            return "OK"
        return msg.value

    def __str__(self):
        return self.GetMessage()
