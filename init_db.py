from flask_app.database import init_db, db_session
from flask_app.models import Client, Product

init_db()

if len(Client.query.all()) == 0:
	cs = [Client('Client%s' % x) for x in ['A', 'B', 'C']]

	for c in cs:
		db_session.add(c)
	
	p = Product('Policies'); db_session.add(p)
	p = Product('Billing'); db_session.add(p)
	p = Product('Claims'); db_session.add(p)
	p = Product('Reports'); db_session.add(p)

	db_session.commit()