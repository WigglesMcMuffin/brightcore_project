from itertools import count, groupby
from sqlalchemy import event
from flask.ext.sqlalchemy import SignallingSession

from flask_app import db


class Feature(db.Model):
    __tablename__ = 'features'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.Text)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client = db.relationship("Client", foreign_keys=[client_id])
    client_priority = db.Column(db.Integer)
    target_date = db.Column(db.Date)
    ticket_url = db.Column(db.String(300))
    product_area_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_area = db.relationship("Product", foreign_keys=[product_area_id])

    def __init__(self, title=None, description=None, client_id=None, client_priority=None, target_date=None, ticket_url=None, product_area_id=None):
        # typically check for values here, but as SQL has a conecpt of nullable fields
        # I tend to leave that validation to that layer, to keep responsibilities in line and code clean
        self.title = title
        self.description = description
        self.client_id = client_id
        self.client_priority = client_priority
        self.target_date = target_date
        self.ticket_url = ticket_url
        self.product_area_id = product_area_id

    def __repr__(self):
        return '<feature %r - from %r>' % (self.title, self.client.name)


@event.listens_for(SignallingSession, 'before_flush')
def check_client_priority(session, flush_context, instances):
    dirty = session.dirty  # pull down a "copy" because changes are reflected "on the fly"
    check_removed_features(session.deleted)
    check_dirty_features(dirty)
    check_new_features(session.new)


def check_new_features(added_objects):
    features_by_client = {c_id: sorted(list(f), key=lambda x: x.client_priority or 0) for c_id, f in groupby(sorted([x for x in added_objects if type(x).__name__ == 'Feature'], key=lambda x: x.client_id), lambda y: y.client_id)}
    for features in features_by_client.values():
        new_tickets = count(1)
        for feature in features:
            priorities = Feature.query.filter(Feature.client_id == feature.client_id)  # To save lookups, this value is saved as it's called repeatedly
            if feature.client_priority is None or feature.client_priority < 1:
                feature.client_priority = len(priorities.all()) + next(new_tickets)
            else:
                for f in priorities.filter(Feature.client_priority >= feature.client_priority).all():
                    f.client_priority += 1
            feature.client_priority = min(len(priorities.all()) + 1, feature.client_priority)  # To keep the priorities list only consequetive integers


def check_removed_features(removed_objects):
    features_by_client = {c_id: sorted(list(f), key=lambda x: x.client_priority, reverse=True) for c_id, f in groupby(sorted([x for x in removed_objects if type(x).__name__ == 'Feature'], key=lambda x: x.client_id), lambda y: y.client_id)}
    for features in features_by_client.values():
        for feature in features:
            priorities = Feature.query.filter(Feature.client_id == feature.client_id)  # To save lookups, this value is saved as it's called repeatedly
            for f in priorities.filter(Feature.client_priority >= feature.client_priority).all():
                f.client_priority -= 1


def check_dirty_features(dirty_objects):
    pass  # As it stands I don't think this will be required


class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)  # Almost certainly a uuid in a production environment
    name = db.Column(db.String(50), unique=True)
    # Other pertainent info here:
    # Probably things like contact info

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Client %s>' % (self.name)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name=None):
        self.name = name
