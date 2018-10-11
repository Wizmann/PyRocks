#coding=utf-8

import os
import shutil
import unittest
import tempfile

from DB import DB
from DBOptions import DBOptions
from WriteOptions import WriteOptions
from ReadOptions import ReadOptions

class TestDB(unittest.TestCase):
    def setUp(self):
        self.db_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.db_dir, ignore_errors=True)

    def test_db_put_get(self):
        db_options = DBOptions()
        db_options.create_if_missing = True
        db, status = DB.Open(db_options, self.db_dir.encode())
        self.assertTrue(status.OK())

        write_options = WriteOptions()
        status = db.Put(write_options, b"foo", b"bar")
        self.assertTrue(status.OK())

        read_options = ReadOptions()
        value, status = db.Get(read_options, b"foo")
        self.assertTrue(status.OK())
        self.assertEqual(b"bar", value)

    def test_tiered_db(self):
        db_options = DBOptions()
        db_options.create_if_missing = True
        db_options.add_db_path(os.path.join(tempfile.mkdtemp(), "1"), 1024)
        db_options.add_db_path(os.path.join(tempfile.mkdtemp(), "2"), 1024)
        db, status = DB.Open(db_options, self.db_dir.encode())

        self.assertTrue(status.OK())

        write_options = WriteOptions()
        status = db.Put(write_options, b"foo1", b"bar")
        self.assertTrue(status.OK())
        status = db.Put(write_options, b"foo2", b"bar" * 1024)
        self.assertTrue(status.OK())

        read_options = ReadOptions()
        value, status = db.Get(read_options, b"foo1")
        self.assertTrue(status.OK())
        self.assertEqual(b"bar", value)

        value, status = db.Get(read_options, b"foo3")
        self.assertTrue(status.OK())
        self.assertEqual(None, value)
