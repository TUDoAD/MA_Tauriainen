#include <Adafruit_ADS1X15.h>

Adafruit_ADS1115 ads;  /* Use this for the 16-bit version */
// Adafruit_ADS1015 ads;     /* Use this for the 12-bit version */


// assign the connections for the different colors of the rgb LEDs to digital pins
int LED_1_blue = 31;
int LED_1_green = 33;
int LED_1_red = 35;   

int LED_2_blue = 39;
int LED_2_green = 41;
int LED_2_red = 43;  

int LED_3_blue = 47;
int LED_3_green = 49;
int LED_3_red = 51;  

int LED_4_blue = 30;
int LED_4_green = 32;
int LED_4_red = 34;

int LED_5_blue = 38;
int LED_5_green = 40;
int LED_5_red = 42;

int LED_6_blue = 46;
int LED_6_green = 48;
int LED_6_red = 50;

int LED_7_blue = 23;
int LED_7_green = 25;
int LED_7_red = 27;

// define the input strings
String full_command = "";
String command = "";
String value = "";
String LED_red_value ="";
String LED_green_value = "";
String LED_blue_value = "";

// save ADCs values as exactly 16-bit integers (-32,768 to +32,768) with int16_t (only int means the integer has at leat 16 bits)
int16_t adc0, adc1, adc2, adc3;

// pressure sensor constants
const int analogInput0 = A0;  // Analog input pin connected to the sensor
const float Va = 5.0;     // Arduino operating voltage (5V)
const float resistor = 250.0; // Resistor value (250 ohms)
const float minCurrent = 0.004;  // Minimum sensor current (4 mA)
const float maxCurrent = 0.02; // Maximum sensor current (20 mA)
const float minPressure = 0.0; // Minimum pressure (0 bar)
const float maxPressure = 4.0; // Maximum pressure (4 bar)

void setup(void)
{
  Serial.begin(230400); // baudrate
  Serial.setTimeout(1); // if this is not used, the standard time out time is used for Serial.readString()
                        // timeout has a big impact on the measurement speed of the adc sensors

// define all the assigned digital pins as outputs so they can supply voltage
  pinMode(LED_1_red, OUTPUT);
  pinMode(LED_1_green, OUTPUT);
  pinMode(LED_1_blue, OUTPUT);

  pinMode(LED_2_red, OUTPUT);
  pinMode(LED_2_green, OUTPUT);
  pinMode(LED_2_blue, OUTPUT);

  pinMode(LED_3_red, OUTPUT);
  pinMode(LED_3_green, OUTPUT);
  pinMode(LED_3_blue, OUTPUT);

  pinMode(LED_4_red, OUTPUT);
  pinMode(LED_4_green, OUTPUT);
  pinMode(LED_4_blue, OUTPUT);

  pinMode(LED_5_red, OUTPUT);
  pinMode(LED_5_green, OUTPUT);
  pinMode(LED_5_blue, OUTPUT);

  pinMode(LED_6_red, OUTPUT);
  pinMode(LED_6_green, OUTPUT);
  pinMode(LED_6_blue, OUTPUT);

  pinMode(LED_7_red, OUTPUT);
  pinMode(LED_7_green, OUTPUT);
  pinMode(LED_7_blue, OUTPUT);

 if (!ads.begin()) {
    Serial.println("Failed to initialize ADS.");
    while (1);
  }
  // ads.setGain(GAIN_TWOTHIRDS);  // 2/3x gain +/- 6.144V  1 bit = 3mV (default)

  ads.setGain(GAIN_ONE);     // 1x gain   +/- 4.096V  1 bit = 2mV
  // ads.setGain(GAIN_TWO);     // 2x gain   +/- 2.048V  1 bit = 1mV
  // ads.setGain(GAIN_FOUR);    // 4x gain   +/- 1.024V  1 bit = 0.5mV
  // ads.setGain(GAIN_EIGHT);   // 8x gain   +/- 0.512V  1 bit = 0.25mV
  // ads.setGain(GAIN_SIXTEEN); // 16x gain  +/- 0.256V  1 bit = 0.125mV
}

void loop(void)
{
if (Serial.available() > 0)
  {
    //full_command = Serial.readStringUntil("X"); //read command e.g. LED1001
    full_command = Serial.readString();
    command = full_command.substring(0,4); //red command until Char 4 e.g. LED1
    value = full_command.substring(4); //read from Char 4 till end e.g. 001

    if (command=="LED1")
    {
      LED_red_value = value.substring(0,1); //read Char 1 e.g. if full_command is LED1100
      LED_green_value = value.substring(1,2); //read Char 2 e.g. if full_command is LED1010
      LED_blue_value = value.substring(2,3); //read Char 3 e.g. if full_command is LED1001
      digitalWrite(LED_1_red,LED_red_value.toInt()); //transfer string with values into integer to turn on/off the LED
      digitalWrite(LED_1_green,LED_green_value.toInt()); //transfer string with values into integer
      digitalWrite(LED_1_blue,LED_blue_value.toInt()); //transfer string with values into integer
    }

    else if (command=="LED2")
    {
      LED_red_value = value.substring(0,1); //read Char 1
      LED_green_value = value.substring(1,2); //read Char 2
      LED_blue_value = value.substring(2,3); //read Char 3
      digitalWrite(LED_2_red,LED_red_value.toInt()); //transfer string with values into integer
      digitalWrite(LED_2_green,LED_green_value.toInt()); //transfer string with values into integer
      digitalWrite(LED_2_blue,LED_blue_value.toInt()); //transfer string with values into integer
    }

    else if (command=="LED3")
    {
      LED_red_value = value.substring(0,1); //read Char 1
      LED_green_value = value.substring(1,2); //read Char 2
      LED_blue_value = value.substring(2,3); //read Char 3
      digitalWrite(LED_3_red,LED_red_value.toInt()); //transfer string with values into integer
      digitalWrite(LED_3_green,LED_green_value.toInt()); //transfer string with values into integer
      digitalWrite(LED_3_blue,LED_blue_value.toInt()); //transfer string with values into integer
    }

    else if (command=="LED4")
    {
      LED_red_value = value.substring(0,1); //read Char 1
      LED_green_value = value.substring(1,2); //read Char 2
      LED_blue_value = value.substring(2,3); //read Char 3
      digitalWrite(LED_4_red,LED_red_value.toInt()); //transfer string with values into integer
      digitalWrite(LED_4_green,LED_green_value.toInt()); //transfer string with values into integer
      digitalWrite(LED_4_blue,LED_blue_value.toInt()); //transfer string with values into integer
    }

    else if (command=="LED5")
    {
      LED_red_value = value.substring(0,1); //read Char 1
      LED_green_value = value.substring(1,2); //read Char 2
      LED_blue_value = value.substring(2,3); //read Char 3
      digitalWrite(LED_5_red,LED_red_value.toInt()); //transfer string with values into integer
      digitalWrite(LED_5_green,LED_green_value.toInt()); //transfer string with values into integer
      digitalWrite(LED_5_blue,LED_blue_value.toInt()); //transfer string with values into integer
    }

    else if (command=="LED6")
    {
      LED_red_value = value.substring(0,1); //read Char 1
      LED_green_value = value.substring(1,2); //read Char 2
      LED_blue_value = value.substring(2,3); //read Char 3
      digitalWrite(LED_6_red,LED_red_value.toInt()); //transfer string with values into integer
      digitalWrite(LED_6_green,LED_green_value.toInt()); //transfer string with values into integer
      digitalWrite(LED_6_blue,LED_blue_value.toInt()); //transfer string with values into integer
    }

    else if (command=="LED7")
    {
      LED_red_value = value.substring(0,1); //read Char 1
      LED_green_value = value.substring(1,2); //read Char 2
      LED_blue_value = value.substring(2,3); //read Char 3
      digitalWrite(LED_7_red,LED_red_value.toInt()); //transfer string with values into integer
      digitalWrite(LED_7_green,LED_green_value.toInt()); //transfer string with values into integer
      digitalWrite(LED_7_blue,LED_blue_value.toInt()); //transfer string with values into integer
    }

    else if (command=="ADC0")
    {
      adc0 = ads.readADC_SingleEnded(0); //read the value of ADC A0 e.g. if full_command is ADC0
      Serial.println(adc0); //print the value
    }

    else if (command=="ADC1")
    {
      adc1 = ads.readADC_SingleEnded(1); //read the value of ADC A1
      Serial.println(adc1);
    }

    else if (command=="ADC2")
    {
      adc2 = ads.readADC_SingleEnded(2); //read the value of ADC A2
      Serial.println(adc2);
    }

    else if (command=="ADC3")
    {
      adc3 = ads.readADC_SingleEnded(3); //read the value of ADC A3
      Serial.println(adc3);
    }

    else if (command == "PRES")
    {
      float pressure = readPressure(); // read the pressure value
      //Serial.print("Pressure: ");
      Serial.println(pressure, 4); // print the pressure with 4 decimal places
      //Serial.println(" bar");
    }

  }
}

// pressure sensor
float readPressure() {
  int sensorValue = analogRead(analogInput0);  // Read the analog input
  float voltage = (sensorValue / 1023.0) * Va;  // Convert the analog reading to voltage
  float current = voltage / resistor;  // Convert voltage to current
  float pressure = mapPressure(current); // Convert current to pressure
  return pressure;
}

float mapPressure(float current) {
  // Map the sensor current (4-20 mA) to the pressure range (0-4 bar)
  float pressure = ((current - minCurrent) * (maxPressure - minPressure) / (maxCurrent - minCurrent)) + minPressure + 0.0225; // (0.0225) for Wika 0-1 bar, just deviation //+ 0.0127 + 1.01325 (for WIKA 0-4 bar); //interpolation with added deviation and atm pressure
  return pressure;
}

