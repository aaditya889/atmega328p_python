#from serial_write import extract_data_from_line

#line = ':10010000214601360121470136007EFE09D2190140'

#print(extract_data_from_line(line))


import os 
file = '/Users/aadityasharma/working/atmega_328p_projects/workspace/esp01_server/test_wireless_compiled/test_wireless.hex'
previous = -2
words = list()
hex_data = list()

with open('screenlog.0', 'rb') as fd:
	
	line = fd.readline()
	while line:
		
		try:	
			if 'Ad' in line.decode():
				address = int(line.decode().split('Ad: ')[1][0:-1])
				if address == previous + 2:
					# print("true")
					previous = address
				else:
					print("false!!")
					exit(1)
			if 'wo' in line.decode():
				word = int(line.decode().split('wo: ')[1][0:-1])
				# print("word - %s" % '0x{0:0{1}X}'.format(word, 4))
				words.append(word)

			if 'Clr' in line.decode():
				clear = int(line.decode().split('Clr: ')[1][0:-1])
				print("clear - %d " % clear)
			if 'bu' in line.decode():
				burn = int(line.decode().split('bu: ')[1][0:-1])
				print("burn - %d " % burn)

			line = fd.readline()
		except UnicodeDecodeError:
			break

print("WORDS:\n ", words)

with open(file, 'r') as fd:
	line = fd.readline()

	while line:
		line = line.split(':')[1]
		# print(line.split(':')[1])
		bytes = int(line[0:2], 16)
		f_data = line[8:8 + bytes*2]
		i = 0

		for dat in range(round(bytes/2)):
			low = int(f_data[i:i+2], 16)
			high = int(f_data[i+2:i+4], 16)
			l_data = low & 0xff
			l_data = ((high << 8) | l_data)
			# print(l_data)
			hex_data.append(l_data)
			i += 4

		# print('line - %s' % line[0:-1])
		# print('data - %s\n' % f_data)
		line = fd.readline()

print("HEX: \n", hex_data)

print(hex_data == words)
