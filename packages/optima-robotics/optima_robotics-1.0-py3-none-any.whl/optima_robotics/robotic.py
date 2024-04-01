import serial

class Arduino:
    """
        A class representing an Arduino board.

        Args:
            port (str): The port name where Arduino is connected.
            baudrate (int, optional): The baud rate for serial communication. Default is 9600.
        """
    def __init__(self, port, baudrate=9600):
        """
                Initialize the Arduino object.

                Args:
                    port (str): The port name where Arduino is connected.
                    baudrate (int, optional): The baud rate for serial communication. Default is 9600.
                """
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None

    def connect(self):
        """
               Connect to the Arduino board.
               """
        try:
            self.serial_connection = serial.Serial(self.port, self.baudrate)
            print("Arduino connected.")
        except serial.SerialException as e:
            print(f"Failed to connect to Arduino: {e}")

    def disconnect(self):
        """
                Disconnect from the Arduino board.
        """
        if self.serial_connection:
            self.serial_connection.close()
            print("Arduino disconnected.")
        else:
            print("Arduino is not connected.")

    def turn_on_led(self, pin):
        """
                Turn on an LED connected to a specific pin.

                Args:
                    pin (int): The pin number of the LED.
        """
        if self.serial_connection:
            command = f"on {pin}\n"
            self.serial_connection.write(command.encode())
            print(f"Turned on LED on pin {pin}.")
        else:
            print("Arduino is not connected.")

    def turn_off_led(self, pin):
        """
                Turn off an LED connected to a specific pin.

                Args:
                    pin (int): The pin number of the LED.
        """
        if self.serial_connection:
            command = f"off {pin}\n"
            self.serial_connection.write(command.encode())
            print(f"Turned off LED on pin {pin}.")
        else:
            print("Arduino is not connected.")
