from time import sleep


class QwiicKeypad:
    default_I2C_address = 0x4B    
    RegisterMap = {
        "KEYPAD_ID": 0x00,
        "KEYPAD_VERSION1": 0x01,
        "KEYPAD_VERSION2": 0x02,
        "KEYPAD_BUTTON": 0x03,
        "KEYPAD_TIME_MSB": 0x04,
        "KEYPAD_TIME_LSB": 0x05,
        "KEYPAD_UPDATE_FIFO": 0x06,
        "KEYPAD_CHANGE_ADDRESS": 0x07
    }

    def __init__(self, qwiic: I2C, address: int = default_I2C_address) -> None:
        self._device_address: int = address
        self.i2c: I2C = qwiic

    def begin(self) -> None:
        return self.is_connected()

    def is_connected(self) -> bool:
        result: bytes = self.i2c.readfrom(self._device_address, 1)
        return True if result else False

    def get_version(self) -> str:
        version_prefix: bytes = self._read_register(self.RegisterMap.get("KEYPAD_VERSION1"))
        version_suffix: bytes = self._read_register(self.RegisterMap.get("KEYPAD_VERSION2"))
        integer_prefix: int = int.from_bytes(version_prefix, "little")
        integer_suffix: int = int.from_bytes(version_suffix, "little")
        return "v" + str(integer_prefix) + "." + str(integer_suffix)

    def get_button(self) -> str:
        button_bytes: bytes = self._read_register(self.RegisterMap.get("KEYPAD_BUTTON"))
        button_char: str = chr(int.from_bytes(button_bytes, "little"))
        return button_char

    def get_time_since_pressed(self) -> int:
        MSB_bytes: bytes = self._read_register(self.RegisterMap.get("KEYPAD_TIME_MSB"))
        LSB_bytes: bytes = self._read_register(self.RegisterMap.get("KEYPAD_TIME_LSB"))
        MSB: int = int.from_bytes(MSB_bytes, "little")
        LSB: int = int.from_bytes(LSB_bytes, "little")
        
        time_since_pressed: int = MSB << 8
        time_since_pressed |= LSB
        
        return time_since_pressed

    def update_fifo(self) -> None:
        self._write_register(self.RegisterMap.get("KEYPAD_UPDATE_FIFO"), 0x01)

    def set_i2c_address(self, new_address: int) -> None:
        if new_address < 8 or new_address > 118:
            raise Exception("Address outside 8-119 range")
        
        is_applied: bool = self._write_register(self.RegisterMap.get("KEYPAD_CHANGE_ADDRESS"), new_address)
        sleep(100)
        
        active_i2c_slaves = self.i2c.scan()

        if is_applied and new_address in active_i2c_slaves:
            self._device_address = new_address
            can_connect: bool = self.is_connected()
            if not can_connect:
                raise Exception("Address is changed, however, connection cannot be established.")
        else:
            raise Exception("Address change is failured.")
            

    def _write_register(self, register_address: int, value: int) -> bool:
        value_in_bytes: bytes = self.convert_uint8_to_bytes(value)
        ACKs_recieved = self.i2c.writeto_mem(self._device_address, register_address, value_in_bytes)
        return True if ACKs_recieved else False

    def _read_register(self, register_address: int) -> int:
        register_in_bytes: bytes = self.convert_uint8_to_bytes(register_address)
        ACKs_recieved = self.i2c.writeto(self._device_address, register_in_bytes)
        
        if ACKs_recieved:
            result: bytes = self.i2c.readfrom(self._device_address, 1)
            return result

        raise Exception("There was no ACK response.")

    @staticmethod
    def convert_uint8_to_bytes(int_value: int) -> bytes:
        return int_value.to_bytes(1, "little")
