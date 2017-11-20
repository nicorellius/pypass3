import mongoengine
import datetime


class Secret(mongoengine.EmbeddedDocument):

    account_name = mongoengine.StringField(required=True)
    login_string = mongoengine.StringField()
    # password = mongoengine.StringField()
    password = mongoengine.BinaryField()
    url = mongoengine.URLField()
    notes = mongoengine.StringField()
    created = mongoengine.DateTimeField(required=True,
                                        default=datetime.datetime.now)
