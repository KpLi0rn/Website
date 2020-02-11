from datetime import datetime,timedelta
import unittest
from app.models import User,Post
from app import app,db

class UserModelTest(unittest.TestCase):
    def setUp(self):
        app.config['SQKALCHEMY_DATABASE_URL']="sqlite://"
        db.create_all()
    # 删除
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hash(self): # 进行用户密码的测试
        u = User(username="test")
        u.set_password('abc123456')
        self.assertTrue(u.check_password('abc123456'))
        self.assertFalse(u.check_password('123456abc'))

    def test_follow(self):
        u1 = User(username="aaa",email="111111111@qq.com")
        u2 = User(username="bbb",email="222222222@qq.com")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(),[])
        self.assertEqual(u2.followed.all(),[])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(),1)
        self.assertEqual(u1.followed.first().username,"bbb")
        self.assertEqual(u2.followers.count(),1)    # 这里的followers 有点不懂 需要回顾一下
        self.assertEqual(u2.followers.first().username,"aaa")

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(),0)
        self.assertEqual(u2.followers.count(),0)

    def test_follow_posts(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1,u2,u3,u4])

        now = datetime.utcnow()
        p1 = Post(content="post from john", author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(content="post from susan", author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(content="post from mary", author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(content="post from david", author=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1,p2,p3,p4])
        db.session.commit()

        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()

        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1,[p2,p4,p1])
        self.assertEqual(f2,[p2,p3])
        self.assertEqual(f3,[p3,p4])
        self.assertEqual(f4,[p4])

if __name__ == '__main__':
    unittest.main(verbosity=2)