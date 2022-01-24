import time
import json

from xyz import *

# Set current OS and port
open_port(XYZ_LINUX, 0)

# Open .json file
j = open("xyz.json", "r")

# Tell the program that the current position is zero
currentX = 0
currentY = 0
currentZ = 0

# !!! Note to self: The waste and vial constants are still PLACEHOLDERS
# Change the when you've installed the tray in the machine

# Wait until grbl is connected then reset the input and output buffers and set the units to metric
time.sleep(2)
reset_buffers()
set_to_metric()

# Write your program here:

# Go back to origin, reset input and output buffers and close the serial port .json file.
go_to_origin()
reset_buffers()
serial_close()
j.close()
