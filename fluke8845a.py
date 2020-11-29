import telnetlib


class Fluke8845A:
    def __init__(self, ip, port=3490):
        self.ip = ip
        self.port = port
        self.inst = telnetlib.Telnet(ip, port)
        self.write('SYSTem:REMote')

    def reset(self):
        self.write('*RST')

    def id(self):
        return self.query("*IDN?")

    def dc_voltage(self, digit_filter=True):
        if digit_filter:
            self.write('SENSe:VOLTage:DC:FILTer:DIGItal:STATe on')
        return float(self.query('MEASure:VOLTage:DC?'))

    def ac_voltage(self):
        return float(self.query('MEASure:VOLTage:AC?'))

    def dc_current(self, digit_filter=True):
        if digit_filter:
            self.write('SENSe:CURRent:DC:FILTer:DIGItal:STATe on')
        return float(self.query('MEASure:CURRent:DC?'))

    def ac_current(self):
        return float(self.query('MEASure:CURRent:AC?'))

    def resistance(self, digit_filter=True):
        if digit_filter:
            self.write('SENSe:RESistance:FILTer:DIGItal:STATe on')
        ret = self.query('Measure:RESistance?')
        if ret is None:
            return None
        return float(ret)

    def write(self, cmd: str):
        if cmd[-1] != '\n':
            cmd += '\n'
        self.inst.write(bytearray(cmd, encoding='utf-8'))

    def read(self):
        ret = self.inst.read_until(b'\n', timeout=1.).decode('utf-8')
        if len(ret) < 1:
            return None
        while ret[-1] == ('\n' or '\r'):
            ret = ret[:-1]
        return ret

    def query(self, cmd: str):
        self.write(cmd)
        return self.read()


def main():
    import sys
    if 1 < len(sys.argv):
        ip = sys.argv[1]
    else:
        ip = input('Please input the ip address (e.g. 192.168.1.100) > ')
    port = 3490
    if 2 < len(sys.argv):
        port = int(sys.argv[2])

    dmm = Fluke8845A(ip, port)
    print(dmm.id())
    print(dmm.dc_voltage())
    print(dmm.dc_current())
    print(dmm.resistance())


if __name__ == '__main__':
    main()
