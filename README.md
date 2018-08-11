# PyRocks

An out-of-box Python binding for RocksDB using ctypes.
 
## Why PyRocks?

There is already a Python binding for RocksDB called [python-rocksdb][1] which wraps C++ API from RocksDB code using Cython. But the problem is we have to build the library before we start and sometimes the build process will fail and you can do nothing to fix it.

PyRocks leverages the C API which provided by RocksDB which is more mature and stable. And it's pure python code and you can start use it with no extra work.

## Try PyRocks

PyRocks is still under development. You can come up with iussus or make pull requests to contribute the project.

Please make sure you have the shared lib of rocksdb before you start. The easy way is to `sudo apt install librocksdb-dev` (in Ubuntu). And the other way is to `make shared_lib` using rocksdb source code.

You can run `py.test` to go through all test cases. Or do some experiments with at your will.

[1]: https://github.com/twmht/python-rocksdb

