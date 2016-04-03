from itertools import groupby
from flask import Blueprint, render_template

from flask_app.forms import FeatureRequestForm, ClientForm, ProductAreaForm
from flask_app.models import Feature, Client, Product

main_site = Blueprint('main', __name__)


@main_site.route('/')
def main_page():
    request_form = FeatureRequestForm()
    request_form.client_id.choices = [(c.id, c.name) for c in Client.query.all()]
    request_form.product_area_id.choices = [(p.id, p.name) for p in Product.query.all()]
    client_form = ClientForm()
    product_form = ProductAreaForm()
    return render_template('main.jade',
                           pageTitle='Home Page',
                           request_form=request_form,
                           client_form=client_form,
                           product_form=product_form)


@main_site.route('/features/')
def features():
    def keyfunc(x):
        return x.client.name
    features_by_client = groupby(sorted(Feature.query.all(), key=keyfunc), keyfunc)
    features_by_client = {c: sorted(list(f), key=lambda x: x.client_priority) for c, f in features_by_client}
    return render_template('features.jade',
                           pageTitle='Current Features',
                           features_by_client=features_by_client)


@main_site.route('/features/<feature_id>/')
def feature(feature_id):
    selected_feature = Feature.query.get(feature_id)
    return render_template('feature.jade',
                           pageTitle='Feature - %s' % (selected_feature.title),
                           feature=selected_feature)


@main_site.route('/features/<client_id>/sort/')
def sort_features(client_id):
    selected_features = sorted(Feature.query.filter(Feature.client_id == client_id).all(), key=lambda x: x.client_priority)
    return render_template('sorted.jade',
                           pageTitle='Sort Featurse',
                           features=selected_features)
