from os import path

from tinydb import Query, TinyDB

# Using TinyDB as database which saves data to db.json file in directory
basedir = path.abspath(path.dirname(__file__))
TinyDB.default_table_name = "posts"
db = TinyDB(path.join(basedir, "../db.json"))
