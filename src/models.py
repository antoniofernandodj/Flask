from . import db, app


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'

with app.app_context():
    db.create_all()
    user = User(username='admin', email='admin@admin')
    item = db.session.query(User).filter_by(username='admin').first()
    if not item:
        db.session.add(user)
        db.session.commit()