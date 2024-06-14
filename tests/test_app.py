# tests/test_app.py
import unittest
from app import create_app, db
from app.db_models import User

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/Smart_Waste'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_creation(self):
        with self.app.app_context():
            user = User(username='testuser', role='household', email='test@example.com')
            db.session.add(user)
            db.session.commit()
            self.assertIsNotNone(User.query.filter_by(username='testuser').first())

if __name__ == '__main__':
    unittest.main()
