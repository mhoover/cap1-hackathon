#!/usr/bin/python
# -*- coding: utf-8 -*-
import ConfigParser
import pandas as pd
import random

from datetime import datetime
from dateutil.relativedelta import relativedelta

from cap1Hackathon import *


def create_transaction_df(transactions):
    df = pd.DataFrame()
    for account in transactions:
        acctid = account[0]['account_id']
        for customer in account[0]['customers']:
            custid = customer['customer_id']
            tmp = pd.DataFrame({
                'acct_id': acctid,
                'cust_id': custid,
                'spend': get_values(customer['transactions'], 'amount'),
                'reward': get_values(customer['transactions'], 'rewards_earned'),
                'month': get_values(customer['transactions'], 'month'),
                'year': get_values(customer['transactions'], 'year'),
            })
            df = pd.concat([df, tmp], axis=0)
    return df.reset_index(drop=True)


def gather_account_information(account, client):
    tmp = client.accounts(account)
    return pd.DataFrame({
        'acct_id': [tmp[0]['account_id']],
        'credit': [tmp[0]['credit_limit'] - tmp[0]['balance']],
        'points': [tmp[0]['total_rewards_earned'] - tmp[0]['total_rewards_used']],
    })


def gather_customer_information(customer, client):
    tmp = client.customers(customer)
    dob = datetime.strptime(tmp[0]['customers'][0]['dob'], '%m/%d/%Y')
    return pd.DataFrame({
        'acct_id': [tmp[0]['account_id']],
        'cust_id': [tmp[0]['customers'][0]['customer_id']],
        'primary': [tmp[0]['customers'][0]['is_primary']],
        'age': [relativedelta(datetime.now(), dob).years],
    })


def gather_payment_information(account, client):
    tmp = client.payments(account)
    return pd.DataFrame({
        'acct_id': tmp[0]['account_id'],
        'card': tmp[0]['card_type'],
        'balance': [x['total_balance_remaining'] for x in tmp[0]['payments']],
        'month': [x['month'] for x in tmp[0]['payments']],
        'year': [x['year'] for x in tmp[0]['payments']],
    })


def get_values(data, field):
    return [x[field] for x in data]


def sample_accounts(accounts, n=50):
    if len(accounts)>n:
        return random.sample(accounts, n)
    else:
        return accounts


def run():
    # initial API client
    client = Cap1API()

    # gather transactions
    customer_accounts = [x for x in client.customers() if
                         len(x['customer_id'])==int(n_family)]
    accounts = [x['account_id'] for x in customer_accounts]

    transactions = [client.transactions(x) for x in sample_accounts(accounts)]

    # parse out money and points
    df = create_transaction_df(transactions)

    # create account, customer, and payment detail dataframes
    acct_df = pd.concat([gather_account_information(x, client) for x in
                        df.acct_id.unique().tolist()], axis=0)

    cust_df = pd.concat([gather_customer_information(x, client) for x in
                        df.cust_id.unique().tolist()], axis=0)

    pay_df = pd.concat([gather_payment_information(x, client) for x in
                       df.acct_id.unique().tolist()], axis=0)

    # merge data together
    df = df.merge(acct_df, on='acct_id')
    df = df.merge(cust_df, on=['acct_id', 'cust_id'])
    df = df.merge(pay_df, on=['acct_id', 'month', 'year'])

    # dump data to disk
    df.to_csv('sampled_data.csv', index=False)


if __name__ == '__main__':
    cfg = ConfigParser.ConfigParser()
    cfg.read('config.cfg')
    n_family = cfg.get('setup', 'n_family')

    run()
