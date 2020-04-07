from database import db


class MM(db.Model):
    __tablename__ = 'modes_of_donation'

    id = db.Column(db.INTEGER, primary_key=True)
    mode_name = db.Column(db.VARCHAR(15), unique=True, nullable=False)
    create_date = db.Column(db.DATE, nullable=False, unique=False)
    update_date = db.Column(db.DATE, nullable=False, unique=False)

    donations = db.relationship('DonationsModel', backref='mode', lazy=True)

    def __init__(self, _id, mode_name, create_date, update_date):
        self.id = _id
        self.mode_name = mode_name
        self.create_date = create_date
        self.update_date = update_date

    @classmethod
    def get_all_modes(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name):
          return cls.query.filter_by(mode_name=name).first()

    def save_to_database(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self):
        db.session.delete(self)
        db.session.commit()
