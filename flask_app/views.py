from flask import render_template, redirect, flash, url_for
from itertools import groupby

from flask_app import app
from flask_app.database import db_session
from flask_app.forms import FeatureRequestForm, ClientForm, ProductAreaForm
from flask_app.models import Feature, Client, Product

@app.route('/')
def main_page():
	request_form = FeatureRequestForm()
	request_form.client_id.choices = [(c.id, c.name) for c in Client.query.all()]
	request_form.product_area_id.choices = [(p.id, p.name) for p in Product.query.all()]
	client_form = ClientForm()
	product_form = ProductAreaForm()
	return render_template('main.jade', pageTitle='Home Page', request_form=request_form, client_form=client_form, product_form=product_form)
	
@app.route('/features/')
def features():
	def keyfunc(x):
		return x.client.name
	features_by_client = groupby(sorted(Feature.query.all(), key=keyfunc), keyfunc)
	features_by_client = {c: sorted(list(f), key=lambda x: x.client_priority) for c, f in features_by_client}
	return render_template('features.jade', pageTitle='Current Features', features_by_client=features_by_client)
	
@app.route('/features/<feature_id>')
def feature(feature_id):
	feature = Feature.query.get(feature_id)
	return render_template('feature.jade', pageTitle='Home Page', feature=feature)

	
#Normally these might be sequestered away in their own MethodViews, and probably in a blueprint
@app.route('/feature', methods=['POST'])
def new_feature():
	form = FeatureRequestForm()
	form.client_id.choices = [(c.id, c.name) for c in Client.query.all()]
	form.product_area_id.choices = [(p.id, p.name) for p in Product.query.all()]
	if form.validate_on_submit():
		title = form.title.data
		description = form.description.data
		client_id = form.client_id.data
		client_priority = form.client_priority.data
		print(client_priority)
		target_date = form.target_date.data
		ticket_url = form.ticket_url.data
		product_area_id = form.product_area_id.data
		#Feature.query.filter('client_priority' = client_priority).all()
		f = Feature(title=title, description=description, client_id=client_id, client_priority=client_priority, target_date=target_date, ticket_url=ticket_url, product_area_id=product_area_id)
		db_session.add(f)
		db_session.commit()
		flash('Feature added', 'list-group-item-success')
	else:
		flash('Feature addition failed', 'list-group-item-danger')
	return redirect(url_for('main_page'))
		
@app.route('/client', methods=['POST'])
def new_client():
	form = ClientForm()
	if form.validate_on_submit():
		name = form.name.data
		c = Client(name=name)
		db_session.add(c)
		db_session.commit()
		flash('Client Added', 'list-group-item-info')
	else:
		flash('Client addition failed', 'list-group-item-warning')
	return redirect(url_for('main_page'))

@app.route('/product', methods=['POST'])
def new_product_area():
	form = ProductAreaForm()
	if form.validate_on_submit():
		name = form.name.data
		p = Product(name=name)
		db_session.add(p)
		db_session.commit()
		flash('Product Area added', 'list-group-item-info')
	else:
		flash('Product Area addition failed', 'list-group-item-warning')
	return redirect(url_for('main_page'))