import pytest
from .. import src
import os

l = None
def setup_module(module):
    global l
    l = src.my_logger(name='test.log',level=10)

def test_file_creation():
    l.debug('Test file creation')
    assert os.path.exists('test.log')

def test_correct_level():
    l = src.my_logger(name='test.log')
    test_msg = 'TEST'
    l.debug(test_msg)
    with open('test.log','r') as f:
        last_record = f.read().split('\n')[-2] #The last item is an empty string
        msg = last_record.split(' - ')[-1]
    assert test_msg == msg