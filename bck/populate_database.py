#!/usr/bin/python3

if input("Do you understand that this script will clear all data tables and run a series of unit tests? (y/N) ").lower() != 'y':
	exit()

import sys
import bckconfig
import hashlib
from bck import course, database, exam, bckconfig, section, studentexam, user
db = database.BckDB()

# Clear data tables
db.queryNoResults('DELETE FROM sessions')
db.queryNoResults('DELETE FROM studentexams')
db.queryNoResults('DELETE FROM sections')
db.queryNoResults('DELETE FROM examshares')
db.queryNoResults('DELETE FROM exams')
db.queryNoResults('DELETE FROM courses_users')
db.queryNoResults('DELETE FROM courses')
db.queryNoResults('DELETE FROM users')

# Create some users
u1 = user.User(email='test1@test.com',name='First1 Last',teachername='Mr. First1',password_plaintext='1234', is_admin=True)
u2 = user.User(email='test2@test.com',name='First2 Last',teachername='Mr. First2',password_plaintext='1234')
u3 = user.User(email='test3@test.com',name='First3 Last',teachername='Mr. First3',password_plaintext='1234')
u4 = user.User(email='test4@test.com',name='First4 Last',teachername='Mr. First4',password_plaintext='1234')
u1.save()
u2.save()
u3.save()
u4.save()
u4.save() # Yes, twice: should run an update the second time.
assert hashlib.md5(('1234' + bckconfig.password_salt).encode('utf-8')).hexdigest() == u1.password
assert user.getUserByID(u1.usersid).teachername == 'Mr. First1'

# Create some courses
c1 = course.Course(name='Math 1')
c2 = course.Course(name='Math 2')
c3 = course.Course(name='Math 3')
c4 = course.Course(name='Math 4')
c1.save()
c2.save()
c3.save()
c4.save()
c4.save() # Yes, twice; should run an update the second time.
assert c1.coursesid
assert course.getCourseByID(c1.coursesid).name == 'Math 1'

# Tie users to courses:
c1.addOrUpdateRole(u1.usersid, 'own')
c1.addOrUpdateRole(u2.usersid, 'view')
c1.addOrUpdateRole(u3.usersid, 'edit')
c2.addOrUpdateRole(u1.usersid, 'own')
c2.addOrUpdateRole(u3.usersid, 'edit')
c3.addOrUpdateRole(u1.usersid, 'own')
c3.addOrUpdateRole(u1.usersid, 'edit')
c3.addOrUpdateRole(u1.usersid, 'own')
c4.addOrUpdateRole(u2.usersid, 'own')
assert c4.getRole(u2.usersid) == 'own'

# Add in some exams
e1 = exam.Exam(name='Exam 1', coursesid=c1.coursesid, layout='DDDD', show_coursename=True, show_directions=True, show_points=False, show_teachername=True)
e2 = exam.Exam(name='Exam 2', coursesid=c1.coursesid, layout='CCCC', show_coursename=True, show_directions=True, show_points=False, show_teachername=True)
e3 = exam.Exam(name='Exam 3', coursesid=c2.coursesid, layout='EDDD', show_coursename=True, show_directions=True, show_points=False, show_teachername=True)
e1.save() 
e2.save()
e3.save()
e3.save() # yes, twice: should run an UPDATE the second time
assert exam.getExamByID(e1.examsid).name == 'Exam 1'

# Add a few shares
key1 = e1.addShareKey()
key2 = e1.addShareKey()
assert key1 != key2
assert key1 in e1.getShareKeys()
assert len(e1.getShareKeys()) == 2
e1.deactivateShareKey(key1)
assert key1 not in e1.getShareKeys()
assert key1 in e1.getDeactivatedKeys()
assert key2 in e1.getShareKeys()

# Add a few sections
s1 = section.Section(name='Section 1', coursesid=c1.coursesid)
s2 = section.Section(name='Section 2', coursesid=c1.coursesid)
s3 = section.Section(name='Section 3', coursesid=c2.coursesid)
s1.save()
s2.save()
s3.save()
s3.save() # yes, twice: should run an UPDATE the second time.
assert len(c1.getSections()) == 2
assert c2.getSections()[0].name == 'Section 3'

# Add a few student exams
se1 = studentexam.StudentExam(examsid=e1.examsid, sectionsid=s1.sectionsid, answers='ABCD')
se2 = studentexam.StudentExam(examsid=e1.examsid, sectionsid=s1.sectionsid, answers='BBBB')
se3 = studentexam.StudentExam(examsid=e1.examsid, sectionsid=s2.sectionsid, answers='CCCC')
se4 = studentexam.StudentExam(examsid=e1.examsid, sectionsid=s2.sectionsid, answers='DDDD')
se1.save()
se2.save()
se3.save()
se4.save()
se4.save()
assert len(e1.getStudentExams()) == 4
assert e1.getStudentExams()[0].answers == 'ABCD'
assert e1.getStudentExams()[0].examsid == e1.examsid
