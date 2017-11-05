#!/usr/bin/python
# -*- coding: utf-8 -*-
import ConfigParser
import pandas as pd
import random

from datetime import datetime
from dateutil.relativedelta import relativedelta

from cap1Hackathon import *


def sample_accounts(accounts, n=50):
    if len(accounts)>n:
        return random.sample(accounts, n)
    else:
        return accounts


def run():
    # initialize API client
    client = Cap1API()

    # gather transactions
    customer_accounts = [x for x in client.customers() if
                         len(x['customer_id'])==int(n_family)]
    accounts = [x['account_id'] for x in customer_accounts]

    transactions = [client.transactions(x) for x in sample_accounts(accounts)]

    # parse out money and points
    acct = Cap1Account(client)
    df = acct.create_transaction_df(transactions)

    # create account, customer, and payment detail dataframes
    acct_df = acct.gather_account_information(df.acct_id.unique().tolist())

    cust_df = acct.gather_customer_information(df.cust_id.unique().tolist())

    pay_df = acct.gather_payment_information(df.acct_id.unique().tolist())

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
