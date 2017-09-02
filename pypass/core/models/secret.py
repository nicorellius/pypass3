import mongoengine


class Secret(mongoengine.EmbeddedDocument):

    account_name = mongoengine.StringField(required=True)
    login_string = mongoengine.StringField()
    password = mongoengine.StringField()
    url = mongoengine.URLField()
    notes = mongoengine.StringField()

    meta = {
        'db_alias': 'core',
        'collection': 'secrets',
    }
