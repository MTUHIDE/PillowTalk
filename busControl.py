""" 
Import smbus for inflating and deflating

Import RPI.GPIO
Import time
for the button

To start

DEVICE_BUS = 1
DEVICE_ADDR = 0x10
bus = smbus.SMBus(DEVICE_BUS)

# ID 1, 2 are for the left motor
# ID 3, 4 are for the right motor
bus.write_byte_data(DEVICE_ADDR, 1, #HEX HERE)
bus.write_byte_data(DEVICE_ADDR, 2, #HEX HERE)
bus.write_byte_data(DEVICE_ADDR, 3, #HEX HERE)
bus.write_byte_data(DEVICE_ADDR, 4, #HEX HERE)

all 0x00 to stop

{
    0xFF
    0x00
    0xFF
    0x00
}    to inflate both, to inflate the left the top 2 (ID 1, 2). to inflate the right the bottom 2 (ID 3, 4)

{
    0xFF
    0x00
    0xFF
    0x00
} To deflate both, To deflate the left the top 2 (ID 1, 2). To deflate the right the bottom 2 (ID 3,4).

    
    
"""
