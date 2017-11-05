#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
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
    helper.make_density_plots(df_agg, agg_values, month, 'spend')
    helper.make_density_plots(df_agg, agg_values, month, 'reward')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run user against Capital One '
                                     'distributions.')
    parser.add_argument('-u', '--user', required=True, type=int, help='The '
                        'customer ID to compare against distributions.')
    args_dict = vars(parser.parse_args())

    run(args_dict)
