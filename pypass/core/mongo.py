import ssl

import mongoengine


def global_init(user=None, password=None,
                port=27972, server='localhost', use_ssl=True):

    if user or password:
        data = dict(
            username=user,
            password=password,
            host=server,
            port=port,
            authentication_source='admin',
            authentication_mechanism='SCRAM-SHA-1',
            ssl=use_ssl,
            ssl_cert_reqs=ssl.CERT_NONE)
        mongoengine.register_connection(alias='core', name='pypass', **data)
        data['password'] = '***************'
        print("Registering production connection: {}".format(data))

    else:
        print("Registering development connection")
        mongoengine.register_connection(alias='core', name='pypass')
