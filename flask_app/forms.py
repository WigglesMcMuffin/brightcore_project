from flask.ext.wtf import Form
from wtforms import DateField, IntegerField, SelectField, TextField, TextAreaField
from wtforms.validators import Required, Optional

class FeatureRequestForm(Form):
	title = TextField('Title', validators=[Required()])
	description = TextAreaField('Email', validators=[Optional()])
	client_id = SelectField('Client', coerce=int, validators=[Required()])
	client_priority = IntegerField('Client Priority', validators=[Optional()])
	target_date = DateField('Target Date', format='%m-%d-%Y', validators=[Required()])
	ticket_url = TextField('Ticket URL', validators=[Required()])
	product_area_id = SelectField('Product Area', coerce=int, validators=[Required()])
	
class ClientForm(Form):
	name = TextField('Name', validators=[Required()])
	
class ProductAreaForm(Form):
	name = TextField('Product Area', validators=[Required()])