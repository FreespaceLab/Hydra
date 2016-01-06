__author__ = 'Benli'
__version__ = 'v1.0.20160105'

import visa
from SCPI import SCPI
from InstrumentServers import InstrumentServer,DeviceException
from Utils import SingleThreadProcessor
import math

class IT6322:
    def __init__(self, port):
        try:
            rm = visa.ResourceManager().open_resource(port)
            print(rm)
        except BaseException as e:
            raise DeviceException('Error in open device ID: {}'.format(id), e)
        stp = SingleThreadProcessor()
        def stpQuery(*args):
            return stp.invokeAndWait(rm.query, *args)
        def stpWrite(*args):
            stp.invokeLater(rm.write, *args)
        self.scpi = SCPI(stpQuery, stpWrite)
        idns = self.getIdentity()
        if (idns[0] == 'ITECH Ltd.') and (idns[1] == 'IT6322'):
            self.serialNumber = idns[2]
            self.version = idns[3]
            self.maxChannelNum = 3
        else:
            raise DeviceException('Identity {} not recognized.'.format(idns))
        self.__remote()
        self.voltageSetpoints = self.getVoltageSetpoints()
        self.currentLimits = self.getCurrentLimits()
        self.outputStatuses = self.getOutputStatuses()

    def getIdentity(self):
        try:
            idn = self.scpi._IDN.query()
            if idn is None:
                return [''] * 4
            if len(idn) is 0:
                return [''] * 4
            idns = idn.split(',')
            idns = [idn.strip(' ') for idn in idns]
            while len(idns) < 4:
                idns.append('')
            return idns[:4]
        except Exception as e:
            raise DeviceException('Error in getIdentity', e)

    def getVersion(self):
        return self.scpi.SYSTem.VERSion.query()

    def beeper(self):
        try:
            self.scpi.SYSTem.BEEPer.write()
        except Exception as e:
            raise DeviceException('Error in beeper', e)

    def measureVoltages(self):
        try:
            voltageString = self.scpi.MEAS.VOLT.ALL.query().split(', ')
            voltages = [float(vs) for vs in voltageString]
            return voltages
        except Exception as e:
            raise DeviceException('Error in measureVoltages', e)

    def measureCurrents(self):
        try:
            currentString = self.scpi.MEAS.CURR.ALL.query().split(', ')
            currents = [float(vs) for vs in currentString]
            return currents
        except Exception as e:
            raise DeviceException('Error in measureCurrents', e)

    def getVoltageSetpoints(self):
        try:
            vs = self.scpi.APP.VOLT.query()
            vs = vs.split(', ')
            self.voltageSetpoints = [float(v) for v in vs]
            return self.voltageSetpoints
        except Exception as e:
            raise DeviceException('Error in getVoltages')

    def getCurrentLimits(self):
        try:
            cs = self.scpi.APP.CURR.query()
            cs = cs.split(', ')
            self.currentLimits = [float(v) for v in cs]
            return self.currentLimits
        except Exception as e:
            raise DeviceException('Error in getCurrentLimit')

    def setVoltages(self, voltages):
        if len(voltages) is not self.maxChannelNum:
            raise DeviceException('Length of voltages do not match the channel number.')
        try:
            outputCodeString = ['{}'.format(v) for v in voltages]
            outputCode = ', '.join(outputCodeString)
            self.scpi.APP.VOLT.write(outputCode)
            setted = self.getVoltageSetpoints()
            same = [math.fabs(voltages[i]-setted[i])<0.001  for i in range(self.maxChannelNum)]
        except Exception as e:
            raise DeviceException('Error in setVoltages')
        if sum(same) is not self.maxChannelNum:
            raise DeviceException('Voltage out of range.')

    def setVoltage(self, channel, voltage):
        self.__checkChannel(channel)
        voltages = self.voltageSetpoints.copy()
        voltages[channel] = voltage
        self.setVoltages(voltages)

    def setCurrentLimits(self, currents):
        if len(currents) is not self.maxChannelNum:
            raise DeviceException('Length of currents do not match the channel number.')
        try:
            outputCodeString = ['{}'.format(v) for v in currents]
            outputCode = ', '.join(outputCodeString)
            self.scpi.APP.CURR.write(outputCode)
            setted = self.getCurrentLimits()
            same = [math.fabs(currents[i]-setted[i])<0.001  for i in range(self.maxChannelNum)]
        except Exception as e:
            raise DeviceException('Error in setCurrents')
        if sum(same) is not self.maxChannelNum:
            raise DeviceException('Current out of range.')

    def setCurrentLimit(self, channel, currentLimit):
        self.__checkChannel(channel)
        currentLimits = self.currentLimits.copy()
        currentLimits[channel] = currentLimit
        self.setCurrentLimits(currentLimits)

    def getOutputStatuses(self):
        try:
            os = self.scpi.APP.OUT.query()
            os = os.split(', ')
            self.outputStatuses = [o == '1' for o in os]
            return self.outputStatuses
        except Exception as e:
            raise DeviceException('Error in setVoltages')

    def setOutputStatuses(self, outputStatuses):
        if len(outputStatuses) is not self.maxChannelNum:
            raise DeviceException('Length of outputStatuses do not match the channel number.')
        try:
            outputCodeString = ['{}'.format(1 if v else 0) for v in outputStatuses]
            outputCode = ', '.join(outputCodeString)
            self.scpi.APP.OUT.write(outputCode)
            setted = self.getOutputStatuses()
            same = [outputStatuses[i]==setted[i] for i in range(self.maxChannelNum)]
        except Exception as e:
            raise DeviceException('Error in setCurrents')
        if sum(same) is not self.maxChannelNum:
            raise DeviceException('OutputStatus error.')

    def setOutputStatus(self, channel, outputStatus):
        self.__checkChannel(channel)
        outputStatuses = self.outputStatuses.copy()
        outputStatuses[channel] = outputStatus
        self.setOutputStatuses(outputStatuses)

    def reset(self):
        try:
            self.scpi._RST.write()
        except Exception as e:
            raise DeviceException('', e)

    def __remote(self):
        try:
            return self.scpi.SYSTem.REMote.write()
        except Exception as e:
            raise DeviceException('', e)

    def __checkChannel(self, channel):
        if channel>=0 and channel < self.maxChannelNum:
            return
        raise DeviceException('Channel {} out of range.'.format(channel))

if __name__ == '__main__':
    print('BKPrecision_IT6322')
    pm = IT6322('ASRL11::INSTR')
    #pm.setCurrentLimits([1, 1, 1])
    #pm.setOutputStatuses([True]*3)
    import time
    pm.setVoltages([24, 0.15, 0.475])
