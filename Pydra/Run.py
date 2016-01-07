__author__ = 'Hwaipy'

import pyvisa as visa
from Utils import SingleThreadProcessor
from SCPI import SCPI
import sys
import Instruments

if __name__ == '__main__':
    print('Run')
    from servers.Thorlabs_PowerMeters import PM200 as PM200
    from servers.ITECH_IT6322 import IT6322
    import time
    isn = Instruments.InstrumentsServer()
    res = PM200.listResources()
    for re in res:
        pm = PM200(re)
        print(pm.getIdentity())

    res = IT6322.listResources()
    for re in res:
        pm = IT6322(re)
        print(pm.getIdentity())
