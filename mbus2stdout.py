##
##from pymodbus.client.sync import ModbusSerialClient as ModbusClient
##
##client = ModbusClient(method='rtu', baudrate=9600, port='/dev/ttyS0')
###client.write_coil(1, True)
##result = client.read_coils(20,4, unit=34)
##print result.bits
##client.close()


#:00010022004C91

import datetime

from pymodbus.server.sync import StartSerialServer




#Function definitions
def writeCoils(address, value):
	client.write_coil(address, value, unit=34)
	

def readCoil(address):
	result = client.read_coils(address, unit=34)
	return result.getBit(0)

def readReg(address):
	result = client.read_holding_registers(address, unit=34)
	return result.getRegister(0)

def writeReg(address, value):
	client.write_register(address, value, unit=34)



def readCoilList(listOfRegs):
	result = []
	for reg in listOfRegs:
		result.append(readCoil(reg))
	return result

def writeCoilList(listOfRegs, listOfValues):
	while len(listOfRegs) > 0:
		reg = listOfRegs.pop()
		val = listOfValues.pop()
		writeCoils(reg, val)

def readRegList(listOfRegs):
	result = []
	for reg in listOfRegs:
		result.append(readReg(reg))
	return result

def writeRegList(listOfRegs, listOfValues):
	while len(listOfRegs) > 0:
		reg = listOfRegs.pop()
		val = listOfValues.pop()
		writeReg(reg, val)



#Setup serial interface to the RTU. 
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
client = ModbusClient(method='rtu', baudrate=9600, port='/dev/ttyS0')


#Want to:

# 1. Write arbitrary set value commands, maybe define a struct or array or something 
#    to set it up, with an arbitrary poll time
# 2. Poll certain tags on a certain duty cycle, printing output to STDOUT and a log file.

boolean = 1

listOfCoils = [5, 26, 32, 42, 54, 60, 61, 63, 67, 71, 75, 80]
listOfWR 	= [66, 75, 98, 172]
listOfVals 	= [1, 102, 1100, 800] 


file = open("output.txt", "a")

print "CTRL + C Exits!"
while True:
	#try:
		
		# Tags to write to:
		# FLOW_SP
		# CTRL_MODE
		# ???

		file.write(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + "\n")
		file.write("Coils\n")
		file.write(str(readCoilList(listOfCoils)) + "\n")
		file.write("Regs\n")
		file.write(str(readRegList(listOfRegs)) + "\n")
		
		#Do MODBUS writes
		writeRegList(listOfWR, listOfVals)
		

	#except:
	#	break

client.close()