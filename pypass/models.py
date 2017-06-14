# from
#
# class User(UserMixin, db.Model):
#
#     __tablename__ = 'users'
#
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), nullable=False, unique=True)
#     social_id = db.Column(db.String(64), nullable=False, unique=True)
#     nickname = db.Column(db.String(64), nullable=False)
#     email = db.Column(db.String(64), nullable=True)
#
#     def __init__(self, username, social_id, nickname, email=None):
#         self.username = username
#         self.social_id = social_id
#         self.email = email
#         self.nickname = nickname
#
#     def __repr__(self):
#         return '{0}'.format(self.username)

# from werkzeug.security import check_password_hash

from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, username, social_id, email):
        self.username = username
        self.social_id = social_id
        self.email = email

    def get_id(self):
        return self.username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def __repr__(self):
        return '{0}'.format(self.username)

    # @staticmethod
    # def validate_login(password_hash, password):
    #     return check_password_hash(password_hash, password)
