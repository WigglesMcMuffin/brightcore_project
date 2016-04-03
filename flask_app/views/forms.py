from flask import Blueprint, redirect, flash, url_for, request, jsonify

from flask_app import db, csrf
from flask_app.forms import FeatureRequestForm, ClientForm, ProductAreaForm
from flask_app.models import Feature, Client, Product


form_endpoints = Blueprint('forms', __name__)

@form_endpoints.route('/feature', methods=['POST'])
def new_feature():
    form = FeatureRequestForm()
    form.client_id.choices = [(c.id, c.name) for c in Client.query.all()]
    form.product_area_id.choices = [(p.id, p.name) for p in Product.query.all()]
    if form.validate_on_submit():
        f = Feature()
        form.populate_obj(f)
        db.session.add(f)
        db.session.commit()
        flash('Feature added', 'list-group-item-success')
    else:
        flash('Feature addition failed', 'list-group-item-danger')
        for field, errors in form.errors.items():
            flash('%s: %s' %(field, ', '.join([str(x) for x in errors])), 'list-group-item-danger')
    return redirect(url_for('main.main_page'))


@form_endpoints.route('/client', methods=['POST'])
def new_client():
    form = ClientForm()
    if form.validate_on_submit():
        name = form.name.data
        c = Client(name=name)
        db.session.add(c)
        db.session.commit()
        flash('Client Added', 'list-group-item-info')
    else:
        flash('Client addition failed', 'list-group-item-warning')
    return redirect(url_for('main.main_page'))


@form_endpoints.route('/product', methods=['POST'])
def new_product_area():
    form = ProductAreaForm()
    if form.validate_on_submit():
        name = form.name.data
        p = Product(name=name)
        db.session.add(p)
        db.session.commit()
        flash('Product Area added', 'list-group-item-info')
    else:
        flash('Product Area addition failed', 'list-group-item-warning')
    return redirect(url_for('main.main_page'))

@form_endpoints.route('/priorities/<int:client_id>/', methods=['POST'])
def priority_change(client_id):
    # Normally these sorts of changes would be behind something like logins or other protections that would be checked
    json_objects = request.get_json()
    new_priorities = str(json_objects['priorities']).split('_')
    features = Feature.query.filter(Feature.client_id == client_id).order_by(Feature.client_priority).all()
    for feature, new_priority in zip(features, new_priorities):
        feature.client_priority = new_priority
        db.session.add(feature)
    db.session.commit()
    return jsonify(result='Ok'), 200
