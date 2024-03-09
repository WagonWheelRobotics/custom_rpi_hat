import smbus
import time

addr=0x76

MS5611_CMD_ADC_CONV = 0x40
MS5611_CMD_ADC_READ = 0x00
MS5611_CMD_ADC_4096 = 0x08 #ADC OSR=4096
MS5611_CMD_RESET = 0x1E
MS5611_CMD_CONV_D1 = 0x00
MS5611_CMD_CONV_D2 = 0x10
MS5611_CMD_READ_PROM = 0xA0

def read_prom(i2c, offset):
    r=MS5611_CMD_READ_PROM + offset*2
    x=i2c.read_i2c_block_data(addr, r, 2) 
    #print(offset,'%02x'%r,x)
    return x[0]*256.0+x[1]





POW2_6=2**6
POW2_7=2**7
POW2_8=2**8
POW2_15=2**15
POW2_16=2**16
POW2_17=2**17
POW2_21=2**21
POW2_23=2**23
POW2_31=2**31

i2c = smbus.SMBus(1)

i2c.write_byte(addr, MS5611_CMD_RESET)
time.sleep(0.1)

# read calibration data
C=[]
for i in range(0,8):
    C.append(read_prom(i2c,i))

#print(C)

while True:

    # read pressure
    i2c.write_byte(addr, MS5611_CMD_ADC_CONV+MS5611_CMD_CONV_D1+MS5611_CMD_ADC_4096)
    time.sleep(0.01)
    x=i2c.read_i2c_block_data(addr, MS5611_CMD_ADC_READ,3) 
    D1=x[0]*65536.0+x[1]*256.0+x[2]

    # read temperature
    i2c.write_byte(addr, MS5611_CMD_ADC_CONV+MS5611_CMD_CONV_D2+MS5611_CMD_ADC_4096)
    time.sleep(0.01)
    x=i2c.read_i2c_block_data(addr, MS5611_CMD_ADC_READ,3) 
    D2=x[0]*65536.0+x[1]*256.0+x[2]


    #print("D1",D1,"D2",D2)

    dT  = D2 - C[5]*POW2_8
    OFF = C[2]*POW2_17 + dT*C[4]/POW2_6
    SENS= C[1]*POW2_16 + dT*C[3]/POW2_7

    T=2000+(dT*C[6]/POW2_23)  # 0.01degC

    #print("dT",dT)
    #print("T",T)

    if T<2000:
        T2=(dT*dT) / POW2_31
        T=T-T2
        delta=T-2000.0
        delta=5.0*delta*delta
        OFF =OFF-delta / 2.0
        SENS=SENS-delta / 4.0

        if T<-1500:
            delta=T+1500
            delta=delta*delta
            OFF =OFF-7.0*delta
            SENS=SENS-5.5*delta

    P= ((D1*SENS)/POW2_21-OFF)/POW2_15 # 0.01mbar

    print('%.3f mbar'%(P*0.01), '%.3f degC'%(T*0.01))

    time.sleep(1.0)