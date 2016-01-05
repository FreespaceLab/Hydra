__author__ = 'Benli'
__version__ = 'v1.0.20160105'

import visa
from SCPI import SCPI
from InstrumentServers import InstrumentServer,DeviceException
from Utils import SingleThreadProcessor

class PM200:
    def __init__(self, id):
        self.id = id
        try:
            rm = visa.ResourceManager().open_resource(id)
        except BaseException as e:
            raise DeviceException('Error in open device ID: {}'.format(id), e)
        stp = SingleThreadProcessor()
        def stpQuery(*args):
            return stp.invokeAndWait(rm.query, *args)
        def stpWrite(*args):
            stp.invokeLater(rm.write, *args)
        self.scpi = SCPI(stpQuery, stpWrite)
        idns = self.getIdentity()
        if (idns[0] == 'Thorlabs') and (idns[1] == 'PM200'):
            self.serialNumber = idns[2]
            self.version = idns[3]
            self.maxChannelNum = 1
        else:
            raise DeviceException('Identity {} not recognized.'.format(idns))
        self.__setLineFrequency()

    def getIdentity(self):
        try:
            idn = self.scpi._IDN.query()
            if idn is None:
                return [''] * 4
            if len(idn) is 0:
                return [''] * 4
            idns = idn.split(',')
            while len(idns) < 4:
                idns.append('')
            return idns[:4]
        except Exception as e:
            raise DeviceException('Error in getIdentity', e)

    def getWavelength(self, channel):
        self.__checkChannel(channel)
        try:
            wl = self.scpi.SENSE.CORRECTION.WAVELENGTH.query()
            return float(wl)
        except Exception as e:
            raise DeviceException('Error in getWavelength', e)

    def setWavelength(self, channel, wavelength):
        self.__checkChannel(channel)
        try:
            wavelengthI = wavelength * 100 // 1 / 100
            self.scpi.SENSE.CORRECTION.WAVELENGTH.write(wavelengthI)
            wavelengthC = self.getWavelength(channel)
        except Exception as e:
            raise DeviceException('Error in setWavelength', e)
        if wavelengthI != wavelengthC:
            raise DeviceException('Wavelength {} out of range.'.format(wavelength))

    def isAutoRange(self, channel):
        self.__checkChannel(channel)
        try:
            return self.scpi.SENSE.POWER.DC.RANGE.AUTO.query() == '1'
        except Exception as e:
            raise DeviceException('Error in isAutoRange', e)

    def setAutoRange(self, channel, status):
        self.__checkChannel(channel)
        try:
            self.scpi.SENSE.POWER.RANGE.AUTO.write(1 if status else 0)
        except Exception as e:
            raise DeviceException('Error in setAutoRange', e)

    def getMeasureRange(self, channel):
        self.__checkChannel(channel)
        try:
            return self.scpi.SENSE.POWER.DC.RANGE.query()
        except Exception as e:
            raise DeviceException('Error in getMeasureRange', e)

    def setMeasureRange(self, channel, measureRange):
        self.__checkChannel(channel)
        try:
            self.scpi.SENSE.POWER.RANGE.write(measureRange)
        except Exception as e:
            raise DeviceException('Error in setMeasureRange', e)

    def beeper(self):
        try:
            self.scpi.SYSTem.BEEPer.write()
        except Exception as e:
            raise DeviceException('Error in beeper', e)

    def getAveragingRate(self, channel):
        self.__checkChannel(channel)
        try:
            return int(self.scpi.SENSe.AVERage.COUNt.query())
        except Exception as e:
            raise DeviceException('Error in getAveragingRate', e)

    def setAveragingRate(self, channel, averagingRate):
        self.__checkChannel(channel)
        try:
            self.scpi.SENSe.AVERage.COUNt.write(averagingRate)
        except Exception as e:
            raise DeviceException('Error in setAveragingRate', e)

    def getBandWidthFilterStatus(self, channel):
        self.__checkChannel(channel)
        try:
            return self.scpi.INPut.FILTer.query() == '1'
        except Exception as e:
            raise DeviceException('Error in getBandWidthFilterStatus', e)

    def setBandWidthFilterStatus(self, channel, status):
        self.__checkChannel(channel)
        try:
            self.scpi.INPut.FILTer.write(1 if status else 0)
        except Exception as e:
            raise DeviceException('', e)

    def getBeamDiameter(self, channel):
        self.__checkChannel(channel)
        try:
            return self.scpi.SENSE.CORRECTION.BEAMdiameter.query()
        except Exception as e:
            raise DeviceException('', e)

    def setBeamDiameter(self, channel, diameter):
        self.__checkChannel(channel)
        try:
            self.scpi.SENSE.CORRECTION.BEAMdiameter.write(diameter)
        except Exception as e:
            raise DeviceException('', e)

    def measure(self, channel):
        self.__checkChannel(channel)
        try:
            return float(self.scpi.MEASure.query())
        except Exception as e:
            raise DeviceException('', e)

    def reset(self):
        try:
            self.scpi._RST.write()
        except Exception as e:
            raise DeviceException('', e)

    def __measureLoop(self):
        pass

    def __setLineFrequency(self):
        try:
            return self.scpi.SYSTem.LFRequency.write(50)
        except Exception as e:
            raise DeviceException('', e)

    def __checkChannel(self, channel):
        if channel>=0 and channel < self.maxChannelNum:
            return
        raise DeviceException('Channel {} out of range.'.format(channel))

    def __getSensorInfo__NotComplete(self):
        try:
            si = self.scpi.SYSTem.SENsor.IDN.query()
            print(si)
            # sis=re.split(',',si[:-1])
            # print(sis)
            # sibin=bin(int(sis[5]))
            # if sibin＆(1<<5)
            return si
        except Exception as e:
            raise DeviceException('', e)
            # self.rm.query('SYSTem:SENSor:IDN?')

if __name__ == '__main__':
    print('go')
    rm = visa.ResourceManager()
    instIDs = rm.list_resources()
    id = 'USB0::0x1313::0x80B0::P3000997::INSTR'
    pm = PM200(id)
    print(pm.setWavelength(0,809.1))
    print(pm.getWavelength(0))