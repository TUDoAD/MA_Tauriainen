import serial as ser
import time

# This class controls the Arduino (LDR and presure sensors) vial serial connection
class Arduino_Control():
    # The __init__ method initializes the serial connection with the Arduino
    def __init__(self):                                                                              
        self.Arduino = ser.Serial("COM4", 230400, timeout=1) # Define serial port, baudrate, timeout (to increase measureing speed of acds, decrease timeout in Arduino IDE)
        if self.Arduino.is_open:
            print("Serial port for Arduino has opened.")
        time.sleep(1)

    # Methods to control each LED connected to the Arduino
    def Write_LED1(self, red, green, blue):
        value_string = str(red)+str(green)+str(blue)
        command_string = "LED1" + value_string
        command_string = command_string.encode("ASCII")
        self.Arduino.write(command_string)
        string = self.Arduino.readline()

    def Write_LED2(self, red, green, blue):
        value_string = str(red)+str(green)+str(blue)
        command_string = "LED2" + value_string
        command_string = command_string.encode("ASCII")
        self.Arduino.write(command_string)
        string = self.Arduino.readline()
        # print(string)

    def Write_LED3(self, red, green, blue):
        value_string = str(red)+str(green)+str(blue)
        command_string = "LED3" + value_string
        command_string = command_string.encode("ASCII")
        self.Arduino.write(command_string)
        string = self.Arduino.readline()
        # print(string)

    def Write_LED4(self, red, green, blue):
        value_string = str(red)+str(green)+str(blue)
        command_string = "LED4" + value_string
        command_string = command_string.encode("ASCII")
        self.Arduino.write(command_string)
        string = self.Arduino.readline()
        # print(string)

    def Write_LED5(self, red, green, blue):
        value_string = str(red)+str(green)+str(blue)
        command_string = "LED5" + value_string
        command_string = command_string.encode("ASCII")
        self.Arduino.write(command_string)
        string = self.Arduino.readline()
        # print(string)

    def Write_LED6(self, red, green, blue):
        value_string = str(red)+str(green)+str(blue)
        command_string = "LED6" + value_string
        command_string = command_string.encode("ASCII")
        self.Arduino.write(command_string)
        string = self.Arduino.readline()
        # print(string)

    def Write_LED7(self, red, green, blue):
        value_string = str(red)+str(green)+str(blue)
        command_string = "LED7" + value_string
        command_string = command_string.encode("ASCII")
        self.Arduino.write(command_string)
        string = self.Arduino.readline()
        # print(string)   

    # Methods to read analog values from the Arduino's Analog to Digital Converter (ADC)
    def read_adc0(self):
        command_string = "ADC0\n"
        command_string = command_string.encode("ASCII")
        self.Arduino.write(command_string)
        return_string = self.Arduino.readline().decode()
        return_string = return_string[:-2]
        return return_string
    
    def read_adc1(self):
        command_string = "ADC1\n"
        command_string = command_string.encode("ASCII")
        self.Arduino.write(command_string)
        return_string = self.Arduino.readline().decode()
        return_string = return_string[:-2]
        return return_string
    
    def read_adc2(self):
        command_string = "ADC2\n"
        command_string = command_string.encode("ASCII")
        self.Arduino.write(command_string)
        return_string = self.Arduino.readline().decode()
        return_string = return_string[:-2]
        return return_string
    
    def read_adc3(self):
        command_string = "ADC3\n"
        command_string = command_string.encode("ASCII")
        self.Arduino.write(command_string)
        return_string = self.Arduino.readline().decode()
        return_string = return_string[:-2]
        return return_string
    
    def read_pressure(self):
        self.Arduino.write(b'PRES\n')
        time.sleep(0.2)  # Wait a bit for the Arduino to process and respond
        # Read the response from the Arduino
        response = self.Arduino.readline().decode('utf-8').strip()
        pressure_value = float(response)
        return pressure_value
    
# Method closes the serial connection with the Arduino
    def close_connection(self):
        self.Arduino.close()
        print("Serial port for Arduino has closed.")

# Test program
if __name__ == "__main__":
    arduino_control = Arduino_Control()

    # LED1
    arduino_control.Write_LED1(1,0,0)
    time.sleep(2)
    arduino_control.Write_LED1(0,1,0)
    time.sleep(2)
    arduino_control.Write_LED1(0,0,1)
    time.sleep(2)
    arduino_control.Write_LED1(0,0,0)
    time.sleep(2)
    # LED2
    arduino_control.Write_LED2(1,0,0)
    time.sleep(2)
    arduino_control.Write_LED2(0,1,0)
    time.sleep(2)
    arduino_control.Write_LED2(0,0,1)
    time.sleep(2)
    arduino_control.Write_LED2(0,0,0)
    time.sleep(2)
    # LED3
    arduino_control.Write_LED3(1,0,0)
    time.sleep(2)
    arduino_control.Write_LED3(0,1,0)
    time.sleep(2)
    arduino_control.Write_LED3(0,0,1)
    time.sleep(2)
    arduino_control.Write_LED3(0,0,0)
    time.sleep(2)
    # LED4
    arduino_control.Write_LED4(1,0,0)
    time.sleep(2)
    arduino_control.Write_LED4(0,1,0)
    time.sleep(2)
    arduino_control.Write_LED4(0,0,1)
    time.sleep(2)
    arduino_control.Write_LED4(0,0,0)
    time.sleep(2)
    # LED5
    arduino_control.Write_LED5(1,0,0)
    time.sleep(2)
    arduino_control.Write_LED5(0,1,0)
    time.sleep(2)
    arduino_control.Write_LED5(0,0,1)
    time.sleep(2)
    arduino_control.Write_LED5(0,0,0)
    time.sleep(2)
    # LED6
    arduino_control.Write_LED6(1,0,0)
    time.sleep(2)
    arduino_control.Write_LED6(0,1,0)
    time.sleep(2)
    arduino_control.Write_LED6(0,0,1)
    time.sleep(2)
    arduino_control.Write_LED6(0,0,0)
    time.sleep(2)
    # LED7
    arduino_control.Write_LED7(1,0,0)
    time.sleep(2)
    arduino_control.Write_LED7(0,1,0)
    time.sleep(2)
    arduino_control.Write_LED7(0,0,1)
    time.sleep(2)
    arduino_control.Write_LED7(0,0,0)
    time.sleep(2)

    # ADC0
    adc0 = arduino_control.read_adc0()
    print("ADC0 =", adc0)
    time.sleep(2)
    # ADC1
    adc1 = arduino_control.read_adc1()
    print("ADC1 =", adc1)
    time.sleep(2)
    # ADC2
    adc2 = arduino_control.read_adc2()
    print("ADC2 =", adc2)
    time.sleep(2)
    # ADC3
    adc3 = arduino_control.read_adc3()
    print("ADC3 =", adc3)
    time.sleep(2)


    arduino_control.close_connection()