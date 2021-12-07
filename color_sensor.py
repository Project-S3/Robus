import smbus

class ColorSensor:
    def __init__(self, address=0x11):
        self.bus = smbus.SMBus(1)
        self.address = address

    def read_raw(self):
        for _ in range(0, 5):
            try:
                raw_result = self.bus.read_i2c_block_data(self.address, 0, 10)
                connection_ok = True
                break
            except:
                connection_ok = False

        if connection_ok:
            return raw_result
        else:
            print("Error accessing %2X" % self.address)
            return False

    def read(self, trys=5):
        for _ in range(trys):
            raw_result = self.read_raw()
            if raw_result:
                analog_result = [0, 0, 0, 0, 0]
                for i in range(0, 5):
                    high_byte = raw_result[i * 2] << 8
                    low_byte = raw_result[i * 2 + 1]
                    analog_result[i] = high_byte + low_byte
                    if analog_result[i] > 1024:
                        continue
                return analog_result
            else:
                raise IOError("Line follower read error. Please check the wiring.")