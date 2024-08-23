import sys
from PyQt5 import QtWidgets, QtCore
from datetime import datetime
from modelLoop import Model
from GUI.CFI_GUI1_red import Ui_MainWindow
from PyQt5.QtCore import QThread  

class MyMainWindow(QtWidgets.QMainWindow):
    model_request = QtCore.pyqtSignal(dict)

    def __init__(self):
        super(MyMainWindow, self).__init__()

        # User interface from QtDesigner
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Ensure the LDR_env_meas checkbox is always checked
        self.ui.LDR_env_meas.setChecked(True)

        # Connect start and stop button click to start_experiment function
        self.ui.pushStart.clicked.connect(self.start_experiment)
        #self.ui.pushStop.clicked.connect(self.stop_experiment)

        self.model = Model()
        self.model_thread = QThread()
        self.model.data_signal.connect(self.update_progress)
        #self.model.pressure_signal.connect(self.update_pressure) #'signal'
        self.model_request.connect(self.model.mode_selection)
        self.model.moveToThread(self.model_thread)
        self.model_thread.start()

        self.experiment_running = False  # Flag to track whether the experiment is running

    def start_experiment(self):
        if not self.experiment_running:
            # Get Data from QLineEdit fields
            Qt_Inputs = {}
            for i in range(1, 8):
                Qt_Inputs[f'LED{i}_Red_QLE'] = int(getattr(self.ui, f'LED{i}_Red_QLE').text())
                Qt_Inputs[f'LED{i}_Green_QLE'] = int(getattr(self.ui, f'LED{i}_Green_QLE').text())
                Qt_Inputs[f'LED{i}_Blue_QLE'] = int(getattr(self.ui, f'LED{i}_Blue_QLE').text())

        # Get measurement time and time interval from QLineEdit fields
        measure_time = float(self.ui.LDR_Meas_Time_QLE.text())
        time_interval = float(self.ui.LDR_Time_Int_QLE.text())

        # Add measurement time and time interval to the Qt_Inputs dictionary
        Qt_Inputs['Measurement_Time'] = measure_time
        Qt_Inputs['Time_Interval'] = time_interval
        Qt_Inputs['LDR_env_meas'] = self.ui.LDR_env_meas.isChecked()  # Check if environmental measurement is requested

        Qt_Inputs["Mode"] = "Simple"

        # Perform experiment using Model
        self.model_request.emit(Qt_Inputs)
        self.experiment_running = True  # Update flag to indicate experiment is running
        
        # Start pressure reading
        #self.model_thread.start()

    #@QtCore.pyqtSlot(float)
    #def update_pressure(self, pressure_value):
        # Update the GUI element (e.g., QLineEdit) with pressure value
        #self.ui.p_Out_QLE.setText(f"{pressure_value:.2f}")

    def update_progress():
        print("Update signal received.")

def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MyMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
