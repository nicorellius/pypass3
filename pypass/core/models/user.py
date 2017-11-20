import mongoengine
import datetime

from flask_login import UserMixin

from .secret import Secret


class User(mongoengine.Document, UserMixin):

    name = mongoengine.StringField()
    username = mongoengine.StringField(required=True)
    social_id = mongoengine.StringField(required=True)
    email = mongoengine.EmailField()
    created = mongoengine.DateTimeField(required=True,
                                        default=datetime.datetime.now)
    # avatar = mongoengine.ImageField()

    passwords = mongoengine.EmbeddedDocumentListField(Secret)

    meta = {
        'db_alias': 'core',
        'collection': 'users',
    }

    def __unicode__(self):
        return self.username

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
        return self.social_id
