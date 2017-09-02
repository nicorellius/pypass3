import mongoengine

from flask_login import UserMixin

from .secret import Secret


# class User(UserMixin):
#
#     def __init__(self, username, social_id, email=None):
#
#         self.username = username
#         self.social_id = social_id
#         self.email = email
#
#     def __repr__(self):
#         return '{0}'.format(self.username)
#
#     @property
#     def is_authenticated(self):
#         return True
#
#     @property
#     def is_active(self):
#         return True
#
#     @property
#     def is_anonymous(self):
#         return False
#
#     def get_id(self):
#         return self.username


class User(mongoengine.Document, UserMixin):

    name = mongoengine.StringField()
    username = mongoengine.StringField(required=True)
    social_id = mongoengine.StringField()
    email = mongoengine.EmailField(required=True)
    # avatar = mongoengine.ImageField()

    passwords = mongoengine.EmbeddedDocumentListField(Secret)

    meta = {
        'db_alias': 'core',
        'collection': 'users',
    }

    # def __init__(self, username, social_id, email=None):
    #
    #     self.username = username
    #     self.social_id = social_id
    #     self.email = email

    def __repr__(self):
        return '{0}'.format(self.username)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username
