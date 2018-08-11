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
        db, status = DB.Open(db_options, self.db_dir)
        self.assertTrue(status.OK())

        write_options = WriteOptions()
        status = db.Put(write_options, "foo", "bar")
        self.assertTrue(status.OK())

        read_options = ReadOptions()
        value, status = db.Get(read_options, "foo")
        self.assertTrue(status.OK())
        self.assertEqual("bar", value)

