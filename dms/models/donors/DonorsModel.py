from dms.app import db
from datetime import datetime as dt
from ..donations.DonationsModel import DonationsModel


class DonorsModel(db.Model):
    __tablename__ = "donors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email_address = db.Column(db.String(50), unique=True, nullable=False, )
    gender = db.Column(db.String(6), unique=False, nullable=False, )
    date_of_birth = db.Column(db.Date, unique=False, nullable=False)
    date_of_anniversary = db.Column(db.Date, unique=False, nullable=True)
    pan = db.Column(db.String(10), unique=True, nullable=False)
    uid = db.Column(db.Integer, unique=True, nullable=False)
    country_code = db.Column(db.Integer, unique=False, nullable=False)
    phone_number = db.Column(db.String(12), unique=True, nullable=False)
    reference_id = db.Column(
        db.Integer, db.ForeignKey("references.id"), unique=False, nullable=False
    )
    referrer_name = db.Column(db.String(20), unique=False, nullable=True)
    other_reference = db.Column(db.String(20), unique=False, nullable=True)
    address_line_1 = db.Column(db.String(50), nullable=False, unique=False)
    address_line_2 = db.Column(db.String(50), nullable=False, unique=False)
    city = db.Column(db.String(30), nullable=False, unique=False)
    state = db.Column(db.String(20), nullable=False, unique=False)
    country = db.Column(db.String(20), nullable=False, unique=False)
    pincode = db.Column(db.BigInteger, nullable=False, unique=False)
    create_date = db.Column(db.DateTime, nullable=False, unique=False)
    # update_date = db.Column(db.DateTime, nullable=True, unique=False, default=dt.now())

    donations_details = db.relationship("DonationsModel", backref="donors")

    def __init__(
        self,
        _id: int,
        name: str,
        gender: str,
        email_address: str,
        date_of_birth,
        date_of_anniversary,
        pan: str,
        uid: int,
        country_code: int,
        phone_number: str,
        reference: int,
        other_reference: str,
        referrer_name: str,
        address_line_1: str,
        address_line_2: str,
        city: str,
        state: str,
        country: str,
        pincode: int,
        create_date,
        # update_date,
    ):
        self.id = _id
        self.name = name
        self.email_address = email_address
        self.gender = (gender,)
        self.date_of_birth = date_of_birth
        self.date_of_anniversary = date_of_anniversary
        self.pan = pan
        self.uid = uid
        self.country_code = country_code
        self.phone_number = phone_number
        self.reference = reference
        self.other_reference = other_reference
        self.referrer_name = referrer_name
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city = city
        self.state = state
        self.country = country
        self.pincode = pincode
        self.create_date = create_date

        # if update_date is None:
        #     self.update_date = None

    @classmethod
    def find_by_email_address(cls, email_address: str):
        return cls.query.filter_by(email_address=email_address).first()

    @classmethod
    def get_all_donors(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id: str):
        return cls.query.filter_by(id=_id).first()

    def save_to_database(self) -> None:
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self) -> None:
        db.session.delete(self)
        db.session.commit()