# Sparkfun Qwiic Keypad for MicroPython
This library is an direct implementation of Sparkfun's own API.

|                               | Description                                               |
| ----------------------------- | --------------------------------------------------------- |
| **.begin()**                  | It only returns if the I2C slave is connected.            |
| **.is_connected()**           | Returns True if I2C slave responses.                      |
| **.get_version()**            | Returns a string contains version numbers such as `v1.0`. |
| **.get_button()**             | Returns last pressed button as char-string.               |
| **.get_time_since_pressed()** | Returns milliseconds after last pressed button.           |
| **.update_fifo()**            | It is needed to run before `.get_button()` method.        |
| **.set_i2c_address()**        | Changes the slave address of the device.                  |

### Example

```python
from time import sleep
from machine import I2C

from qwiic_keypad import QwiicKeypad

qwiic_I2C = I2C(10, 11)
keypad = QwiicKeypad(qwiic_I2C)
    
if keypad.is_connected():
    keypad.update_fifo()
    button = keypad.get_button()
    charButton = chr(int.from_bytes(button, "little"))
    print(charButton)

    sleep(0.25)
```

You can find other examples in `examples/` directory.

### License

It is under MIT license, check out the [LICENSE](./LICENSE) file.
