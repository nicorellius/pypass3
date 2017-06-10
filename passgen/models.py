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