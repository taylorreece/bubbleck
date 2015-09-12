import user
import course

# Create some users
u1 = user.User(email='test1@test.com',name='First1 Last',teachername='Mr. First1',password_plaintext='1234')
u2 = user.User(email='test2@test.com',name='First2 Last',teachername='Mr. First2',password_plaintext='1234')
u3 = user.User(email='test3@test.com',name='First3 Last',teachername='Mr. First3',password_plaintext='1234')
u4 = user.User(email='test4@test.com',name='First4 Last',teachername='Mr. First4',password_plaintext='1234')
u1.save()
u2.save()
u3.save()
u4.save()

# Create some courses
c1 = course.Course(name='Math 1')
c2 = course.Course(name='Math 2')
c3 = course.Course(name='Math 3')
c4 = course.Course(name='Math 4')
c1.save()
c2.save()
c3.save()
c4.save()

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

