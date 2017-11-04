import requests


class Cap1API(object):
    EP = 'https://3hkaob4gkc.execute-api.us-east-1.amazonaws.com/prod/au-hackathon'

    def accounts(self, acctid=None):
        if acctid:
            body = {
                'account_id': acctid,
            }
            return requests.post('{}/accounts'.format(self.EP), json=body)
        else:
            return requests.post('{}/accounts'.format(self.EP))

    def customers(self, custid=None):
        if custid:
            body = {
                'customer_id': custid,
            }
            return requests.post('{}/customers'.format(self.EP), json=body)
        else:
            return requests.post('{}/customers'.format(self.EP))

    def transactions(self, acctid):
        body = {
            'account_id': acctid,
        }
        return requests.post('{}/transactions'.format(self.EP), json=body)

    def rewards(self, acctid):
        body = {
            'account_id': acctid,
        }
        return requests.post('{}/rewards'.format(self.EP), json=body)

    def payments(self, acctid):
        body = {
            'account_id': acctid,
        }
        return requests.post('{}/payments'.format(self.EP), json=body)
