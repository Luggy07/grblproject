import time

from grblproject import *

currentX = 0
currentY = 0
currentZ = 0

# !!! Note to self: The waste and vial constants are still PLACEHOLDERS
# Change the when you've installed the tray in the machine

time.sleep(2)
reset_buffers()
set_to_metric()

# Write your program here:
go_to_adds(1)
time.sleep(2)
go_to_next_vial()

time.sleep(5)
go_to_origin()
time.sleep(5)
reset_buffers()

serial_close()
