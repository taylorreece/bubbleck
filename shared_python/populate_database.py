#!/usr/bin/python

if raw_input("Do you understand that this script will clear all data tables and run a series of unit tests? (y/N) ").lower() != 'y':
	exit()

import sys
sys.path.insert(1,"/var/www/myautota")
import mat_config
import hashlib
from mat import user
from mat import course
from mat import database
db = database.mat_db()

# Clear data tables
db.queryNoResults('DELETE FROM courses_users')
db.queryNoResults('DELETE FROM courses')
db.queryNoResults('DELETE FROM users')

# Create some users
u1 = user.User(email='test1@test.com',name='First1 Last',teachername='Mr. First1',password_plaintext='1234')
u2 = user.User(email='test2@test.com',name='First2 Last',teachername='Mr. First2',password_plaintext='1234')
u3 = user.User(email='test3@test.com',name='First3 Last',teachername='Mr. First3',password_plaintext='1234')
u4 = user.User(email='test4@test.com',name='First4 Last',teachername='Mr. First4',password_plaintext='1234')
u1.save()
u2.save()
u3.save()
u4.save()
assert hashlib.md5('1234' + mat_config.password_salt).hexdigest() == u1.password

# Create some courses
c1 = course.Course(name='Math 1')
c2 = course.Course(name='Math 2')
c3 = course.Course(name='Math 3')
c4 = course.Course(name='Math 4')
c1.save()
c2.save()
c3.save()
c4.save()
assert c1.coursesid

# Tie users to courses:
c1.addOrUpdateRole(u1.usersid, 'own')
c1.addOrUpdateRole(u2.usersid, 'view')
c1.addOrUpdateRole(u3.usersid, 'edit')
c2.addOrUpdateRole(u1.usersid, 'own')
c2.addOrUpdateRole(u3.usersid, 'edit')
c3.addOrUpdateRole(u1.usersid, 'own')
c3.addOrUpdateRole(u1.usersid, 'edit')
c3.addOrUpdateRole(u1.usersid, 'edit')
c4.addOrUpdateRole(u2.usersid, 'own')
assert c4.getRole(u2.usersid) == 'own'
