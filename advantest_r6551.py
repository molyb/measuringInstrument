import ar488
import time

# up to 40 characters (excluding block delimiters) can be set at a time.
# R6551 Instruction Manual P. 63 5.6 Listener Specification


class AdvantestR6551(ar488.Ar488):
    def __init__(self, com, target_index=1, rx_timeout=3, tx_wait=0.05, eol='\r\n', wait4measure=0.):
        self.wait4measure = wait4measure
        super().__init__(com, target_index, rx_timeout, tx_wait, '\r\n')

    def dc_voltage(self):
        return self._request('F1,R0,M1,PR2,RE5', 'DV')

    def ac_voltage(self):
        return self._request('F2,R0,M1,PR2,RE5', 'AV')

    def dc_current(self):
        return self._request('F5,R0,M1,PR2,RE5', 'DI')

    def ac_current(self):
        return self._request('F6,R0,M1,PR2,RE5', 'AI')

    def resistance(self):
        return self._request('F3,R0,M1,PR2,RE5', 'R')

    def _request(self, cmd: str, header: str):
        self.write(cmd)
        time.sleep(self.wait4measure)
        ret = self.query('E')
        l_head = len(header)
        if ret[:l_head] == header:
            return float(ret[l_head:])
        return None


if __name__ == '__main__':
    dmm = AdvantestR6551('com3', rx_timeout=3, tx_wait=0.05)
    for i in range(3):
        print('dv', dmm.dc_voltage())
        print('av', dmm.ac_voltage())
        print('r', dmm.resistance())
        print('di', dmm.dc_current())
        print('ai', dmm.ac_current())
