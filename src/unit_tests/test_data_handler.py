# -*- coding: utf-8 -*-
import datetime
import pytest

from data_handler import StreamingDataframe


def test_handle_CMTE_ID():
    # Only criteria here is that the ID is not blank
    valid, _ = StreamingDataframe._handle_CMTE_ID('SINFIO')
    assert valid

    valid, _ = StreamingDataframe._handle_CMTE_ID(' ')
    assert not valid


def test_handle_NAME():
    # Name must have a first and last separated by comma
    valid, _ = StreamingDataframe._handle_NAME('Nobody')
    assert not valid

    valid, _ = StreamingDataframe._handle_NAME('SOME, Body')
    assert valid

    # Test unicode handling
    valid, _ = StreamingDataframe._handle_NAME('UNICODE, José')
    hash('UNICODE, José')
    assert valid


def test_handle_ZIP_CODE():
    # Must have at least 5 digits
    valid, _ = StreamingDataframe._handle_ZIP_CODE('123')
    assert not valid

    # Greater than 5 ok
    valid, _ = StreamingDataframe._handle_ZIP_CODE('12345678')
    assert valid

    # Must have numbers in first 5
    valid, _ = StreamingDataframe._handle_ZIP_CODE('A12345')
    assert not valid

    # Blank fails
    valid, _ = StreamingDataframe._handle_ZIP_CODE('')
    assert not valid


def test_handle_TRANSACTION_DT():
    # Date string too long
    valid, _ = StreamingDataframe._handle_TRANSACTION_DT('120319999')
    assert not valid

    # Date string too short
    valid, _ = StreamingDataframe._handle_TRANSACTION_DT('1203199')
    assert not valid

    # Invalid month field
    valid, _ = StreamingDataframe._handle_TRANSACTION_DT('13031999')
    assert not valid

    # Invalid day field
    valid, _ = StreamingDataframe._handle_TRANSACTION_DT('12331999')
    assert not valid

    # Year before 1975
    valid, _ = StreamingDataframe._handle_TRANSACTION_DT('12031974')
    assert not valid

    # Correctly formatted date
    valid, _ = StreamingDataframe._handle_TRANSACTION_DT('12031999')
    assert valid

    # Today's date ok
    now = datetime.datetime.now()
    date_string = ''.join([
        str(now.month).zfill(2),
        str(now.day).zfill(2),
        str(now.year)])
    valid, _ = StreamingDataframe._handle_TRANSACTION_DT(date_string)
    assert valid

    # Date has not yet passed
    now += datetime.timedelta(days=7)
    date_string = ''.join([
        str(now.month).zfill(2),
        str(now.day).zfill(2),
        str(now.year)])
    valid, _ = StreamingDataframe._handle_TRANSACTION_DT(date_string)
    assert not valid


def test_handle_TRANSACTION_AMT():
    # Transaction amount can't be negative
    valid, _ = StreamingDataframe._handle_TRANSACTION_AMT('-12.53')
    assert not valid

    # Transaction amount must be a number
    valid, _ = StreamingDataframe._handle_TRANSACTION_AMT('-A1 steaksauce')
    assert not valid

    # Valid number
    valid, _ = StreamingDataframe._handle_TRANSACTION_AMT('12.53 ')
    assert valid


def test_handle_OTHER_ID():
    # Field should be blank
    valid, _ = StreamingDataframe._handle_OTHER_ID('AOFOO')
    assert not valid

    # Valid entry
    valid, _ = StreamingDataframe._handle_OTHER_ID('  ')
    assert valid
