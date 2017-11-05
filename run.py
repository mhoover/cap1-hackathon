#!/usr/bin/python
# -*- coding: utf-8 -*-
import ConfigParser
import pandas as pd
import sys

from cap1Hackathon import *


def run(args_dict):
    # initialize API client and account helper class
    client = Cap1API()
    helper = Cap1Account(client)

    # load distribution data
    try:
        dist = pd.read_csv('sampled_data.csv', sep=None, engine='python')
    except IOError:
        sys.exit('STOP! Have not setup comparison distributions. Please do so.')

    # get customer information
    acct = client.customers(args_dict['user'])
    trans = client.transactions(acct[0]['account_id'])
    age = helper.calculate_age(acct[0]['customers'][0]['dob'])
    agg_values = helper.get_cust_transaction_values(args_dict['user'], trans)

    # filter data to age range
    df = dist[((age-5) <= dist.age) & (dist.age <= (age+5))]

    # aggregate data
    df_agg = (df
              .groupby(['acct_id', 'month', 'year'])
              [['reward', 'spend']]
              .sum()
              .reset_index())

    # make plots
    month = datetime.now().month
    decision = helper.make_density_plots(df_agg, agg_values, month,
                                         args_dict['graph'], args_dict['limit'])

    # return decision
    return decision


if __name__ == '__main__':
    run(args_dict)
