commands used till now:

ESP-01 connections:
normal connections (chp_pd/rst/vcc to positive, GND/GPIO0 to GND, RX/TX to TX/RX of FTDI) (power up only when the wires have been connected)
erase esp-01:
esptool.py --port <port> erase_flash
write bin file to esp-01:
esptool.py -p <port> write_flash 0x000000 ~/Downloads/ESP_8266_v0.9.2.2_AT_Firmware.bin -fm dout

to compile c/cpp file:
cd /Users/aadityasharma/working/atmega_328p_projects/workspace/<where the C file is located>
../comile.sh <c file>

to upload the compiled file using usbasp:
cd /Users/aadityasharma/working/atmega_328p_projects/workspace/<where the C file is located>
../upload_usbasp.sh <c_file>_compiled/<c_file>.hex

serial read using screen:
screen -L /dev/cu.usbserial-A50285BI 9600
