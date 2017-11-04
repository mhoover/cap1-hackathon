#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest

from cap1Hackathon import *


def test_api_accounts():
    result = Cap1API().accounts()
    assert isinstance(result, list)


def test_api_accounts_record():
    result = Cap1API().accounts(100300000)
    assert isinstance(result, list)
    assert len(result)==1
    assert isinstance(result[0], dict)


def test_api_customers():
    result = Cap1API().customers()
    assert isinstance(result, list)


def test_api_customers_record():
    result = Cap1API().customers(101710000)
    assert isinstance(result, list)
    assert len(result)==1
    assert isinstance(result[0], dict)


def test_api_transactions():
    result = Cap1API().transactions(100300000)
    assert isinstance(result, list)
    assert len(result)>=1
    assert isinstance(result[0], dict)


def test_api_rewards():
    result = Cap1API().rewards(100300000)
    assert isinstance(result, list)
    assert len(result)>=1
    assert isinstance(result[0], dict)


def test_api_payments():
    result = Cap1API().payments(100300000)
    assert isinstance(result, list)
    assert len(result)>=1
    assert isinstance(result[0], dict)
