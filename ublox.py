import serial

ser = serial.Serial('/dev/ttyAMA5',baudrate=230400, timeout=1, parity = serial.PARITY_NONE)
x=ser.read(100)
print(x)

ser.close