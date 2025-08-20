import sys
import os

# Add parent dir of pyvesc_custom to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pyvesc
from pyvesc.VESC.messages import GetValues, SetRPM, SetDutyCycle, SetCurrent, SetRotorPositionMode, GetRotorPosition
import serial
import time

# Set your serial port here (either /dev/ttyX or COMX)
serialport = '/dev/ttyACM0'

def get_values_example():
    with serial.Serial(serialport, baudrate=115200, timeout=0.05) as ser:
        try:
            # Optional: Turn on rotor position reading if an encoder is installed
            ser.write(pyvesc.encode(SetRotorPositionMode(SetRotorPositionMode.DISP_POS_OFF)))
            time.sleep(0.1)

            while True:
                # Set the ERPM of the VESC motor
                #    Note: if you want to set the real RPM you can set a scalar
                #          manually in setters.py
                #          12 poles and 19:1 gearbox would have a scalar of 1/228
                ser.write(pyvesc.encode(SetDutyCycle(0.03)))

                # Clear input buffer to avoid old data
                ser.reset_input_buffer()

                # Request the current measurement from the vesc
                ser.write(pyvesc.encode_request(GetValues))

                # Wait for response
                # time.sleep(0.1)
                # all_data = ser.read(ser.in_waiting) 

                # Read the correct amount: 76 bytes (not 61!)
                if ser.in_waiting >= 79:
                    response_data = ser.read(79)  # Use correct size from analysis
                    (response, consumed) = pyvesc.decode(response_data)
                    # print(response)
                    # Print out the values
                    try:
                        print(f"RPM: {response.rpm}")
                        print(f"Avg input current: {response.avg_input_current}")

                    except:
                        # ToDo: Figure out how to isolate rotor position and other sensor data
                        #       in the incoming datastream
                        #try:
                        #    print(response.rotor_pos)
                        #except:
                        #    pass
                        pass


        except KeyboardInterrupt:
            # Turn Off the VESC
            ser.write(pyvesc.encode(SetCurrent(0)))


if __name__ == "__main__":
    get_values_example()
