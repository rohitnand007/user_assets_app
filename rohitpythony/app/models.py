from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


from app import db, login_manager


class User(UserMixin, db.Model):
    """
    Create an User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    department = db.Column(db.String(256))
    position = db.Column(db.String(256))
    active = db.Column(db.Boolean, default=True)
    assets = db.relationship('Asset', backref='user_assets', lazy=True)
    tickets = db.relationship('Ticket', backref='user_tickets', lazy=True)
    inventory = db.relationship('Inventory', backref='user_inventory', lazy=True)


    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.name)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Location(db.Model):
    """
    Create a locations table
    """

    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    active = db.Column(db.Boolean, default=True)
    assets = db.relationship('Asset', backref='location_assets',
                                lazy='dynamic')
    inventory = db.relationship('Inventory',backref='location_inventory',
                                lazy='dynamic')

    def __repr__(self):
        return '<Location: {}>'.format(self.description)    


class Asset(db.Model):
    """
    Create a Asset table
    """

    __tablename__ = 'assets'

    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'),
        nullable=False)
    location = db.Column(db.Integer, db.ForeignKey('locations.id'),
        nullable=False)
    managed_by = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    assigned_to = db.Column(db.Integer)
    assigned_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    certified_by = db.Column(db.Integer)
    comments = db.Column(db.Text)

    def __repr__(self):
        return '<Asset: {}>'.format(self.id)


class Inventory(db.Model):
    """
    Create Inventory table
    """
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    inventory_type = db.Column(db.String(256))
    manufacturer = db.Column(db.String(256))
    model = db.Column(db.String(256))
    serial_number = db.Column(db.String(256))
    vendor = db.Column(db.String(256))
    cost = db.Column(db.Float())
    date_purchased = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    purchased_by = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    count = db.Column(db.Integer)
    location =  db.Column(db.Integer, db.ForeignKey('locations.id'),
        nullable=False)

    def __repr__(self):
        return '<Inventory: {}>'.format(self.inventory_type)

class TicketType(db.Model):
    """
    Create Ticket Types table
    """
    __tablename__ = "ticket_types"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256))
    active = db.Column(db.Boolean,default=True)
    tickets = db.relationship('Ticket', backref='ticket_types', lazy=True)

    def __repr__(self):
        return '<TicketType: {}>'.format(self.description)

class Ticket(db.Model):
    """
    Create Table tickets
    """
    __tablename__ = "tickets"
    id = db.Column(db.Integer, primary_key=True)
    ticket_type = db.Column(db.Integer, db.ForeignKey('ticket_types.id'),
        nullable=False)
    description = db.Column(db.Text)
    opened_by = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    opened_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow) 
    due_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    updated_by = db.Column(db.Integer)

    def __repr__(self):
        return '<Ticket: {}>'.format(self.description)  

                        













                        