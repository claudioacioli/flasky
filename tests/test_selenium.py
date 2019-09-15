import re
import threading
import time
import unittest
from selenium import webdriver
from app import create_app, db, fake
from app.models import User, Role

class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # inicia o chrome
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        try:
            cls.client = webdriver.Chrome(chrome_options=options)
        except:
            pass

        # Ignora testes caso navegador não possa ser inicalizado
        if cls.client:
            # cria app
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel('ERROR')

            db.create_all()
            Role.insert_roles()
            fake.users(10)
            fake.posts(10)

            # Adiciona um usuario adm
            admin_role = Role.query.filter_by(name='Administrator').first()
            admin = User(
                email='acioli@example.com',
                username='acioli',
                password='cat',
                role=admin_role,
                confirmed=True
            )
            db.session.add(admin)
            db.session.commit()

            #Inicia servidor flask thread segundo plano
            cls.server_thread = threading.Thread(
                target=cls.app.run, kwargs={
                    'debug': False,
                    'use_reloader': False,
                    'use_debugger': False
                }
            )

            cls.server_thread.start()
            time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.quit()
            cls.server_thread.join()

            db.drop_all()
            db.session.remove()

            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web Browser não disponível')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        # navega para pagina inicial
        self.client.get('http://localhost:5000')
        self.assertTrue(re.search('Hello,\s+Stranger!', self.client.page_source))

        self.client.find_element_by_link_text('Acessar').click()
        self.assertIn('<h1>Login</h1>', self.client.page_source)

        self.client.find_element_by_name('email').send_keys('acioli@example.com')
        self.client.find_element_by_name('password').send_keys('cat')
        self.client.find_element_by_name('submit').click()
        self.assertTrue(re.search('Hello,\s+acioli!', self.client.page_source))


        self.client.find_element_by_link_text('Profile').click()
        self.assertIn('<h1>acioli</h1>', self.client.page_source)