import sys
import time
import struct
import requests
import json

# :10778000F1CF86957105610508940895E894BB27AB
# :0E77900066277727CB0197F90895F894FFCF6D
# :040000030000700089
# :00000001FF
# main hex file path - /Users/aadityasharma/working/atmega_328p_projects/workspace/general_testing/main_compiled/main.hex

ESP_URL = 'http://192.168.1.7'
SERIAL_RESPONSE_OK = 'a'
LAST_LINE_IN_HEX = ':00000001FF'
END_OF_LINE = 'e'
START_CHAR = ':'
END_CHAR = ';'
hex_fd = None
ser = None


def send_esp(data):

	header = {"Content-Type": "application/json"}
	sess = requests.session()
	while True:
		try:
			response = sess.post(ESP_URL, data=data, headers=header, timeout=10)
			time.sleep(0.3)
			break
		except requests.exceptions.ReadTimeout:
			if LAST_LINE_IN_HEX in data:
				print("Sent line %s!" % data)
				print("Done!")
				exit(0)
				return
			print("TIMEOUT!")
			pass
		except requests.exceptions.ConnectionError:
			print("CONNECTION ERROR!")
			pass

	assert response.content.decode() == data


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
	
	return line.rstrip('\n')


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
	char_write(START_CHAR)
	validate_response_from_mcu()
	int_write(line_data['address_high'])
	validate_response_from_mcu()
	int_write(line_data['address_low'])
	validate_response_from_mcu()
	int_write(line_data['byte_count'])
	validate_response_from_mcu()
	for data in line_data['data']:
		int_write(data)
		validate_response_from_mcu()

	char_write(END_OF_LINE)
	return True

def wireless_upload_line_to_mcu(line):

	send_esp(line)


	
if __name__ == '__main__':


	# send_esp("aaditya")
	# exit(0)
	# for i in range(10):
	# 	send_esp(":100000000C9434000C9451000C9451000C94510049|:100000000C9434000C9451000C9451000C94510049")

	# exit(0)



	if len(sys.argv) < 2:
		raise Exception("Usage - python serial_write.py <hex_file_path>\n")

	hex_file_path = sys.argv[1]
	# hex_file_path = '/Users/aadityasharma/working/atmega_328p_projects/workspace/general_testing/main_compiled/main.hex'
	# print(extract_data_from_line(get_next_line_from_hex_file(hex_file_path)))

	# exit(0)

	# while upload_line_to_mcu(get_next_line_from_hex_file(hex_file_path)):
	# 	print("Sent the line - %d" %line_num)
	# 	line_num += 1
	i = 0
	while True:
		
		line1 = get_next_line_from_hex_file(hex_file_path)
		if not line1:
			line1 = LAST_LINE_IN_HEX
			line2 = LAST_LINE_IN_HEX

		else:
			line2 = get_next_line_from_hex_file(hex_file_path)
			if not line2:
				line2 = LAST_LINE_IN_HEX

		line = line1 + '|' + line2
		wireless_upload_line_to_mcu(line)

		print("Sent line %s!" % line)
		i += 1
		if line1 == LAST_LINE_IN_HEX or line2 == LAST_LINE_IN_HEX:
			break


































