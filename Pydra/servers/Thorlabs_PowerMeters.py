__author__ = 'Benli'
__version__ = 'v1.0.20160105'

import visa
import sys
import SCPI

class PM200:
    def __init__(self, id):
        self.id = id
        self.rm = visa.ResourceManager().open_resource(id)
        self.scpi = SCPI(self.rm.query, self.rm.write)

    def rest(self):
        self.rm.write('*RST')
        return 'Device had been rest.'

    def setLineFrequency(self):
        return self.scpi.SYSTem.LFRequency.write([50])

    def getIdentity(self):
        return self.scpi._IDN.query()

    def getSensorInfo(self):
        return  self.scpi.SYSTem.SENsor.IDN.query()

    def getWavelength(self):
        wl = self.scpi.SENSE.CORRECTION.WAVELENGTH.query()
        return float(wl)

    def setWavelength(self, wavelength):
        self.scpi.SENSE.CORRECTION.WAVELENGTH.write([wavelength])

    def isAutoRange(self):
        return self.scpi.SENSE.POWER.DC.RANGE.AUTO.query()

    def getMeasureRange_at_W(self):
        return self.scpi.SENSE.POWER.DC.RANGE.query()

    def setMeasureRange_at_W(self, range):
        self.scpi.SENSE.POWER.RANGE.write([range])

    def setAutoRange(self, status):
        self.scpi.SENSE.POWER.RANGE.AUTO.write([1 if status else 0])

    def measure(self):
        return float(self.scpi.MEASure.query()[:-1])

    def Beeper(self):
        self.scpi.SYSTem.BEEPer.write()
        return 'Beeper had been activated'

    def setbeamdiameter(self, diameter):
        self.scpi.SENSE.CORRECTION.BEAMdiameter.write([diameter])

    def setdefaultbeamdiameter(self):
        self.setbeamdiameter('DEFault')

    def getbeamdiameter(self):
        return self.scpi.SENSE.CORRECTION.BEAMdiameter.query()

    def getbandwidth(self):
        return self.scpi.INPut.FILTer.query()


    def onBandwidthFilter(self):
        self.scpi.INPut.FILTer.write([1])

    def offBandwidthFilter(self):
        self.scpi.INPut.FILTer.write([0])

    def setAveragingRate(self, rate):
        self.scpi.SENSe.AVERage.COUNt.write([rate])

    def getAveragingRate(self):
        return self.scpi.SENSe.AVERage.COUNt.query()


class DeviceException(Exception):
    def __init__(self, msg, exception=None):
        self.message = msg
        self.exception = exception


class PM:
    def __init__(self, id):
        self.id = id
        try:
            rm = visa.ResourceManager().open_resource(id)
            IDN = rm.query('*IDN?')
            if (IDN.find('Thorlabs') != -1) and IDN.find('PM200'):
                self.pm = PM200(id)
                self.type = 'PM200'
                self.maxChannelNum = 1
            elif (IDN.find('Thorlabs') != -1) and IDN.find('PM320'):
                self.pm = PM320(id)
                self.type = 'PM320'
                self.maxChannelNum = 2
            # self.type=re.split(',',IDN[:-1])[1]

            self.__setLineFrequency()
        except Exception as e:
            raise DeviceException('', e)

            # thorlabs   serial


    def reset(self):
        try:
            return self.pm.rest()
        except Exception as e:
            raise DeviceException('', e)

    def __setLineFrequency(self):

        try:
            return self.pm.setLineFrequency()
        except Exception as e:
            raise DeviceException('', e)

    def getIdentity(self):
        try:
            return self.pm.getIdentity()
        except Exception as e:
            raise DeviceException('', e)

    def getSensorInfo(self):
        try:
            si = self.pm.getSensorInfo()
            # sis=re.split(',',si[:-1])
            # print(sis)
            # sibin=bin(int(sis[5]))
            # if sibin＆(1<<5)
            return si
        except Exception as e:
            raise DeviceException('', e)
            # self.rm.query('SYSTem:SENSor:IDN?')

    def getWavelength(self, channel):

        if channel in range(1, self.maxChannelNum + 1):
            try:
                return self.pm.getWavelength()
            except Exception as e:
                raise DeviceException('', e)
        else:
            raise DeviceException('Channel out of range')

    def setWavelength(self, channel, wavelength):
        if channel in range(1, self.maxChannelNum + 1):
            try:
                return self.pm.setWavelength(wavelength)
            except Exception as e:
                raise DeviceException('', e)
        else:
            raise DeviceException('Channel out of range')

    def isAutoRange(self, channel):
        if channel in range(1, self.maxChannelNum + 1):
            try:
                return self.pm.isAutoRange()
            except Exception as e:
                raise DeviceException('', e)
        else:
            raise DeviceException('Channel out of range')

    def getMeasureRange(self, channel):

        if channel in range(1, self.maxChannelNum + 1):
            try:
                return self.pm.getMeasureRange_at_W()
            except Exception as e:
                raise DeviceException('', e)
        else:
            raise DeviceException('Channel out of range')

    def setMeasureRange(self, channel, Range):
        if channel in range(1, self.maxChannelNum + 1):
            try:
                self.pm.setMeasureRange_at_W(Range)
            except Exception as e:
                raise DeviceException('', e)
        else:
            raise DeviceException('Channel out of range')

    def onAutoRange(self, channel):
        if channel in range(1, self.maxChannelNum + 1):
            try:
                self.pm.setAutoRange(1)
            except Exception as e:
                raise DeviceException('', e)
        else:
            raise DeviceException('Channel out of range')
    def offAutoRange(self,channel):
        if channel in range(1, self.maxChannelNum + 1):
            try:
                self.pm.setAutoRange(0)
            except Exception as e:
                raise DeviceException('', e)
        else:
            raise DeviceException('Channel out of range')
    def measure(self, channel, averaging=1):
        if channel in range(1, self.maxChannelNum + 1):
            try:
                if averaging != 1:
                    self.setAveragingRate(channel,averaging)
                return float(self.pm.measure())
            except Exception as e:
                raise DeviceException('', e)
        else:
            raise DeviceException('Channel out of range')

    def Beeper(self):
        try:
            return self.pm.Beeper()
        except Exception as e:
            raise DeviceException('', e)

    def setBeamDiameter(self, channel, diameter):
        if channel in range(1, self.maxChannelNum + 1):
            try:
                self.pm.setbeamdiameter(diameter)
            except Exception as e:
                raise DeviceException('', e)
        else:
            raise DeviceException('Channel out of range')

            # def setdefaultbeamdiameter(self):
            #   self.pm.setdefaultbeamdiameter()

    def getBeamDiameter(self, channel):
        if channel in range(1, self.maxChannelNum + 1):
            try:
                return self.pm.getbeamdiameter()
            except Exception as e:
                raise DeviceException('', e)
        else:
            raise DeviceException('Channel out of range')

    # filter on/off
    def getFilterStatus(self, channel):
        if channel in range(1, self.maxChannelNum + 1):
            try:
                return  self.pm.getbandwidth()
            except Exception as e:
                raise DeviceException('', e)
        else:
            raise DeviceException('Channel out of range')

    def onBandWidthFilter(self, channel):

        if channel in range(1, self.maxChannelNum + 1):
            try:
                self.pm.onBandwidthFilter()
            except Exception as e:
                raise DeviceException('', e)
        else:
            raise DeviceException('Channel out of range')

    def offBandWidthFilter(self, channel):

        if channel in range(1, self.maxChannelNum + 1):
            try:
                self.pm.offBandwidthFilter()
            except Exception as e:
                raise DeviceException('', e)
        else:
            raise DeviceException('Channel out of range')


        # measure

    def setAveragingRate(self, channel, rate):

        if channel in range(1, self.maxChannelNum + 1):
            try:
                self.pm.setAveragingRate(rate)
            except Exception as e:
                raise DeviceException('', e)
        else:
            raise DeviceException('Channel out of range')

    def getAveragingRate(self, channel):

        if channel in range(1, self.maxChannelNum + 1):
            try:
                return self.pm.getAveragingRate()
            except Exception as e:
                raise DeviceException('', e)
        else:
            raise DeviceException('Channel out of range')


def init_PM():
    rm = visa.ResourceManager()
    instIDs = rm.list_resources()
    # choose=int(input("Choose your instrument(begin with 1): "))
    choose = 1
    pmA = PM(instIDs[choose - 1])

    print(pmA.type)
    #pmA.Beeper()
    print(pmA.measure(1,3000))
    print(pmA.getIdentity())
    print(pmA.getSensorInfo())
    print(pmA.getAveragingRate(1))
    pmA.onBandWidthFilter(1)
    print(pmA.getFilterStatus(1))
    pmA.offBandWidthFilter(1)
    print(pmA.getFilterStatus(1))
    pmA.setBeamDiameter(1,1)
    print(pmA.getBeamDiameter(1))
    pmA.setWavelength(1,800)
    print(pmA.getWavelength(1))
    pmA.onAutoRange(1)
    print(pmA.isAutoRange(1))
    pmA.setMeasureRange(1,2)
    print(pmA.getMeasureRange(1))

init_PM()
