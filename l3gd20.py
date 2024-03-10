import smbus
import time
import struct

addr=0x6b

L3GD20_WHOAMI = 0x0f
L3GD20_CTRL1 = 0x20
L3GD20_CTRL2 = 0x21
L3GD20_CTRL3 = 0x22
L3GD20_CTRL4 = 0x23
L3GD20_CTRL5 = 0x24
L3GD20_OUT_TEMP = 0x26
L3GD20_X_L = 0x28
L3GD20_X_H = 0x29
L3GD20_Y_L = 0x2a
L3GD20_Y_H = 0x2b
L3GD20_Z_L = 0x2c
L3GD20_Z_H = 0x2d

i2c = smbus.SMBus(1)
x=i2c.read_byte_data(addr, L3GD20_WHOAMI) 


if x==0xd4:
    i2c.write_byte_data(addr, L3GD20_CTRL1, 0x30)    #ODR 95Hz, 25Hz cutoff, power active, XYZ enable
    time.sleep(0.1)

    i2c.write_byte_data(addr, L3GD20_CTRL1, 0x3f)    #ODR 95Hz, 25Hz cutoff, power active, XYZ enable
    time.sleep(0.1)

    i2c.write_byte_data(addr, L3GD20_CTRL2, 0x00)

    i2c.write_byte_data(addr, L3GD20_CTRL3, 0x08)  #Dataready on INT2 (GPIO27)

    i2c.write_byte_data(addr, L3GD20_CTRL4, 0x80)  #Block update, FS=250dps


    while True:
        x=[]
        x.append( i2c.read_byte_data(addr, L3GD20_X_L) )
        x.append( i2c.read_byte_data(addr, L3GD20_X_H) )
        x.append( i2c.read_byte_data(addr, L3GD20_Y_L) )
        x.append( i2c.read_byte_data(addr, L3GD20_Y_H) )
        x.append( i2c.read_byte_data(addr, L3GD20_Z_L) )
        x.append( i2c.read_byte_data(addr, L3GD20_Z_H) )

        [wx,wy,wz]=struct.unpack('<hhh', bytearray(x))
        temp=i2c.read_byte_data(addr, L3GD20_OUT_TEMP)
        status=i2c.read_byte_data(addr, 0x27)
        print(x,wx,wy,wz,temp,'%02x'%status)
        time.sleep(1.0/95.0)
else:
    print('L3GD20 is not detected')
