import visa

class PM320:
    def __init__(self,id):
        self.id = id
        self.rm = visa.ResourceManager().open_resource(id)

    def getIdentity(self):
        return self.rm.query('*IDN?')

    def getWavelength(self,channel):
        wl = self.rm.query(':WAVEL{}:VAL?'.format(channel))
        return float(wl)

    def setWavelength(self,channel,wavelength):
        self.rm.write(':WAVEL{}:VAL {}'.format(channel,wavelength))

    def setAutoRange(self,channel):
        self.rm.write(':PRANGE{} AUTO'.format(channel))

    def measure(self,channel):
        return float(self.rm.query(':POW{}:VAL?'.format(channel)))
