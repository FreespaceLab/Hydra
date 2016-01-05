__author__ = 'Hwaipy'

from Hydra import Session, Message, ProtocolException
import time


class RemoteInstrument:
    def __init__(self, name, targetName, address=('localhost', 20102), invokers=[]):
        self.name = name
        self.targetName = targetName
        self.address = address
        self.invokers = invokers

    def start(self, async=False):
        self.session = Session(self.name, self.address, [], self.invokers)
        self.session.start(async)

    def __request__(self, message, async=False):
        # TODO sync only for now
        if not isinstance(message, Message):
            raise RuntimeError('Not a message.')
        if async:
            raise
        else:
            response = self.session.request(message, async)
            type = response.getType()
            if type is Message.Type.Response:
                return response.Result
            elif type is Message.Type.Error:
                raise ProtocolException(response.ErrorMessage, message)
            else:
                print('Wrong message: {}'.format(response))

    def __getattr__(self, item):
        def invoke(*args, **kwargs):
            args = [arg for arg in args]
            kwargs['Arguments'] = args
            kwargs['Target'] = self.targetName
            message = Message.creator.__getattr__(item)(**kwargs)
            return self.__request__(message)

        return invoke


if __name__ == '__main__':
    ri = RemoteInstrument('RemoteInstrumentTest3', 'R22_AdvantechADC_PCI1742U', address=('127.0.0.1', 20102))
    ri.start(async=True)
    #    print(ri.identity('arg1', 20, 'arg3', ['l1', 2, 'l3'], time=100))
    #print(ri.readAnalogVoltage(2))

    time.sleep(10)

    time.sleep(2000)
