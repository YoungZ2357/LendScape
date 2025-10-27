from app import db
from datetime import datetime
import enum

class UserClass(enum.Enum):
    ACTIVE = 'active'
    DEACTIVATED = 'deactivated'
    BANNED = 'banned'

class UserStatus(enum.Enum):
    ACTIVE = 'active'
    DEACTIVATED = 'deactivated'
    BANNED = 'banned'

class StatusType(enum.Enum):
    PENDING = 'pending'
    COMPLETE = 'complete'

user_item_association = db.Table('UserItem',
    db.Column('userId', db.Integer, db.ForeignKey('User.userId'), primary_key=True),
    db.Column('itemId', db.Integer, db.ForeignKey('Item.itemId'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {"extend_existing": True}
    userId = db.Column('userId', db.Integer, primary_key=True, autoincrement=True)
    firstName = db.Column('firstName', db.String(20), nullable=False)
    lastName = db.Column('lastName', db.String(20), nullable=False)
    email = db.Column('email', db.String(120), nullable=False, unique=True)
    locationId = db.Column('locationId', db.Integer, db.ForeignKey('Location.locationId'))
    phoneNumber = db.Column('phoneNumber', db.Integer)
    class_ = db.Column('class', db.Enum(UserClass), name='user_class')
    pwd = db.Column('pwd', db.String(255))
    status = db.Column('status', db.Enum(UserStatus), name='user_status')

    location = db.relationship('Location', backref='users')
    items = db.relationship('Item', backref='owner', foreign_keys='Item.userId')
    reviews = db.relationship('Review', backref='reviewer', foreign_keys='Review.userId')
    renter_orders = db.relationship('Order', backref='renter', foreign_keys='Order.renterId')
    borrower_orders = db.relationship('Order', backref='borrower', foreign_keys='Order.borrowerId')

    associated_items = db.relationship('Item', secondary=user_item_association, backref='associated_users')

    def to_dict(self):
        return {
            'userId': self.userId,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'locationId': self.locationId,
            'phoneNumber': self.phoneNumber,
            'class': self.class_.value if self.class_ else None,
            'status': self.status.value if self.status else None
        }


class Location(db.Model):
    __tablename__ = 'Location'
    __table_args__ = {'extend_existing': True}

    locationId = db.Column('locationId', db.Integer, primary_key=True, autoincrement=True)
    address = db.Column('address', db.Text)
    city = db.Column('city', db.String(100))
    state = db.Column('state', db.String(100))
    country = db.Column('country', db.String(100))
    postcode = db.Column('postcode', db.String(20))
    is_default = db.Column('is_default', db.Boolean, default=False)

    def to_dict(self):
        return {
            'locationId': self.locationId,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'postcode': self.postcode,
            'is_default': self.is_default
        }


class Item(db.Model):
    __tablename__ = 'Item'
    __table_args__ = {'extend_existing': True}

    itemId = db.Column('itemId', db.Integer, primary_key=True, autoincrement=True)
    itemName = db.Column('itemName', db.String(255))
    userId = db.Column('userId', db.Integer, db.ForeignKey('User.userId'))
    description = db.Column('description', db.Text)
    price = db.Column('price', db.DECIMAL(10, 2))
    image_url = db.Column('image_url', db.Text)
    is_available = db.Column('is_available', db.Boolean)

    def to_dict(self):
        return {
            'itemId': self.itemId,
            'itemName': self.itemName,
            'userId': self.userId,
            'description': self.description,
            'price': float(self.price) if self.price else None,
            'image_url': self.image_url,
            'is_available': self.is_available
        }


class Order(db.Model):
    __tablename__ = 'Order'
    __table_args__ = {'extend_existing': True}

    orderId = db.Column('orderId', db.Integer, primary_key=True, autoincrement=True)
    renterId = db.Column('renterId', db.Integer, db.ForeignKey('User.userId'))
    borrowerId = db.Column('borrowerId', db.Integer, db.ForeignKey('User.userId'))
    reviewId = db.Column('reviewId', db.Integer, db.ForeignKey('Review.reviewId'))
    status = db.Column('status', db.Enum(StatusType), name='status_type')

    review = db.relationship('Review', backref='order', foreign_keys=[reviewId])

    def to_dict(self):
        return {
            'orderId': self.orderId,
            'renterId': self.renterId,
            'borrowerId': self.borrowerId,
            'reviewId': self.reviewId,
            'status': self.status.value if self.status else None
        }


class Review(db.Model):
    __tablename__ = 'Review'
    __table_args__ = {'extend_existing': True}

    reviewId = db.Column('reviewId', db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column('userId', db.Integer, db.ForeignKey('User.userId'))
    itemId = db.Column('itemId', db.Integer, db.ForeignKey('Item.itemId'))
    orderId = db.Column('orderId', db.Integer, db.ForeignKey('Order.orderId'))
    content = db.Column('content', db.Text)
    rating = db.Column('rating', db.DECIMAL(3, 2))

    def to_dict(self):
        return {
            'reviewId': self.reviewId,
            'userId': self.userId,
            'itemId': self.itemId,
            'orderId': self.orderId,
            'content': self.content,
            'rating': float(self.rating) if self.rating else None
        }