import serial
import time

s = serial.Serial("COM5", 115200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)

# !!! Note to self: These are PLACEHOLDERS
# Change them when you've installed the tray in the machine
currentX = 0
currentY = 0
currentZ = 0
wasteX = 10
wasteY = 10
vial00X = 5
vial00Y = 0

def go_to_waste():
  global currentX
  currentX = wasteX
  global currentY
  currentY = wasteY
  s.write("G0 X" + str(currentX) + " Y" + str(currentY) + "\n")

def go_to_adds(adds):
  x = vial00X + (13.725 * (adds % 9))
  y = -1 * (vial00Y + (13.18 * (adds - (adds % 9))))
  global currentX
  currentX = x
  global currentY
  currentY = y
  s.write("G0 X" + str(currentX) + " Y" + str(currentY) + "\n")

def go_to_next_vial():
  global currentX
  global currentY
  xAdds = (currentX - vial00X) / 13.725
  print(xAdds)
  yAdds = (currentY - vial00Y) / 13.18
  print(yAdds)
  if (xAdds == 8 and yAdds == 5):
    currentX = vial00X
    currentY = vial00Y
    s.write("G0 X" + str(currentX) + " Y" + str(currentY) + "\n")
  elif (xAdds == 8):
    currentX = vial00X
    currentY += 13.18
    s.write("G0 X" + str(currentX) + " Y" + str(currentY) + "\n")
  else:
    currentX += 13.725
    s.write("G0 X" + str(currentX) + " Y" + str(currentY) + "\n")

def sample_to_vial(t):
  go_to_next_vial()
  time.sleep(t)
  go_to_waste()

def go_to_origin():
  s.write("G0 X0 Y0\n")
