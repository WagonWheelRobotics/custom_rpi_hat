import smbus
import time

def crc8(data, start, length):
    POLYNOMIAL = 0x131 # P(x) = x^8 + x^5 + x^4 + 1 = 100110001
    crc = 0xFF

    for i in range(start,start+length):
        crc ^= data[i]

        for bit in [8,7,6,5,4,3,2,1]:
            if crc & 0x80: crc =(crc << 1) ^ POLYNOMIAL
            else:          crc =(crc << 1)    
    return crc

def show(data):
    temp = round(0.00267 * ((data[0] << 8) + data[1]) -45, 2)
    humi = round(0.00152 * ((data[3] << 8) + data[4]), 2)
    crc =  (data[2]==crc8(data,0,2)) and (data[5]==crc8(data,3,2))

    print(temp,"degC",humi,"%RH", "CRC OK" if crc else "CRC NG")

def measure(i2c):
    i2c.write_byte_data(addr, 0x24, 0x00)
    time.sleep(0.1)
    data=i2c.read_i2c_block_data(addr,0x00,6)
    return data

def heater(i2c, on):
    if on:
        i2c.write_byte_data(addr, 0x30, 0x6d)   #Heater enable
    else:
        i2c.write_byte_data(addr, 0x30, 0x66)   #Heater disable

def soft_reset(i2c):
    i2c.write_byte_data(addr, 0x30, 0xa2)   # soft reset



i2c = smbus.SMBus(1)

addr = 0x44
soft_reset(i2c)
time.sleep(0.1)

data=measure(i2c)
show(data)
time.sleep(1.0)

heater(i2c,True)
print("Heater ON")
time.sleep(2.0)

data=measure(i2c)
show(data)
time.sleep(1.0)

heater(i2c,False)
print("Heater OFF")
time.sleep(2.0)

while True:
    data=measure(i2c)
    show(data)
    time.sleep(1.0)
