import serial
import sys
import time

ports = '/dev/ttyUSB'

max_port = 100

ser = serial.Serial()
ser.baudrate = 9600
# ser.stopbits = 1
# ser.parity = serial.PARITY_ODD

while True:

	try:
		print("Ready for a new connection...")
		
		while not ser.is_open:
			# print ser.is_open
			for num in range(max_port+1):
				try:
					# print "trying for %s" %(port)
					port = ports + str(num)
					ser.port = "/dev/cu.usbserial-A50285BI"					# REMOVE THE HARDCODED STRING!!
					ser.open()
					# print ("status for - ", port, str(ser.is_open))
					break
				except Exception as e:
					pass

		print(ser)
		out = ''
		while True:
			# mpu_value_start = "got acc_x value - "
			avr_data = ser.readline().decode()
			# avr_data = ser.read(10).decode()
			# mpu_value = None
			
			# if avr_data.find(mpu_value_start) == 0:
			# 	mpu_value = int(avr_data[len(mpu_value_start):-1]+mpu_value_start[-1]) 

			# print("printing...")
			print(avr_data)
			# sys.stdout.write("printed!")

			# if mpu_value is not None:
			#         return mpu_value
					# print "numeric value = ", mpu_value

	except Exception as e:
		ser.close()
		print ("disconnection reason - ", str(e))
		ser.is_open = False
		print ("disconnected, waiting...")
		pass
