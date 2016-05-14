import unittest
from werkzeug.exceptions import NotFound
from app import create_app, db
from app.models import User
from .test_client import TestClient


class TestAPI(unittest.TestCase):
    default_username = 'dave'
    default_password = 'cat'

    def setUp(self):
        self.app = create_app('testing')
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.drop_all()
        db.create_all()
        u = User(username=self.default_username)
        u.set_password(self.default_password)
        db.session.add(u)
        db.session.commit()
        self.client = TestClient(self.app, u.generate_auth_token(), '')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_get_disks(self):
        rv, json = self.client.get('/resources/v1/c13-1/disks')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['disk0'] == 'free')

        ## post
        #rv, json = self.client.post('/api/v1/customers/',
                                    #data={'name': 'john'})
        #self.assertTrue(rv.status_code == 201)
        #location = rv.headers['Location']
        #rv, json = self.client.get(location)
        #self.assertTrue(rv.status_code == 200)
        #self.assertTrue(json['name'] == 'john')
        #rv, json = self.client.get('/api/v1/customers/')
        #self.assertTrue(rv.status_code == 200)
        #self.assertTrue(json['customers'] == [location])

        ## put
        #rv, json = self.client.put(location, data={'name': 'John Smith'})
        #self.assertTrue(rv.status_code == 200)
        #rv, json = self.client.get(location)
        #self.assertTrue(rv.status_code == 200)
        #self.assertTrue(json['name'] == 'John Smith')
