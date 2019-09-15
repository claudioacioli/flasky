import json
from base64 import b64encode
import unittest
from app import create_app, db
from app.models import User, Role


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        # use_cookies é setado para false pois API's Rest não mantém estado.
        self.client = self.app.test_client(use_cookies=False)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            'Authorization':
                'Basic ' + b64encode((username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_no_auth(self):
        response = self.client.get('/api/v1/posts/', content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_posts(self):
        # adiciona um usuario
        r = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(r)
        u = User(email='john@example.com', password='cat', confirmed=True, role=r)
        db.session.add(u)
        db.session.commit()

        # escreve postagem
        response = self.client.post(
            '/api/v1/posts/',
            headers=self.get_api_headers('john@example.com','cat'),
            data=json.dumps({'body': 'Criando com os *testes*'})
        )
        self.assertEqual(response.status_code, 201)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)

        # Obtem postagem
        response = self.client.get(url, headers=self.get_api_headers('john@example.com','cat'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual('http://localhost' + json_response['url'], url)
        self.assertEqual(json_response['body'], 'Criando com os *testes*')
        self.assertEqual(json_response['body_html'], '<p>Criando com os <em>testes</em></p>')
