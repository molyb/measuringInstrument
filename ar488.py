import serial
import time

# https://github.com/Twilight-Logic/AR488


class Ar488:
    def __init__(self, com, target_index=1, rx_timeout=3, tx_wait=0.05, eol='\r\n'):
        baudrate = 115200
        self.tx_wait = tx_wait
        self.eol = eol
        self.inst = serial.Serial(com, baudrate, timeout=rx_timeout)
        # ポートオープン直後に通信を開始すると通信エラーになってしまうのでWait
        time.sleep(2)
        self.inst.reset_input_buffer()
        # ++readコマンドを送らなくても応答が帰ってくるようにする
        self.write('++auto 1')

        if not self.is_valid_target_index(target_index):
            target_index = 1
        self.change_target(target_index)

    @staticmethod
    def is_valid_target_index(index):
        return 1 <= index <= 29

    def change_target(self, index):
        if not self.is_valid_target_index(index):
            return
        self.write("++addr " + str(index))

    def write(self, cmd: str):
        cmd = cmd.rstrip('\n')
        cmd = cmd.rstrip('\r')
        cmd += self.eol
        self.inst.write(bytearray(cmd, 'utf-8'))
        time.sleep(self.tx_wait)

    def read(self):
        ret = self.inst.read_until().decode('utf-8')
        if len(ret) < 1:
            return None
        ret = ret.rstrip('\n')
        ret = ret.rstrip('\r')
        return ret

    def query(self, cmd: str):
        self.write(cmd)
        return self.read()
