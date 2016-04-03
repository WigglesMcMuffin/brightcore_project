from flask_app import create_app, db
from flask_app.models import Client, Product

def populate_tables(db_session):
    if len(Client.query.all()) == 0:
        cs = [Client('Client%s' % x) for x in ['A', 'B', 'C']]

        for c in cs:
            db_session.session.add(c)

        p = Product('Policies'); db_session.session.add(p)
        p = Product('Billing'); db_session.session.add(p)
        p = Product('Claims'); db_session.session.add(p)
        p = Product('Reports'); db_session.session.add(p)

        db_session.session.commit()

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        populate_tables(db)
