__author__ = 'Hwaipy'

import pyvisa as visa
from Utils import SingleThreadProcessor
from SCPI import SCPI
import sys

class VISAInstrument:
    manufacturer = 'USTC'
    model = 'VISAInstrument'

    def __init__(self, resourceID, channel=1):
        self.resourceID = resourceID
        self.channelCount = channel
        try:
            self.resource = visa.ResourceManager().open_resource(resourceID)
        except BaseException as e:
            raise DeviceException('Error in open device ID: {}'.format(id), e)
        stp = SingleThreadProcessor()
        def stpQuery(*args):
            return stp.invokeAndWait(self.resource.query, *args)
        def stpWrite(*args):
            stp.invokeLater(self.resource.write, *args)
        self.scpi = SCPI(stpQuery, stpWrite)
        self.verifyIdentity()

    def getIdentity(self):
        return [VISAInstrument.manufacturer,VISAInstrument.model,'0','1.0.0']

    def verifyIdentity(self):
        idns = self.getIdentity()
        if ((idns[0] == self.__class__.manufacturer)) and ((idns[1] ==self.__class__.model)):
            self.serialNumber = idns[2]
            self.version = idns[3]
            self.maxChannelNum = 1
        else:
            raise DeviceException('Identity {} not recognized.'.format(idns))

    def checkChannel(self, channel):
        if channel>=0 and channel < self.channelCount:
            return
        raise DeviceException('Channel {} out of range.'.format(channel))

    @classmethod
    def connect(cls, resourceID):
        wrapper = VISAInstrumentWrapper(cls(resourceID))
        wrapper.verifyIdentity()
        return wrapper

    @classmethod
    def listResources(cls):
        resources = visa.ResourceManager().list_resources()
        valid = []
        for resource in resources:
            try:
                r = visa.ResourceManager().open_resource(resource)
                r.timeout=100
                idn = r.query('*IDN?')[:-1]
                idns = [i.strip(' ') for i in idn.split(',')]
                if (idns[0] == cls.manufacturer) and (idns[1] == cls.model):
                    valid.append(resource)
                r.close()
            except BaseException as e:
                pass
        return valid
class VISAInstrumentWrapper:
    def __init__(self, instrument):
        self.instrument = instrument

    def __getattr__(self, item):
        try:
            method = self.instrument.__getattribute__(item)
        except AttributeError as ae:
            raise AttributeError("'{}' object has no attribute '{}'".format(self.instrument.__class__,item))
        def instrumentInvoke(*args,**kwargs):
            try:
                return method(*args,**kwargs)
            except BaseException as e:
                if isinstance(e,DeviceException):
                    raise e
                raise DeviceException('Error in {}'.format(item), e)
        return instrumentInvoke

class DeviceException(BaseException):
    def __init__(self, msg, exception=None):
        self.message = msg
        self.exception = exception

class InstrumentsServer:
    def __init__(self):
        pass

if __name__ == '__main__':
    print('Instrument')
