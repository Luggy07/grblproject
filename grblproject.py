import serial
import time

s = serial.Serial("/dev/ttyUSB0", 115200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)

# !!! Note to self: These are PLACEHOLDERS
# Change them when you've installed the tray in the machine
currentX = 0
currentY = 0
currentZ = 0
wasteX = 10
wasteY = 10
vial00X = 5
vial00Y = 0

# This is an internal function and just waits for a calculated amount of time after a command is sent to give room for the next command
def wait_until_done(x1, x2, y1, y2):
  if (abs(x1 - x2) > abs(y1 - y2)):
    time.sleep(1 + (abs(x1 - x2) / (1600 / 60)))
  else:
    time.sleep(1 + (abs(y1 - y2) / (1600 / 60)))

def set_to_metric():
  s.write("G21".encode("UTF-8"))

def reset_buffers():
  s.reset_input_buffer()
  s.reset_output_buffer()

def serial_close():
  s.close()
  print("Serial port closed")

def go_to_waste():
  global currentX
  global currentY
  gtwX1 = currentX
  gtwY1 = currentY
  gtwX2 = wasteX
  gtwY2 = wasteY
  currentX = wasteX
  currentY = wasteY
  s.write("G0 X".encode("UTF-8") + str(currentX).encode("ascii") + " Y".encode("UTF-8") + str(currentY).encode("ascii") + "\n".encode("UTF-8"))
  print("Going to waste")
  wait_until_done(gtwX1, gtwX2, gtwY1, gtwY2)

def go_to_adds(adds):
  global currentX
  global currentY
  gtaX1 = currentX
  gtaY1 = currentY
  if (adds > 23):
    print("Error: Max address value is 23, try something smaller!")
  elif (adds < 0):
    print("Error: Minimum address value is 0, try something bigger!")
  else:
    if (adds == 0):
      x = vial00X
      y = vial00Y
    elif (adds > 0 and adds < 6):
      x = vial00X + (19.9 * (adds % 6))
      y = vial00Y
    else:
      x = vial00X + (19.9 * (adds % 6))
      y = -1 * abs(vial00Y + (19.3 * ((adds / 6) - ((adds % 6) / adds))))
    currentX = x
    currentY = y
    gtaX2 = x
    gtaY2 = y
    s.write("G0 X".encode("UTF-8") + str(currentX).encode("ascii") + " Y".encode("UTF-8") + str(currentY).encode("ascii") + "\n".encode("UTF-8"))
    print("Going to vial address " + str(adds))
    wait_until_done(gtaX1, gtaX2, gtaY1, gtaY2)

def go_to_next_vial():
  global currentX
  global currentY
  gtnvX1 = currentX
  gtnvY1 = currentY
  xAdds = (currentX - vial00X) / 19.9
  yAdds = abs((currentY - vial00Y) / 19.3)
  if (xAdds == 5 and yAdds == 3):
    currentX = vial00X
    currentY = vial00Y
    gtnvX2 = vial00X
    gtnvY2 = vial00Y
    s.write("G0 X".encode("UTF-8") + str(currentX).encode("ascii") + " Y".encode("UTF-8") + str(currentY).encode("ascii") + "\n".encode("UTF-8"))
    print("Going to next vial")
    wait_until_done(gtnvX1, gtnvX2, gtnvY1, gtnvY2)
  elif (xAdds == 5):
    currentX = vial00X
    currentY -= 19.3
    gtnvX2 = currentX
    gtnvY2 = currentY
    s.write("G0 X".encode("UTF-8") + str(currentX).encode("ascii") + " Y".encode("UTF-8") + str(currentY).encode("ascii") + "\n".encode("UTF-8"))
    print("Going to next vial")
    wait_until_done(gtnvX1, gtnvX2, gtnvY1, gtnvY2)
  else:
    currentX += 19.9
    gtnvX2 = currentX
    gtnvY2 = gtnvY1
    s.write("G0 X".encode("UTF-8") + str(currentX).encode("ascii") + " Y".encode("UTF-8") + str(currentY).encode("ascii") + "\n".encode("UTF-8"))
    print("Going to next vial")
    wait_until_done(gtnvX1, gtnvX2, gtnvY1, gtnvY2)

def sample_to_vial(t):
  go_to_next_vial()
  time.sleep(t)
  go_to_waste()

def go_to_origin():
  gtoX1 = currentX
  gtoY1 = currentY
  gtoX2 = 0
  gtoY2 = 0
  s.write("G0 X0 Y0\n".encode("UTF-8"))
  print("Going to origin")
  wait_until_done(gtoX1, gtoX2, gtoY1, gtoY2)



# It just works
#  -Todd Howard
