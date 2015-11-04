#!/usr/bin/env python
'''
Pymodbus Server With Updating Thread
--------------------------------------------------------------------------

This is an example of having a background thread updating the
context while the server is operating. This can also be done with
a python thread::

    from threading import Thread

    thread = Thread(target=updating_writer, args=(context,))
    thread.start()
'''

#---------------------------------------------------------------------------# 
# import the various server implementations
#---------------------------------------------------------------------------# 
from pymodbus.server.sync import StartTcpServer
from pymodbus.server.sync import StartUdpServer
from pymodbus.server.sync import StartSerialServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

from pymodbus.transaction import ModbusRtuFramer

#---------------------------------------------------------------------------# 
# import the twisted libraries we need
#---------------------------------------------------------------------------# 
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
#---------------------------------------------------------------------------# 
# configure the service logging
#---------------------------------------------------------------------------# 
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)


import time



#---------------------------------------------------------------------------# 
# define your callback process
#---------------------------------------------------------------------------# 
def updatingThread(context):
    ''' A worker process that runs every so often and
    updates live values of the context. It should be noted
    that there is a race condition for the update.

    :param arguments: The input arguments to the call
    '''
    delay = 1 # 5 seconds delay
    lp = LoopingCall(f=updating_writer, a=(context,))
    lp.start(delay, now=False) 
    
    reactor.run()

def updating_writer(a):



    context  = a[0]
    # So, we put logic here to read and update various registers...

    # Extract the motor commands        
    #
    log.debug("updating the motor positions")

    log.debug("Current Command")
    cmdReg   = 0x03
    slave_id = 0x01
    address  = 0x00
    value    = context[slave_id].getValues(cmdReg, address, count=10)

    log.debug("Value: " + str(value))



    context  = a[0]
    # So, we put logic here to read and update various registers...

    # Extract the motor command and update the position accordingly.   
    #

    nSlaves = 5
    slaveNos = [0x01, 0x02, 0x03, 0x04, 0x05]

    #mm per second of movement from gate
    ROCslave = [220, 200, 350, 210, 400]

    prevCommand = [0, 0, 0, 0, 0]
    prevCommandTime = [0, 0, 0, 0, 0]

    pCom = [0, 0, 0, 0, 0]

    index = 0
    for slave in slaveNos:
        pCom[index] = context[slave].getValues(0x03, 0, count=1)
        index += 1
        #log.info("E:" + str(context[slave].getValues(0x03, 0, count=1)))
        #log.info("C:" + str(slave))
    log.info("Command is: " + str(pCom))

    index = -1
    for slave in slaveNos:
        index += 1
        command = context[slave].getValues(0x03, 0, count=1)

        #Up
        if command == 1:
            if prevCommand[index] == 1:
                currTime = time.time()
                deltaT = currTime - prevCommandTime[index]
                prevCommandTime[index] = currTime
                #Check where you're writing and reading from
                currVal = context[slave].getValues(0x04, 0x01, count=1)
                nextVal = currVal + ROCslave*deltaT
                context[slave].setValues(0x04, 0x01, values)
            else:
                prevCommandTime[index] = time.time()
                prevCommand[index] = 1

        if command == 2:
            if prevCommand[index] == 2:
                currTime = time.time()
                deltaT = currTime - prevCommandTime[index]
                prevCommandTime[index] = currTime
                currVal = context[slave].getValues(0x04, 0x01, count=1)
                nextVal = currVal - ROCslave*deltaT
                context[slave].setValues(0x04, 0x01, values)
            else:
                prevCommandTime[index] = time.time()
                prevCommand[index] = 2

        else:
            prevCommand[index] = 0
            continue

    

#---------------------------------------------------------------------------# 
# initialize your data store
#---------------------------------------------------------------------------# 
store1 = ModbusSlaveContext(
    di = ModbusSequentialDataBlock(0, [0]*100),
    co = ModbusSequentialDataBlock(0, [0]*100),
    hr = ModbusSequentialDataBlock(0, [0]*100),
    ir = ModbusSequentialDataBlock(0, [0]*100))

store2 = ModbusSlaveContext(
    di = ModbusSequentialDataBlock(0, [0]*100),
    co = ModbusSequentialDataBlock(0, [0]*100),
    hr = ModbusSequentialDataBlock(0, [0]*100),
    ir = ModbusSequentialDataBlock(0, [0]*100))

store3 = ModbusSlaveContext(
    di = ModbusSequentialDataBlock(0, [0]*100),
    co = ModbusSequentialDataBlock(0, [0]*100),
    hr = ModbusSequentialDataBlock(0, [0]*100),
    ir = ModbusSequentialDataBlock(0, [0]*100))

store4 = ModbusSlaveContext(
    di = ModbusSequentialDataBlock(0, [0]*100),
    co = ModbusSequentialDataBlock(0, [0]*100),
    hr = ModbusSequentialDataBlock(0, [0]*100),
    ir = ModbusSequentialDataBlock(0, [0]*100))

store5 = ModbusSlaveContext(
    di = ModbusSequentialDataBlock(0, [0]*100),
    co = ModbusSequentialDataBlock(0, [0]*100),
    hr = ModbusSequentialDataBlock(0, [0]*100),
    ir = ModbusSequentialDataBlock(0, [0]*100))

slaveList = {
    0x01: store1,
    0x02: store2,
    0x03: store3,
    0x04: store4,
    0x05: store5,
    }
context = ModbusServerContext(slaves=slaveList, single=False)

#---------------------------------------------------------------------------# 
# initialize the server information
#---------------------------------------------------------------------------# 
identity = ModbusDeviceIdentification()
identity.VendorName  = 'pymodbus'
identity.ProductCode = 'PM'
identity.VendorUrl   = 'http://github.com/bashwork/pymodbus/'
identity.ProductName = 'pymodbus Server'
identity.ModelName   = 'pymodbus Server'
identity.MajorMinorRevision = '1.0'



#---------------------------------------------------------------------------# 
# run the processes
#---------------------------------------------------------------------------# 
from threading import Thread

# Start running the context updater thread
updateThread = Thread(target=updatingThread, args=(context,))
updateThread.daemon = True
updateThread.start()


# Start running the server thread
servThread = Thread(target= StartSerialServer(context, framer=ModbusRtuFramer,identity=identity, port='/dev/ttyS0', timeout=0.01, baudrate=9600))
servThread.daemon = True
servThread.start()


#chill

import msvcrt as m
def wait():
    m.getch()

wait()

updateThread.stop()
servThread.stop()

