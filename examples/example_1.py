from time import sleep
from machine import I2C

from qwiic_keypad import QwiicKeypad

I2C_PINS = {
    "SCL": 10,
    "SDA": 11
}

if __name__ == "__main__":
    qwiic_I2C = I2C(I2C_PINS.get("SCL"), I2C_PINS.get("SDA"))
    keypad = QwiicKeypad(qwiic_I2C)

    print("\nSparkFun Qwiic Keypad | Example 1\n")

    if not keypad.is_connected():
        raise Exception("The Qwiic Keypad device isn't connected to the system. Please check your connection.")

    print(f"Firmware Version: {keypad.get_version()}")
    print("Press a button: * to do a space. # to go to next line.")

    button = 0
    while True:
        # Necessary for keypad to pull button from stack to readable register
        keypad.update_fifo()
        button = keypad.get_button()

        if button == -1:
            print("No keypad detected")
            sleep(1)

        elif button != 0:
            # Get the character version of this char
            charButton = chr(int.from_bytes(button, "little"))
            if charButton == '#':
                print()
            elif charButton == '*':
                print(" ", end="")
            else:
                print(charButton, end="")

        sleep(.25)
