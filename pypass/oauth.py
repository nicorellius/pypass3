import json

from flask import current_app, url_for, request, redirect, session

from rauth import OAuth1Service, OAuth2Service

from . import config
from . import utils


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

        super(GitHubSignIn, self).__init__('github')

        self.service = OAuth2Service(
            name='github',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://github.com/login/oauth/authorize',
            access_token_url='https://github.com/login/oauth/access_token',
            base_url='https://api.github.com'
        )

    def authorize(self):

        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):

        if 'code' not in request.args:
            return None, None, None

        oauth_session = self.service.get_auth_session(
            data={
                'code': request.args['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': self.get_callback_url()
            },
        )

        config.logger.info('[{0}] OAuth session: {1}'.format(
            utils.get_timestamp(), oauth_session))

        # social_id = 'github${0}'.format('social_id')
        # username = 'username'
        # email = 'email'

        # the "me" response
        me = oauth_session.get('user').json()
        username = me['login']
        social_id = 'github${0}'.format(me['id'])
        email = me['url']
        # nickname = me['name'].split()[0].lower()

        return social_id, username, email  # nickname,


class FacebookSignIn(OAuthSignIn):

    def __init__(self):

        super(FacebookSignIn, self).__init__('facebook')

        self.service = OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )

    def authorize(self):

        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):

        def decode_json(payload):
            return json.loads(payload.decode('utf-8'))

        if 'code' not in request.args:
            return None, None, None

        oauth_session = self.service.get_auth_session(
            data={
                'code': request.args['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': self.get_callback_url()
            },
            decoder=decode_json
        )

        me = oauth_session.get('me?fields=id,email').json()
        config.logger.info('[{0}] Me in provider callback: {1}'.format(
            utils.get_timestamp(), me))

        # Facebook does not provide a username, so the user email is used
        # to extract one out

        social_id = 'facebook${0}'.format(me['id'])
        username = me.get('email').split('@')[0]
        email = me.get('email')

        return social_id, username, email


class TwitterSignIn(OAuthSignIn):

    def __init__(self):

        super(TwitterSignIn, self).__init__('twitter')

        self.service = OAuth1Service(
            name='twitter',
            consumer_key=self.consumer_id,
            consumer_secret=self.consumer_secret,
            request_token_url='https://api.twitter.com/oauth/request_token',
            authorize_url='https://api.twitter.com/oauth/authorize',
            access_token_url='https://api.twitter.com/oauth/access_token',
            base_url='https://api.twitter.com/1.1/'
        )

    def authorize(self):

        request_token = self.service.get_request_token(
            params={
                'oauth_callback': self.get_callback_url()
            }
        )

        session['request_token'] = request_token

        return redirect(self.service.get_authorize_url(request_token[0]))

    def callback(self):

        request_token = session.pop('request_token')

        if 'oauth_verifier' not in request.args:
            return None, None, None

        oauth_session = self.service.get_auth_session(
            request_token[0],
            request_token[1],
            data={
                'oauth_verifier': request.args['oauth_verifier']
            }
        )

        me = oauth_session.get('account/verify_credentials.json').json()
        social_id = 'twitter${0}'.format(str(me.get('id')))
        username = me.get('screen_name')

        return social_id, username, None  # Twitter does not provide email


class GoogleSignIn(OAuthSignIn):

    def __init__(self):

        super(GoogleSignIn, self).__init__('google')

        self.service = OAuth2Service(
            name='google',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            access_token_url='https://accounts.google.com/o/oauth2/token',
            base_url='https://www.googleapis.com/plus/v1/people/'
        )

    def authorize(self):

        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):

        def decode_json(payload):
            return json.loads(payload.decode('utf-8'))

        if 'code' not in request.args:
            return None, None, None

        oauth_session = self.service.get_auth_session(
            data={
                'code': request.args['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': self.get_callback_url()
            },
            decoder=decode_json
        )

        try:
            me = oauth_session.get('me').json()
            me_email = None

            config.logger.info('[{0}] Me in provider callback: {1}'.format(
                utils.get_timestamp(), me))

            for e in me['emails']:
                if e['type'] == 'account':
                    me_email = e['value']

            return me.get('id'), me.get('displayName'), me_email

        except KeyError as ke:
            print("Seems something is wrong with Google's response")
            print('KeyError: {0} not found in response'.format(ke))

