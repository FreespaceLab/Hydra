__author__ = 'Hwaipy'

from Hydra import Session, Message

class InstrumentServer:
    def __init__(self, name, address=('localhost', 20102), services=[], invokers=[]):
        self.name = name
        self.address = address
        self.services = services
        self.invokers = invokers

    def start(self, async=False):
        self.session = Session(self.name, self.address, self.services, self.invokers)
        self.session.start(async)

    def sendMessageLaser(self, messae):
        raise

    def __messageInvoker__(self, message):
        print(message)
        assert message.type == Message.Type.Request
        command = message.command
        if message.content.__contains__('Arguments'):
            arguments = message.content.__getitem__('Arguments')
            if arguments == None:
                arguments = []
            elif not isinstance(arguments, list):
                arguments = [arguments]
        else:
            arguments = []
        print('arg: {}'.format(arguments))
        try:
            self.invoker.__getattribute__(command)()
        except Exception as ex:
            print(ex)

class DeviceException(BaseException):
    def __init__(self, msg, exception=None):
        self.message = msg
        self.exception = exception

if __name__ == '__main__':
    class TestDevice:
        def __init__(self):
            pass

        def identity(self):
            return 'Hydra,TestDevice,1.0.0,2015'


    iis = InstrumentServer('InvokableInstrumentServerTest', address=('172.16.60.199', 20102), invokers=TestDevice())
    iis.start()
