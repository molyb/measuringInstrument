import serial
import time


class TakasagoKX100L:
    def __init__(self, com, baudrate, timeout=0.1, target_index=1):
        if baudrate not in (2400, 9600, 38400):
            baudrate = 9600

        if baudrate == 2400:
            self.tx_wait = 0.2
        elif baudrate == 9600:
            self.tx_wait = 0.05
        elif baudrate == 38400:
            self.tx_wait = 0.02
        self.inst = serial.Serial(com, baudrate, timeout=timeout)
        # clear error
        self.write("\n")
        if not self.is_valid_target_index(target_index):
            target_index = 1
        self.change_target(target_index)

    @staticmethod
    def is_valid_target_index(index):
        return 1 <= index <= 50

    def change_target(self, index):
        if not self.is_valid_target_index(index):
            return
        self.write("A" + str(index))

    def output(self, state: bool):
        self.write("OT" + str(int(state)))

    def voltage(self, voltage: float):
        self.write("OV" + str(voltage))

    def current(self, current: float):
        self.write("OC" + str(current))

    def limit_voltage(self, voltage: float):
        self.write("LV" + str(voltage))

    def limit_current(self, current: float):
        self.write("LC" + str(current))

    def measure_voltage(self):
        # a message example is "12.01V\r\n"
        return float(self.query("TK6").split('V')[0])

    def measure_current(self):
        return float(self.query("TK7").split('A')[0])
        # return self.query("TK7")

    def write(self, cmd: str):
        if cmd[-1] != '\n':
            cmd += '\n'
        self.inst.write(bytearray(cmd, 'utf-8'))
        while 0 < self.inst.out_waiting:
            continue
        time.sleep(self.tx_wait)

    def read(self):
        ret = self.inst.read_until().decode('utf-8')
        if len(ret) < 1:
            return None
        while ret[-1] == ('\n' or '\r'):
            ret = ret[:-1]
        return ret

    def query(self, cmd: str):
        self.write(cmd)
        return self.read()


def main():
    psu = TakasagoKX100L('com9', 38400)

    # psu1 on
    psu.change_target(1)
    psu.limit_voltage(15)
    psu.voltage(12)
    psu.limit_current(3)
    psu.current(2)
    psu.output(True)
    print(psu.measure_voltage())
    print(psu.measure_current())

    # psu2 on
    psu.change_target(2)
    psu.limit_voltage(4)
    psu.voltage(3.3)
    psu.limit_current(2)
    psu.current(1)
    psu.output(True)
    print(psu.measure_voltage())
    print(psu.measure_current())

    time.sleep(2)

    # off
    psu.change_target(1)
    psu.output(False)
    psu.change_target(2)
    psu.output(False)


if __name__ == '__main__':
    main()
