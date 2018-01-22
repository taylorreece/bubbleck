#!/usr/bin/env python3

import glob
import os
import sys
sys.path.append('.')
sys.path.append('..')
import psycopg2
from bck import database

db = database.BckDB()

try:
	schema_version = db.get_schema_version()
except psycopg2.ProgrammingError:
	schema_version = -1

def apply_schema():
	try:
		schema_version = db.get_schema_version()
	except psycopg2.ProgrammingError:
		schema_version = -1
	next_file = 's{0}.sql'.format(str(int(schema_version) + 1))
	if os.path.isfile(next_file):
		print("Applying {0}...".format(next_file))
		f = open(next_file, 'r')
		db.run_file(f)
		apply_schema()

apply_schema()
