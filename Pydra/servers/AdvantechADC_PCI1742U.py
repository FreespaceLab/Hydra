__author__ = 'Hwaipy'
import sys
import jpype
from InstrumentServers import InstrumentServer
import queue

class AdvantechADC_PCI1742U:
    def __init__(self):
        self.queue = queue.Queue()
        def controlJPype():
            jpype.startJVM(jpype.getDefaultJVMPath(),'-Djava.class.path=..\\Jydra\\AdvantechADCPCI\\build\\classes\\;..\\Jydra\\AdvantechADCPCI\\lib\\jna-3.0.9.jar')
            deviceManager = jpype.JClass('com.hwaipy.unifieddeviceinterface.adc.advantech.AdvantechADCDeviceManager').getManager()
            jpypeObject = deviceManager.getDeviceList()[0]
            jpypeObject.open()
            while True:
                action = self.queue.get()
                action(jpypeObject)
        threading._start_new_thread(controlJPype,())

    def readAnalogVoltage(self,channel):
        if channel>=0 and channel<16:
            try:
                semaphore = threading.Semaphore(0)
                returnValue = []
                def action(jpypeObject):
                    returnValue.append(jpypeObject.analogIOReadVoltage(channel))
                    semaphore.release()
                self.queue.put(action)
                semaphore.acquire()
                return returnValue[0]
            except Exception as e:
                print(e)
        else:
            raise

def runAsService():
    #jpype.startJVM(jpype.getDefaultJVMPath(),'-Djava.class.path=E:\\Coding\\Examples\\Programs\\CODE\\AdvantechADCPCI\\build\\classes\\;E:\\Coding\\Examples\\Programs\\CODE\\Lib\\Native\\jna-3.0.9.jar')
    #deviceManager = jpype.JClass('com.hwaipy.unifieddeviceinterface.adc.advantech.AdvantechADCDeviceManager').getManager()
    #device0 = deviceManager.getDeviceList()[0]
    #device0.open()
    device = AdvantechADC_PCI1742U()
    server = InstrumentServer('R22_AdvantechADC_PCI1742U',address=('172.16.60.199',20102),invokers=[device])
    server.start()

if __name__ == '__main__':
    import threading
    import time
    threading._start_new_thread(runAsService(), ())
    time.sleep(1000)

    runAsService()
    try:
        jpype.startJVM(jpype.getDefaultJVMPath(),
                       '-Djava.class.path=E:\\Coding\\Examples\\Programs\\CODE\\AdvantechADCPCI\\build\\classes\\;E:\\Coding\\Examples\\Programs\\CODE\\Lib\\Native\\jna-3.0.9.jar')
        deviceManager = jpype.JClass('com.hwaipy.unifieddeviceinterface.adc.advantech.AdvantechADCDeviceManager').getManager()
        deviceList = deviceManager.getDeviceList()
        device0 = deviceList[0]
        device0.open()
        print(device0.analogIOReadVoltage(0))
        print(device0.analogIOReadVoltage(2))
        device0.close()
        sys.exit(0)
    except jpype.JavaException as e:
        print(e.message())
        print(e.stacktrace())