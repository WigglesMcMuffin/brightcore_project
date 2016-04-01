from flask.ext.testing import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import date

from flask_app import create_app, db
from flask_app import models


class ModelsTest(TestCase):

    render_templates = False

    def create_app(self):
        return create_app('testing')

    def setUp(self):
        import flask_app.models
        db.create_all()
        db.session.add(models.Client('test_client'))
        db.session.add(models.Product('test_product'))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_feature_priority_count(self):
        """ Test that if no priority is given, next available is assigned """
        test_feature = models.Feature('test_priority_count', '', 1, None, date.today(), '', 1)
        db.session.add(test_feature)
        db.session.commit()
        self.assertTrue(test_feature in db.session)
        self.assertEqual(db.session.query(models.Feature).first().client_priority, 1)

    def test_feature_priority_greater_than_zero(self):
        """ Test that if a number less than 1 is given, the next available is given """
        test_feature = models.Feature('test_priority_greater_than_zero', '', 1, -1, date.today(), '', 1)
        db.session.add(test_feature)
        db.session.commit()
        self.assertTrue(test_feature in db.session)
        self.assertEqual(db.session.query(models.Feature).all()[0].client_priority, 1)

    def test_feature_priority_shrink(self):
        """ Test that when a feature is removed, the lower priority features move up a priority """
        db.session.add(models.Feature('test_priority_shrink_1', '', 1, None, date.today(), '', 1))
        db.session.add(models.Feature('test_priority_shrink_2', '', 1, None, date.today(), '', 1))
        db.session.add(models.Feature('test_priority_shrink_3', '', 1, None, date.today(), '', 1))
        db.session.commit()
        self.assertEqual(len(db.session.query(models.Feature).all()), 3)
        db.session.delete(db.session.query(models.Feature).all()[1])
        db.session.commit()
        self.assertEqual([x.client_priority for x in db.session.query(models.Feature).all()], [1, 2])

    def test_feature_priority_too_high(self):
        """ Test that when a feature is given a number greater than the priority queue, the next available is given """
        db.session.add(models.Feature('test_priority_too_high', '', 1, 7, date.today(), '', 1))
        db.session.commit()
        self.assertEqual(len(db.session.query(models.Feature).all()), 1)
        self.assertEqual(db.session.query(models.Feature).first().client_priority, 1)

    def test_feature_priority_shift(self):
        """ Test that when a new feature requests high priority, all other features shift to acoomodate """
        db.session.add(models.Feature('test_priority_shift_1', '', 1, 1, date.today(), '', 1))
        db.session.commit()
        db.session.add(models.Feature('test_priority_shift_2', '', 1, 1, date.today(), '', 1))
        db.session.commit()
        self.assertEqual(db.session.query(models.Feature).first().client_priority, 2)
        self.assertEqual(db.session.query(models.Feature).all()[-1].client_priority, 1)
