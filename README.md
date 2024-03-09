# custom_rpi_hat
Test code for custom raspberry pi hat

# Devices
## I2C
SHT31-DIS (0x44)

MS5611 (0x76)

L3GD20 (0x6B)

Compass on GNSS Module
 - HMC5883L (0x1E)
 - LIS3MDL (0x1E)
 - IST8308 (0x0E)

## UART4
GNSS NEO-M8N Serial port (https://store.mrobotics.io/product-p/m10034-solo.htm)

# Prerequisites

## I2C
I2C should be enabled in raspi-conf.

## UART4 (Raspberry Pi4/5)
Add these lines to /boot/config.txt
```
enable_uart=1
dtoverlay=uart4
```
