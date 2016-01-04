__author__ = 'Hwaipy'

from  RemoteInstruments import RemotePowerMeter

__clientName__ = 'PowerMetersMonitor_Hwaipy'
__serverPort__ = 20102
__serverAddress__ = 'localhost'

if __name__ == '__main__':
    print('{} is started.'.format(__clientName__))
    RPM = RemotePowerMeter()
#    session = Session(__clientName__, __serverPort__, __serverAddress__, [], {})
#    session.start(True)

#    while True:
#        time.sleep(1)
#        session.sendMessageLater(Message.createRequest('ReadPowers', {Message.KEY_TARGET: 'VirtualPowerMeter_Hwaipy'}))
