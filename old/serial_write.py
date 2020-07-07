import serial
import sys
import time
import struct

# :10778000F1CF86957105610508940895E894BB27AB
# :0E77900066277727CB0197F90895F894FFCF6D
# :040000030000700089
# :00000001FF
# main hex file path - /Users/aadityasharma/working/atmega_328p_projects/workspace/general_testing/main_compiled/main.hex

SERIAL_RESPONSE_OK = 'a'
LAST_LINE_IN_HEX = ':00000001FF'
END_OF_LINE = 'e'
START_CHAR = ':'
END_CHAR = ';'
hex_fd = None
ser = None

def get_low_high_bytes(word):
	low = word & 255
	high = (word >> 8) & 255
	return low, high


def extract_data_from_line(line):

	extracted_data = dict()
	if not line[0] == ':':
		raise Exception("unknown data line!")
	byte_count = int(line[1:3], 16)
	address = int(line[3:7], 16)
	data = line[9:9+(byte_count*2)]
	checksum = int(line[9+(byte_count*2):-1] + line[-1], 16)
	int_data_arr = []

	for i in range(byte_count):
		int_data_arr.append(int(data[i*2:i*2+2], 16))

	extracted_data['byte_count'] = byte_count
	extracted_data['address_low'], extracted_data['address_high'] = get_low_high_bytes(address)
	extracted_data['data'] = int_data_arr
	extracted_data['checksum'] = checksum

	return extracted_data


def get_next_line_from_hex_file(file_path):

	global hex_fd
	if not hex_fd:
		hex_fd = open(file_path, 'r')

	line = hex_fd.readline()

	if not line or LAST_LINE_IN_HEX in line:
		hex_fd.close()
		hex_fd = None
		return None
	return line


def validate_response_from_mcu(isEnd=False):

	global ser
	# print("Validating response...")
	resp = ser.read(size=1).decode()
	# print("GOT - ", resp)
	if isEnd:
		if not resp == SERIAL_RESPONSE_OK:
			print("Got response from MCU - ", resp, " but expected - ", SERIAL_RESPONSE_OK)
			raise Exception("Invalid response from MCU!")
		else:
			print("Hex file uploaded, exiting...")
			while True:
				print(ser.readline())

	elif not resp == SERIAL_RESPONSE_OK:
		print("Got response from MCU - ", resp, " but expected - ", SERIAL_RESPONSE_OK)
		raise Exception("Invalid response from MCU!")

	return True

def int_write(toWrite):

	global ser
	# print("Sending %d to MCU" %(toWrite))
	ser.write(b'' + struct.pack('!B', toWrite))
	ser.readline()
	# print("Got response from MCU - %s " %(ser.readline()))

def char_write(toWrite):

	global ser
	# print("Sending %s to MCU" %(toWrite))
	ser.write(toWrite.encode())
	ser.readline()
	# print("Got response from MCU - %s " %(ser.readline()))

def upload_line_to_mcu(line):

	global ser

	if not line:
		print("Sendind the end char to MCU...")
		char_write(END_CHAR)
		validate_response_from_mcu(isEnd=True)
		return False

	line_data = extract_data_from_line(line)
	# print("=====================================================================================")
	# print("Sendind the init signal to MCU...")
	char_write(START_CHAR)
	validate_response_from_mcu()
	# print("=====================================================================================")
	# print("Sendind the address field to MCU...")
	int_write(line_data['address_high'])
	validate_response_from_mcu()
	int_write(line_data['address_low'])
	validate_response_from_mcu()
	# print("=====================================================================================")
	# print("Sendind the byte count to MCU...")
	int_write(line_data['byte_count'])
	validate_response_from_mcu()
	# print("=====================================================================================")
	# print("Sendind the data to MCU...")
	for data in line_data['data']:
		int_write(data)
		validate_response_from_mcu()

	char_write(END_OF_LINE)

	# print("Sendind the end char to MCU...")
	# int_write(END_CHAR)
	# validate_response_from_mcu()
	return True
	
if __name__ == '__main__':
	ports = '/dev/ttyUSB'
	ports = '/dev/cu.usbserial-A50285BI'

	if len(sys.argv) < 2:
		raise Exception("Usage - python serial_write.py <hex_file_path>\n")

	hex_file_path = sys.argv[1]
	# hex_file_path = '/Users/aadityasharma/working/atmega_328p_projects/workspace/general_testing/main_compiled/main.hex'
	# print(extract_data_from_line(get_next_line_from_hex_file(hex_file_path)))

	# exit(0)

	max_port = 100

	ser = serial.Serial()
	ser.baudrate = 9600
	ser.stopbits = 1
	ser.parity = serial.PARITY_ODD

	while True:

		try:
			print ("Ready for a new connection...")

			while not ser.is_open:
				for num in range(max_port+1):
					try:
						port = ports 
						ser.port = port
						ser.open()
						break
					except Exception as e:
						pass

			print(ser)
			out = ''
			while True:
				# mpu_value_start = "got acc_x value - "
				# avr_data = ser.readline().decode()
				# toSend = b''
				# toSend += struct.pack('!B', 4)
				# ser.write(START_CHAR)
				time.sleep(5)
				
				line_num = 0

				while upload_line_to_mcu(get_next_line_from_hex_file(hex_file_path)):
					print("Sent the line - %d" %line_num)
					line_num += 1
				# while(upload_line_to_mcu(get_next_line_from_hex_file(hex_file_path))):
				# 	print("Line number %d sent!" %(line_num))
				# 	line_num += 1
				
				# ll = get_next_line_from_hex_file(hex_file_path)
				# print(ll)
				# while(ll):
				# 	ll = get_next_line_from_hex_file(hex_file_path)
				# 	print(ll[0:-1])

				# print("Done!!")

				# print(ser.readline().decode())
				# i=5
				# while(i!=0):
				# 	i-=1
				# 	print(ser.read().decode(), end = "")

				# print("DONE2")
				# print("Response from MCU:")
				# print(ser.read(size=1))
				# time.sleep(0.2)


				# mpu_value = None
				# extract_data_from_line()
				# if avr_data.find(mpu_value_start) == 0:
				# 	mpu_value = int(avr_data[len(mpu_value_start):-1]+mpu_value_start[-1])

				# print avr_data, # uncomment this to return to original

				# if mpu_value is not None:
				#         return mpu_value
						# print "numeric value = ", mpu_value

		except Exception as e:
			ser.close()
			print ("disconnection reason - ", str(e))
			ser.is_open = False
			print ("disconnected, waiting...")
			pass
