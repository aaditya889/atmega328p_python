import os
import time
fileName = 'test'
originalTime = os.path.getmtime(fileName)
fd = open(fileName, 'r')
existing = fd.read()
print(existing)
while(True):
    if(os.path.getmtime(fileName) > originalTime):
        print(fd.readline(), end='')
        originalTime = os.path.getmtime(fileName)
    time.sleep(0.1)
