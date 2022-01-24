import serial
import json
import time

# Serial port default to Linux and port one.
s = serial.Serial("/dev/ttyUSB0", 115200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)

# Open .json file.
j = open("xyz.json", "r")
jData = json.loads(j.read())

# Set Windows and Linux serial directories.
XYZ_WINDOWS = "COM"
XYZ_LINUX = "/dev/ttyUSB"
# Zero machine position.
currentX = 0
currentY = 0
currentZ = 0
# Copy .json file variables into python variables.
rows = jData["values"][0]["rows"]
columns = jData["values"][1]["columns"]
vialXOffset = jData["values"][2]["vialXOffset"]
vialYOffset = jData["values"][3]["vialYOffset"]
wasteX = jData["values"][4]["wasteX"]
wasteY = jData["values"][5]["wasteY"]
wasteZ = jData["values"][6]["wasteZ"]
vial00X = jData["values"][7]["vial00X"]
vial00Y = jData["values"][8]["vial00Y"]

# Set OS and port.
def set_port(os: str, port: int):
  if (os == XYZ_WINDOWS):
    s = serial.Serial(XYZ_WINDOWS + str(port), 115200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
  elif (os == XYZ_LINUX):
    s = serial.Serial(XYZ_LINUX + str(port), 115200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
  else:
    print("Error: Valid OS not selected, try XYZ_WINDOWS or XYZ_LINUX")

# Internal function that just waits for a calculated amount of time after a command is sent to give room for the next command.
def wait_until_done(x1, x2, y1, y2, z1, z2):
  if (abs(x1 - x2) > abs(y1 - y2) and abs(x1 - x2) > abs(z1-z2)):
    time.sleep(1 + (abs(x1 - x2) / (1600 / 60)))
  elif abs(y1 - y2) > abs(x1 - x2) and abs(y1 - y2) > abs(z1 - z2):
    time.sleep(1 + (abs(y1 - y2) / (1600 / 60)))
  else:
    time.sleep(1 + (abs(z1 - z2) / (1600 / 60)))

# Sets units to metric.
def set_to_metric():
  s.write("G21".encode("UTF-8"))

# Resets input and output buffers.
def reset_buffers():
  s.reset_input_buffer()
  s.reset_output_buffer()

# Closes the serial port.
def serial_close():
  s.close()
  print("Serial port closed")

# Moves to the waste area.
def go_to_waste():
  global currentX
  global currentY
  global currentZ
  gtwX1 = currentX
  gtwY1 = currentY
  gtwZ1 = currentZ
  gtwX2 = wasteX
  gtwY2 = wasteY
  gtwZ2 = wasteZ
  currentX = wasteX
  currentY = wasteY
  currentZ = wasteZ
  s.write("G0 X".encode("UTF-8") + str(currentX).encode("ascii") + " Y".encode("UTF-8") + str(currentY).encode("ascii") + " Z".encode("UTF-8") + str(currentZ).encode("ascii") + "\n".encode("UTF-8"))
  print("Going to waste")
  wait_until_done(gtwX1, gtwX2, gtwY1, gtwY2, gtwZ1, gtwZ2)

# Moves to the address number given to the function. Address numbers start at zero and go up.
def go_to_adds(adds):
  global currentX
  global currentY
  global currentZ
  gtaX1 = currentX
  gtaY1 = currentY
  gtaZ1 = currentZ
  if (adds > ((rows * columns) - 1)):
    print("Error: Max address value is " + ((rows * columns) - 1) + ", try something smaller!")
  elif (adds < 0):
    print("Error: Minimum address value is 0, try something bigger!")
  else:
    if (adds == 0):
      x = vial00X
      y = vial00Y
    elif (adds > 0 and adds < rows):
      x = vial00X + (vialXOffset * (adds % rows))
      y = vial00Y
    else:
      x = vial00X + (vialXOffset * (adds % rows))
      y = -1 * abs(vial00Y + (vialYOffset * (adds / rows) - ((adds % rows) / adds)))
    z = 0
    currentX = x
    currentY = y
    currentZ = z
    gtaX2 = x
    gtaY2 = y
    gtaZ2 = z
    s.write("G0 X".encode("UTF-8") + str(currentX).encode("ascii") + " Y".encode("UTF-8") + str(currentY).encode("ascii") + " Z".encode("UTF-8") + str(currentZ).encode("ascii") + "\n".encode("UTF-8"))
    print("Going to vial address " + str(adds))
    wait_until_done(gtaX1, gtaX2, gtaY1, gtaY2, gtaZ1, gtaZ2)

# Moves nozzle to the next vial address. If the current vial address is the last one the nozzle will move to address 0.
def go_to_next_vial():
  global currentX
  global currentY
  global currentZ
  gtnvX1 = currentX
  gtnvY1 = currentY
  gtnvZ1 = currentZ
  xAdds = (currentX - vial00X) / vialXOffset
  yAdds = abs((currentY - vial00Y) / vialYOffset)
  if (xAdds == (rows - 1) and yAdds == (columns - 1)):
    currentX = vial00X
    currentY = vial00Y
  elif (xAdds == (rows - 1)):
    currentX = vial00X
    currentY -= vialYOffset
  else:
    currentX += vialXOffset
  gtnvX2 = currentX
  gtnvY2 = currentY
  gtnvZ2 = currentZ
  s.write("G0 X".encode("UTF-8") + str(currentX).encode("ascii") + " Y".encode("UTF-8") + str(currentY).encode("ascii") + " Z".encode("UTF-8") + str(currentZ).encode("ascii") + "\n".encode("UTF-8"))
  print("Going to next vial")
  wait_until_done(gtnvX1, gtnvX2, gtnvY1, gtnvY2, gtnvZ1, gtnvZ2)

# Moves nozzle to origin.
def go_to_origin():
  gtoX1 = currentX
  gtoY1 = currentY
  gtoZ1 = currentZ
  gtoX2 = 0
  gtoY2 = 0
  gtoZ2 = 0
  s.write("G0 X0 Y0 Z0\n".encode("UTF-8"))
  print("Going to origin")
  wait_until_done(gtoX1, gtoX2, gtoY1, gtoY2, gtoZ1, gtoZ2)