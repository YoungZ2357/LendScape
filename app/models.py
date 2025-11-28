from app import db
from datetime import datetime
import enum
from sqlalchemy import Enum
class UserClass(enum.Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    ADMIN = 'admin'

class UserStatus(enum.Enum):
    ACTIVE = 'active'
    DEACTIVATED = 'deactivated'
    BANNED = 'banned'

class StatusType(enum.Enum):
    pending = 'pending'
    complete = 'complete'

class RequestStatus(enum.Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    CANCELLED = 'cancelled'
    EXPIRED = 'expired'


class User(db.Model):
    __tablename__ = 'User'
    __table_args__ = {"extend_existing": True, "schema": "lendscapev1"}

    userId = db.Column('userid', db.Integer, primary_key=True, autoincrement=True)
    firstName = db.Column('firstname', db.String(20), nullable=False)
    lastName = db.Column('lastname', db.String(20), nullable=False)
    email = db.Column('email', db.String(120), nullable=False, unique=True)
    locationId = db.Column('locationid', db.Integer, db.ForeignKey('lendscapev1.Location.locationid'))
    phoneNumber = db.Column('phonenumber', db.Integer)
    userClass = db.Column(
        Enum(UserClass, values_callable=lambda x: [e.value for e in x]),
        name='class'
    )

    auth_id = db.Column('auth_id', db.Integer)
    pwd = db.Column('pwd', db.String(255))
    status = db.Column(
        Enum(UserStatus, values_callable=lambda x: [e.value for e in x]),
        name='status'
    )

    def to_dict_admin(self):
        return {
            'userId': self.userId,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'locationId': self.locationId,
            'phoneNumber': self.phoneNumber,
            'userClass': self.userClass.value if self.userClass else None,
            'status': self.status.value if self.status else None
        }
    def to_dict(self):
        return {
            'userId': self.userId,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'locationId': self.locationId,
            'userClass': self.userClass.value if self.userClass else None,
            'status': self.status.value if self.status else None
        }


class Location(db.Model):
    __tablename__ = 'Location'
    __table_args__ = {"extend_existing": True, "schema": "lendscapev1"}

    locationId = db.Column('locationid', db.Integer, primary_key=True, autoincrement=True)
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
    __table_args__ = {"extend_existing": True, "schema": "lendscapev1"}

    itemId = db.Column('itemid', db.Integer, primary_key=True, autoincrement=True)
    itemName = db.Column('itemname', db.String(100), nullable=False)
    userId = db.Column('userid', db.Integer, db.ForeignKey('lendscapev1.User.userid'))
    description = db.Column('description', db.String(255))
    price = db.Column('price', db.Float)
    image_url = db.Column('image_url', db.String(255))
    is_available = db.Column('is_available', db.Boolean, default=True)

    def to_dict(self):
        return {
            'itemId': self.itemId,
            'itemName': self.itemName,
            'userId': self.userId,
            'description': self.description,
            'price': self.price,
            'image_url': self.image_url,
            'is_available': self.is_available
        }


class Order(db.Model):
    __tablename__ = 'Order'
    __table_args__ = {"extend_existing": True, "schema": "lendscapev1"}

    orderId = db.Column('orderid', db.Integer, primary_key=True, autoincrement=True)
    renterId = db.Column('renterid', db.Integer, db.ForeignKey('User.userid'))
    borrowerId = db.Column('borrowerid', db.Integer, db.ForeignKey('User.userid'))
    reviewId = db.Column('reviewid', db.Integer, db.ForeignKey('Review.reviewid'))
    itemId = db.Column('itemid', db.Integer, db.ForeignKey('Item.itemid'))
    status = db.Column(db.Enum(StatusType))

    # review = db.relationship('Review', backref='order', foreign_keys=[reviewId])

    def to_dict(self):
        return {
            'orderId': self.orderId,
            'renterId': self.renterId,
            'borrowerId': self.borrowerId,
            'reviewId': self.reviewId,
            'itemId': self.itemId,
            'status': self.status.value if self.status else None
        }


class Review(db.Model):
    __tablename__ = 'Review'
    __table_args__ = {"extend_existing": True, "schema": "lendscapev1"}

    reviewId = db.Column('reviewid', db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column('userid', db.Integer, db.ForeignKey('User.userId'))
    itemId = db.Column('itemid', db.Integer, db.ForeignKey('Item.itemId'))
    orderId = db.Column('orderid', db.Integer, db.ForeignKey('Order.orderId'))
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


class UserItem(db.Model):
    __tablename__ = 'UserItem'
    __table_args__ = {"extend_existing": True, "schema": "lendscapev1"}

    userid = db.Column(
        db.Integer,
        db.ForeignKey('lendscapev1.User.userid'),
        primary_key=True
    )
    itemid = db.Column(
        db.Integer,
        db.ForeignKey('lendscapev1.Item.itemid'),
        primary_key=True
    )

    def to_dict(self):
        return {
            'user_id': self.userid,
            'item_id': self.itemid,
        }



class Request(db.Model):
    __tablename__ = 'Request'
    __table_args__ = {"extend_existing": True, "schema": "lendscapev1"}
    requestId = db.Column('requestid', db.Integer, primary_key=True, autoincrement=True)
    requesterId = db.Column('requesterid', db.Integer, db.ForeignKey('lendscapev1.User.userid'), nullable=False)
    ownerId = db.Column('ownerid', db.Integer, db.ForeignKey('lendscapev1.User.userid'), nullable=False)
    itemId = db.Column('itemid', db.Integer, db.ForeignKey('lendscapev1.Item.itemid'), nullable=False)
    orderId = db.Column('orderid', db.Integer, db.ForeignKey('lendscapev1.Order.orderid'))
    startDate = db.Column('startdate', db.DateTime, nullable=False)
    endDate = db.Column('enddate', db.DateTime, nullable=False)
    message = db.Column('message', db.Text)
    status = db.Column(
        'status',
        Enum(RequestStatus, values_callable=lambda x: [e.value for e in x])
    )
    createdAt = db.Column('createdat', db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column('updatedat', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expiresAt = db.Column('expiresat', db.DateTime)
    rejectionReason = db.Column('rejectionreason', db.Text)

    def to_dict(self):
        return {
            'requestId': self.requestId,
            'requesterId': self.requesterId,
            'ownerId': self.ownerId,
            'itemId': self.itemId,
            'orderId': self.orderId,
            'startDate': self.startDate.isoformat() if self.startDate else None,
            'endDate': self.endDate.isoformat() if self.endDate else None,
            'message': self.message,
            'status': self.status.value if self.status else None,
            'createdAt': self.createdAt.isoformat() if self.createdAt else None,
            'updatedAt': self.updatedAt.isoformat() if self.updatedAt else None,
            'expiresAt': self.expiresAt.isoformat() if self.expiresAt else None,
            'reason': self.rejectionReason
        }