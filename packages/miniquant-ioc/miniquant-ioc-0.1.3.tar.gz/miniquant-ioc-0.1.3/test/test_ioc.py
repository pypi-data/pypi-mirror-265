#!/usr/bin/python3

from miniquant_ioc.application  import init_app as init_ioc
import time

import multiprocessing as mp
#mp.set_start_method('fork')

from caproto.sync.client import read as ca_read, write as ca_write
from caproto import CASeverity

import pytest, asyncio, sys, os

now = time.time()

def start_ioc(prefix='MINIQUANT_TEST'):
    app = init_ioc(prefix)
    app.startIoc()
    time.sleep(1)
    print(f'{app.prefix}: IOC running')
    return app

@pytest.mark.asyncio
async def test_ioc():

    #
    # This is just a simple test to ascertain if the IOC comes up at all.
    
    ioc = start_ioc()

    pv = [ 'SYNCRATE', 'CH0_COUNTRATE' ]

    for s in pv:
        epics_var = f'{ioc.prefix}:{s}'
        result = ca_read(epics_var)
        data = result.data
        print(f'{epics_var}: {data}')
        assert len(data) > 0
