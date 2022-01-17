import time

from grblproject import *

s = serial.Serial("/dev/ttyUSB0", 115200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)

currentX = 0
currentY = 0
currentZ = 0

# !!! Note to self: The waste and vial constants are still PLACEHOLDERS
# Change the when you've installed the tray in the machine

time.sleep(2)
reset_buffers()
set_to_metric()

# Write your program here:
go_to_adds(23)
go_to_next_vial()

go_to_origin()
reset_buffers()

serial_close()
