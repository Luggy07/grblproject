import serial
import time

from grblproject import *

s = serial.Serial("COM5", 115200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)

currentX = 0
currentY = 0
currentZ = 0

# !!! Note to self: The waste and vial constants are still PLACEHOLDERS
# Change the when you've installed the tray in the machine

time.sleep(2)
s.reset_input_buffer()
s.write("G21")

# Write your program here:
go_to_adds(1)
time.sleep(2)
go_to_next_vial()

time.sleep(5)
go_to_origin()
time.sleep(5)
s.reset_input_buffer()

s.close()
