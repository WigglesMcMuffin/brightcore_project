from flask.ext.testing import TestCase
from flask import url_for

from flask_app import create_app, db

class ViewsTest(TestCase):
    
    render_templates = False
    
    def create_app(self):
        return create_app('testing', debug=True, testing=True)
        
    def setUp(self):
        from flask_app import models
        db.create_all()
        db.session.add(models.Client('test_client'))
        db.session.add(models.Product('test_product'))
        db.session.commit()
        self.app = self.create_app()
        self.client = self.app.test_client()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def test_homepage(self):
        """ Test just to prove the main page template is working """
        self.client.get(url_for('main.main_page'))
        self.assert_template_used('main.jade')
