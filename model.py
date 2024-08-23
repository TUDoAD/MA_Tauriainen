import time
import os
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from arduino_control import Arduino_Control
import math
from PyQt5.QtCore import QObject, pyqtSignal as Signal, pyqtSlot as Slot, QThread

class Model(QObject):
    data_signal = Signal(dict)
    pressure_signal = Signal(float) #'signal'

    def __init__(self):
        super().__init__()
        self.Arduino_Control = Arduino_Control()

        def update_pressure(self, pressure_value):
            self.pressure_signal.emit(pressure_value)

    @Slot(dict)
    def mode_selection(self, data):
        if data["Mode"] == "Simple":
            self.simple_experiment(data)

    @Slot(dict)
    def simple_experiment(self, Qt_Inputs):
        env_data_pre = pd.DataFrame(columns=["envTime_pre", "envADC0_pre", "envADC1_pre", "envADC2_pre", "envADC3_pre"])
        env_adc_mean_pre = pd.DataFrame(columns=["envADC0_mean_pre", "envADC1_mean_pre", "envADC2_mean_pre", "envADC3_mean_pre"])
        env_data_pre_leds = pd.DataFrame(columns=["envTime_pre_leds", "envADC0_pre_leds", "envADC1_pre_leds", "envADC2_pre_leds", "envADC3_pre_leds"])
        env_adc_mean_pre_leds = pd.DataFrame(columns=["envADC0_mean_pre_leds", "envADC1_mean_pre_leds", "envADC2_mean_pre_leds", "envADC3_mean_pre_leds"])

        env_data_post = pd.DataFrame(columns=["envTime_post", "envADC0_post", "envADC1_post", "envADC2_post", "envADC3_post"])
        env_adc_mean_post = pd.DataFrame(columns=["envADC0_mean_post", "envADC1_mean_post", "envADC2_mean_post", "envADC3_mean_post"])
        env_data_post_leds = pd.DataFrame(columns=["envTime_post_leds", "envADC0_post_leds", "envADC1_post_leds", "envADC2_post_leds", "envADC3_post_leds"])
        env_adc_mean_post_leds = pd.DataFrame(columns=["envADC0_mean_post_leds", "envADC1_mean_post_leds", "envADC2_mean_post_leds", "envADC3_mean_post_leds"])

        #data = pd.DataFrame(columns=["Time", "ADC0", "ADC1", "ADC2", "ADC3"])
        data = pd.DataFrame(columns=["Pressure","Time", "ADC0", "ADC1", "ADC2", "ADC3"])

        if Qt_Inputs.get('LDR_env_meas', False):
            self.meas_env_pre(env_data_pre, env_adc_mean_pre)
            self.meas_env_with_leds(Qt_Inputs, env_data_pre_leds, env_adc_mean_pre_leds, pre_measurement=True)

        self.measure_with_leds(Qt_Inputs, data, env_adc_mean_pre)

        if Qt_Inputs.get('LDR_env_meas', False):
            self.meas_env_with_leds(Qt_Inputs, env_data_post_leds, env_adc_mean_post_leds, pre_measurement=False)
            self.meas_env_post(env_data_post, env_adc_mean_post)

        self.save_to_excel(Qt_Inputs, env_data_pre, env_adc_mean_pre, env_data_pre_leds, env_adc_mean_pre_leds, data, env_data_post, env_adc_mean_post, env_data_post_leds, env_adc_mean_post_leds)

    def meas_env_pre(self, env_data_pre, env_adc_mean_pre):
        self.measure_environment(env_data_pre, env_adc_mean_pre, "pre")

    def meas_env_post(self, env_data_post, env_adc_mean_post):
        self.measure_environment(env_data_post, env_adc_mean_post, "post")

    def measure_environment(self, env_data, env_adc_mean, phase):
        env_starting_time = time.time()
        env_measure_time = 10
        env_time_interval = 0.001

        print(f'{phase} environment measurement starts...')
        while time.time() < env_starting_time + env_measure_time:
            env_adc0_str = self.Arduino_Control.read_adc0()
            env_adc1_str = self.Arduino_Control.read_adc1()
            env_adc2_str = self.Arduino_Control.read_adc2()
            env_adc3_str = self.Arduino_Control.read_adc3()

            try:
                env_adc0 = float(env_adc0_str)
                env_adc1 = float(env_adc1_str)
                env_adc2 = float(env_adc2_str)
                env_adc3 = float(env_adc3_str)
                env_timestamp = time.time() - env_starting_time

                env_data.loc[len(env_data)] = [env_timestamp, env_adc0, env_adc1, env_adc2, env_adc3]
            except ValueError:
                continue

            time.sleep(env_time_interval)

        env_adc0_mean = env_data.iloc[:, 1].mean()  # Assuming the second column is envADC0
        env_adc1_mean = env_data.iloc[:, 2].mean()  # Assuming the third column is envADC1
        env_adc2_mean = env_data.iloc[:, 3].mean()  # Assuming the fourth column is envADC2
        env_adc3_mean = env_data.iloc[:, 4].mean()  # Assuming the fifth column is envADC3

        env_adc_mean.loc[len(env_adc_mean)] = [env_adc0_mean, env_adc1_mean, env_adc2_mean, env_adc3_mean]
        print(f"env_adc0_mean_{phase} = {env_adc0_mean:.0f}, env_adc1_mean_{phase} = {env_adc1_mean:.0f}, env_adc2_mean_{phase} = {env_adc2_mean:.0f}, env_adc3_mean_{phase} = {env_adc3_mean:.0f}")
        print(f'{phase} environment measurement done')

    def meas_env_with_leds(self, Qt_Inputs, env_data, env_adc_mean, pre_measurement):
        phase = "pre_leds" if pre_measurement else "post_leds"
        self.set_leds(Qt_Inputs)

        retry_count = 0
        max_retries = 10

        while retry_count < max_retries:
            self.measure_environment(env_data, env_adc_mean, phase)
            if self.check_leds_on(env_data):
                print(f"LEDs are properly set for {phase}.")
                break
            else:
                print(f"Retrying to set LEDs for {phase} (Attempt {retry_count + 1}/{max_retries})...")
                self.set_leds(Qt_Inputs)
                retry_count += 1

        if retry_count == max_retries:
            print(f"Max retries reached. LEDs may not be properly set for {phase}.")

        for i in range(1, 8):
            getattr(self.Arduino_Control, f'Write_LED{i}')(0, 0, 0)

    def measure_with_leds(self, Qt_Inputs, data, env_adc_mean_pre):
        self.set_leds(Qt_Inputs)

        retry_count = 0
        max_retries = 10

        while retry_count < max_retries:
            starting_time = time.time()
            measure_time = Qt_Inputs.get('Measurement_Time', 100)
            time_interval = Qt_Inputs.get('Time_Interval', 0.000001)

            all_leds_on = True
            while time.time() < starting_time + measure_time:
                timestamp = time.time() - starting_time
                adc0_str = self.Arduino_Control.read_adc0()
                adc1_str = self.Arduino_Control.read_adc1()
                adc2_str = self.Arduino_Control.read_adc2()
                adc3_str = self.Arduino_Control.read_adc3()

                try:
                    adc0 = float(adc0_str)
                    adc1 = float(adc1_str)
                    adc2 = float(adc2_str)
                    adc3 = float(adc3_str)

                    if adc0 < 500 or adc1 < 500 or adc2 < 500 or adc3 < 500:
                        all_leds_on = False
                    
                    #Read pressure value from sensor
                    pressure_value = self.Arduino_Control.read_pressure()
                    print(f"Pressure: {pressure_value:.2f} bar")  # Print pressure to terminal

                    print(f"t = {timestamp:.0f}, adc0 = {adc0:.0f}, adc1 = {adc1:.0f}, adc2 = {adc2:.0f}, adc3 = {adc3:.0f}")

                    timestamp = time.time() - starting_time
                    #data.loc[len(data)] = [timestamp, adc0, adc1, adc2, adc3]
                    data.loc[len(data)] = [pressure_value, timestamp, adc0, adc1, adc2, adc3]

                except ValueError:
                    continue

                time.sleep(time_interval)

            if all_leds_on:
                print("LEDs are properly set for measurement.")
                break
            else:
                print(f"Retrying to set LEDs for measurement (Attempt {retry_count + 1}/{max_retries})...")
                self.set_leds(Qt_Inputs)
                retry_count += 1

        if retry_count == max_retries:
            print("Max retries reached. LEDs may not be properly set for measurement.")

        for i in range(1, 8):
            getattr(self.Arduino_Control, f'Write_LED{i}')(0, 0, 0)

        print('LDR measurement done.')

    def set_leds(self, Qt_Inputs):
        for i in range(1, 8):
            red = Qt_Inputs[f'LED{i}_Red_QLE']
            green = Qt_Inputs[f'LED{i}_Green_QLE']
            blue = Qt_Inputs[f'LED{i}_Blue_QLE']
            getattr(self.Arduino_Control, f'Write_LED{i}')(red, green, blue)

    def check_leds_on(self, env_data):
        last_row = env_data.iloc[-1]
        return all(last_row[1:] >= 500)

    def save_to_excel(self, Qt_Inputs, env_data_pre, env_adc_mean_pre, env_data_pre_leds, env_adc_mean_pre_leds, data, env_data_post, env_adc_mean_post, env_data_post_leds, env_adc_mean_post_leds):
        timestamp_str = datetime.now().strftime('%Y_%m_%d_%H_%M')
        filename = f'fourCoils_40degr_lf10_gf5_{timestamp_str}_onlyAir_pre.xlsx'
        save_folder = 'coilE_50degr'
        save_path = os.path.join('W:/Studenten/Tauriainen/Programming/Python/experimentalData/coilExp/01_08_2024', save_folder, filename)

        inputs_data = list(Qt_Inputs.items())
        inputs_df = pd.DataFrame(inputs_data, columns=['Parameter', 'Value'])

        full_data = pd.concat([
            env_data_pre, env_adc_mean_pre,
            env_data_pre_leds, env_adc_mean_pre_leds,
            data,
            env_data_post, env_adc_mean_post,
            env_data_post_leds, env_adc_mean_post_leds
        ], axis=1)
        full_data.replace({0.0: np.nan}, inplace=True)

        with pd.ExcelWriter(save_path) as writer:
            inputs_df.to_excel(writer, sheet_name='Inputs', index=False)
            full_data.to_excel(writer, sheet_name='Outputs', index=False)

        print("Data saved to Excel. Experiment completed.")

    def stop_experiment(self):
        self.stopped = True
        for i in range(1, 8):
            getattr(self.Arduino_Control, f'Write_LED{i}')(0, 0, 0)
        self.Arduino_Control.close_connection()
        print("Experiment stopped.")