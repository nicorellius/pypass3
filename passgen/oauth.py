from flask import url_for
from rauth import OAuth2Service

from pypass import app as current_app

####################################
from oauth import OAuthSignIn
app.config['OAUTH_CREDENTIALS'] = {
    'github': {
        'id': 'd3be9a39c8db65911ce0',
        'secret': 'cba32867fc777bd1291425e3aeedb222f51ef7c0'
    },
}

@app.route('/authorize/github')
def oauth_authorize(provider):

    if not current_user.is_anonymous():
        return redirect(url_for('index'))

    oauth = OAuthSignIn.get_provider(provider)

    return oauth.authorize()
#########################################


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(cls, provider_name):
        if cls.providers is None:
            cls.providers = {}
            for provider_class in cls.__subclasses__():
                provider = provider_class()
                cls.providers[provider.provider_name] = provider
        return cls.providers[provider_name]


class GitHubSignIn(OAuthSignIn):
    def __init__(self):
        super(GitHubSignIn, self).__init__('facebook')
        self.service = OAuth2Service(
            name='github',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )
