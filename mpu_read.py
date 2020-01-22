import serial
import sys
import time

def get_mpu_values():
    ports = '/dev/ttyUSB'

    max_port = 100

    ser = serial.Serial()
    ser.baudrate = 9600

    while True:
        try:
            # print ("Ready for a new connection...")
            
            while not ser.is_open:
                # print ser.is_open
                for num in range(max_port+1):
                    try:
                        # print "trying for %s" %(port)
                        port = ports + str(num)
                        ser.port = port
                        ser.open()
                        # print ("status for - ", port, str(ser.is_open))
                        break
                    except Exception as e:
                        pass

            # print (ser)
            out = ''
            while True:
                mpu_value_start = "got acc_x value - "
                avr_data = ser.readline().decode()
                mpu_value = None
                
                if avr_data.find(mpu_value_start) == 0:
                    mpu_value = float(avr_data[len(mpu_value_start):-1]+mpu_value_start[-1]) 

                # print avr_data,

                if mpu_value is not None:
                    return mpu_value
                    # print "numeric value = ", mpu_value

        except Exception as e:
            print ("disconnection reason - ", str(e))
            ser.is_open = False
            print ("disconnected, waiting...")
            pass