import requests


class Cap1API(object):
    EP = 'https://3hkaob4gkc.execute-api.us-east-1.amazonaws.com/prod/au-hackathon'

    @staticmethod
    def assert200(call):
        assert call.status_code==200

    def accounts(self, acctid=None):
        if acctid:
            body = {
                'account_id': acctid,
            }
            res = requests.post('{}/accounts'.format(self.EP), json=body)
        else:
            res = requests.post('{}/accounts'.format(self.EP))
        try:
            self.assert200(res)
            return res.json()
        except AssertionError:
            print('Bad call; {}'.format(res.text))

    def customers(self, custid=None):
        if custid:
            body = {
                'customer_id': custid,
            }
            res = requests.post('{}/customers'.format(self.EP), json=body)
        else:
            res = requests.post('{}/customers'.format(self.EP))
        try:
            self.assert200(res)
            return res.json()
        except AssertionError:
            print('Bad call; {}'.format(res.text))

    def transactions(self, acctid):
        body = {
            'account_id': acctid,
        }
        res = requests.post('{}/transactions'.format(self.EP), json=body)
        try:
            self.assert200(res)
            return res.json()
        except AssertionError:
            print('Bad call; {}'.format(res.text))

    def rewards(self, acctid):
        body = {
            'account_id': acctid,
        }
        res = requests.post('{}/rewards'.format(self.EP), json=body)
        try:
            self.assert200(res)
            return res.json()
        except AssertionError:
            print('Bad call; {}'.format(res.text))

    def payments(self, acctid):
        body = {
            'account_id': acctid,
        }
        res = requests.post('{}/payments'.format(self.EP), json=body)
        try:
            self.assert200(res)
            return res.json()
        except AssertionError:
            print('Bad call; {}'.format(res.text))
