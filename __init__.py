import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sbn

from datetime import datetime
from dateutil.relativedelta import relativedelta


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


class Cap1Account(object):
    month_dict = {
        1: ['October', 'November', 'December'],
        2: ['November', 'December', 'January'],
        3: ['December', 'January', 'February'],
        4: ['January', 'February', 'March'],
        5: ['February', 'March', 'April'],
        6: ['March', 'April', 'May'],
        7: ['April', 'May', 'June'],
        8: ['May', 'June', 'July'],
        9: ['June', 'July', 'August'],
        10: ['July', 'August', 'September'],
        11: ['August', 'September', 'October'],
        12: ['September', 'October', 'November'],
    }

    def __init__(self, client):
        self.client = client

    @staticmethod
    def calculate_age(dob):
        return relativedelta(datetime.now(),
                             datetime.strptime(dob, '%m/%d/%Y')).years

    def create_transaction_df(self, transactions):
        df = pd.DataFrame()
        for account in transactions:
            acctid = account[0]['account_id']
            for customer in account[0]['customers']:
                custid = customer['customer_id']
                tmp = pd.DataFrame({
                    'acct_id': acctid,
                    'cust_id': custid,
                    'spend': self.get_values(customer['transactions'], 'amount'),
                    'reward': self.get_values(customer['transactions'],
                                              'rewards_earned'),
                    'month': self.get_values(customer['transactions'], 'month'),
                    'year': self.get_values(customer['transactions'], 'year'),
                })
                df = pd.concat([df, tmp], axis=0)
        return df.reset_index(drop=True)

    def gather_account_information(self, ids):
        df = pd.DataFrame()
        for id in ids:
            tmp = self.client.accounts(id)
            df = pd.concat([
                df,
                pd.DataFrame({
                    'acct_id': [tmp[0]['account_id']],
                    'credit': [tmp[0]['credit_limit'] - tmp[0]['balance']],
                    'points': [tmp[0]['total_rewards_earned'] -
                               tmp[0]['total_rewards_used']],
                })
            ], axis=0)
        return df.reset_index(drop=True)

    def gather_customer_information(self, ids):
        df = pd.DataFrame()
        for id in ids:
            tmp = self.client.customers(id)
            df = pd.concat([
                df,
                pd.DataFrame({
                    'acct_id': [tmp[0]['account_id']],
                    'cust_id': [tmp[0]['customers'][0]['customer_id']],
                    'primary': [tmp[0]['customers'][0]['is_primary']],
                    'age': [self.calculate_age(tmp[0]['customers'][0]['dob'])],
                })
            ], axis=0)
        return df.reset_index(drop=True)

    def gather_payment_information(self, ids):
        df = pd.DataFrame()
        for id in ids:
            tmp = self.client.payments(id)
            df = pd.concat([
                df,
                pd.DataFrame({
                    'acct_id': tmp[0]['account_id'],
                    'card': tmp[0]['card_type'],
                    'balance': [x['total_balance_remaining'] for x in
                                tmp[0]['payments']],
                    'month': [x['month'] for x in tmp[0]['payments']],
                    'year': [x['year'] for x in tmp[0]['payments']],
                })
            ], axis=0)
        return df.reset_index(drop=True)

    def get_cust_transaction_values(self, cust_id, transactions):
        tmp = [x['transactions'] for x in transactions[0]['customers'] if
               x['customer_id']==cust_id]
        tmp_df = pd.DataFrame({
            'month': self.get_values(tmp[0], 'month'),
            'year': self.get_values(tmp[0], 'year'),
            'spend': self.get_values(tmp[0], 'amount'),
            'reward': self.get_values(tmp[0], 'rewards_earned'),
        })
        return (tmp_df
                .groupby(['month', 'year'])
                [['spend', 'reward']]
                .sum()
                .reset_index())

    @staticmethod
    def get_values(data, field):
        return [x[field] for x in data]

    def make_density_plots(self, dist, usr, month, type=['spend', 'reward']):
        months = self.month_dict[month]
        max_ys = [(sbn.kdeplot(dist[type][dist.month==x])
                  .get_lines()[0]
                  .get_data()[1]
                  .max()) for x in months]
        plt.close()

        f, ax = plt.subplots(1, len(months), figsize=(20, 4))
        sbn.despine(left=True)
        [sbn.kdeplot(dist[type][dist.month==x], shade=True, color='red',
                     ax=ax[i], legend=False) for i, x in enumerate(months)]
        [ax[i].axvline(x=float(usr[type][usr.month==x]), color='black') for
         i, x in enumerate(months)]
        [ax[i].set_title('{} Against Distribution of Like People ({})'
                   .format(type.title(), x)) for i, x in enumerate(months)]
        plt.savefig('{}_plt.png'.format(type))
        plt.close()
