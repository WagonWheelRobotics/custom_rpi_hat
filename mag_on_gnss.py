import smbus
import time
import struct

addr=0x1e

i2c = smbus.SMBus(1)

x=i2c.read_i2c_block_data(addr, 0x0a,3) 
#print('%02x'%x[0])
#print('%02x'%x[1])
#print('%02x'%x[2])

if x[0]==0x48 and x[1]==0x34 and x[2]==0x33:
    print('HMC5883L is detected')
    CFGA_REG=0x00
    CFGB_REG=0x01
    MODE_REG=0x02
    DATA_REG=0x03
    STATUS_REG=0x09
    #GN=0 # 0.88Gauss
    GN=3 # 2.5Gauss
    #GN=5 # 4.7Gauss
    #GN=7 # 8.1Gauss
    i2c.write_byte_data(addr, MODE_REG, 0x03)   # idle
    time.sleep(0.05)
    i2c.write_byte_data(addr, CFGA_REG, 0x70)   # 8 average, 15Hz, normal
    i2c.write_byte_data(addr, CFGB_REG, GN << 5)
    x=i2c.read_i2c_block_data(addr, DATA_REG,6) # dymmy read
    i2c.write_byte_data(addr, MODE_REG, 0x00)
    while True:
        t = time.time()
        s=i2c.read_byte_data(addr, STATUS_REG) 
        #print('%02x'%s)
        if (s & 1)==1:
            x=i2c.read_i2c_block_data(addr, DATA_REG,6) 
            [mx,mz,my]=struct.unpack('>hhh', bytearray(x))
            print('%.6f,%d,%d,%d'%(t,mx,my,mz))
            time.sleep(0.065)
        else:
            time.sleep(0.001)
