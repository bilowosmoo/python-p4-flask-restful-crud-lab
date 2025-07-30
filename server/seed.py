from app import app, db
from models import Plant

with app.app_context():
    Plant.query.delete()

    p1 = Plant(name="Aloe Vera", image="https://img.com/aloe.jpg", price=10.0)
    p2 = Plant(name="Basil", image="https://img.com/basil.jpg", price=5.0)

    db.session.add_all([p1, p2])
    db.session.commit()
