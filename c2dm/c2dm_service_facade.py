import urllib
import urllib2


class C2DMServiceFacade:

    def __init__(self, collapse_key='boguskey'):
        self.url = 'https://android.apis.google.com/c2dm/send'
        self._collapse_key = collapse_key
        self.token_factory = ClientLoginTokenFactory()

    def request_wakeup_of_mds(self, registration_id):
        values = {
            'collapse_key': self._collapse_key,
            'registration_id': registration_id,
        }
        body = urllib.urlencode(values)
        request = urllib2.Request(self.url, body)
        token = self.token_factory.get_token()
        request.add_header('Authorization', 'GoogleLogin auth=%s' % token)
        response = urllib2.urlopen(request)
        if response.code == 200:
            print('Attempt to send message to device with registration id:')
            print(registration_id)
            print('was successful.')
            print('The returned body is:')
            print(response.read())
            return True


class ClientLoginTokenFactory():
    _token = None

    def __init__(self):
        self.url = 'https://www.google.com/accounts/ClientLogin'
        self.account_type = 'HOSTED_OR_GOOGLE'
        self.email = 'c2dmvalidaccount@gmail.com'
        self.password = 'password'
        self.source = 'C2DMVALIDACCOUNT-C2DM-1'
        self.service = 'ac2dm'

    def get_token(self):
        if self._token is None:
            values = {
                'accountType': self.account_type,
                'Email': self.email,
                'Passwd': self.password,
                'source': self.source,
                'service': self.service,
            }
            data = urllib.urlencode(values)
            request = urllib2.Request(self.url, data)
            response = urllib2.urlopen(request)
            responseAsString = response.read()
            responseAsList = responseAsString.split('\n')
            self._token = responseAsList[2].split('=')[1]

        return self._token
