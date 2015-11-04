#!/usr/bin/env python
'''
Pymodbus Server
--------------------------------------------------------------------------
'''
#---------------------------------------------------------------------------# 
# import the various server implementations
#---------------------------------------------------------------------------# 


from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer


#---------------------------------------------------------------------------# 
# import the twisted libraries we need
#---------------------------------------------------------------------------# 
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

import logging


class PyServer:



    def updatingWriter(a):
        context  = a[0]
        # So, we put logic here to read and update various registers...

        # Extract the motor commands        
        #
        self.logger.debug("updating the motor positions")

        print 'lelelel'

        self.logger.debug("Current Command")
        cmdReg   = 6
        slave_id = 1
        address  = 0x00
        value    = context[slave_id].getValues(cmdReg, address, count=1)

        self.logger.debug("Value: " + str(value))
        
        self.logger.debug("updating the context")
        
        register = 4
        slave_id = 0x01
        address  = 0x00
        values   = context[slave_id].getValues(register, address, count=5)
        values   = [v + 1 for v in values]
        self.logger.debug("new values: " + str(values))
        context[slave_id].setValues(register, address, values)
        

    #---------------------------------------------------------------------------# 
    # define your callback process
    #---------------------------------------------------------------------------# 
    def updatingThread(context, function = updatingWriter, delay = 1):
        ''' A worker process that runs every _delay_ seconds and
        updates live values of the context.
        '''
        from twisted.internet.task import LoopingCall
        from twisted.internet import reactor
        
        lp = LoopingCall(f=function, a=(context,))
        lp.start(delay, now=False) 
        
        reactor.run()


    '''
    Completion of this function will allow us to configure the server from a txt file.
    Unecessary at present
    def loadArgs(argDoc)
        f = open(argDoc, 'r')
        for line in f:
            args = line.split(' ')
            methodToCall = getattr(this, 'set' + args[0])
            this.methodToCall(args[1])
    '''
    #---------------------------------------------------------------------------# 
    # run the processes upon initialisation of the server
    #---------------------------------------------------------------------------# 
    def init():
        # Start running the context updater thread

        self.updateThread.start()


        # Start running the server thread
        #servThread = Thread(target= StartSerialServer(context, framer=ModbusRtuFramer,identity=identity, port='/dev/ttyS0', timeout=0.01, baudrate=9600))

        self.servThread.start()

    def preinit(self):
        from threading import Thread
        from pymodbus.server.sync import StartSerialServer
        from pymodbus.transaction import ModbusRtuFramer
        print 'lelelelelel'
        self.updateThread = 'lel'
        #Initialise threads
        self.updateThread = Thread(target=self.updatingThread, args=(self.context,))
        self.updateThread.daemon = True
        print self.baudrate
        self.servThread = Thread(target=StartSerialServer(self.context, framer=ModbusRtuFramer,identity=self.identity, port=self.port, timeout=self.timeout, baudrate=self.baudrate))
        print self.baudrate
        self.servThread.daemon = True


    #---------------------------------------------------------------------------# 
    # configure the service logging
    #---------------------------------------------------------------------------# 

    logging.basicConfig(filename="logfile.txt")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)


    updateThread = []
    servThread = []


    #---------------------------------------------------------------------------# 
    # initialize server args
    #---------------------------------------------------------------------------# 
    framer   = ModbusRtuFramer
    port     = '/dev/ttyS0'
    timeout  = 0.01
    baudrate = 9600

    #---------------------------------------------------------------------------# 
    # initialize data store
    #---------------------------------------------------------------------------# 
    store = ModbusSlaveContext(
        di = ModbusSequentialDataBlock(0, [17]*100),
        co = ModbusSequentialDataBlock(0, [17]*100),
        hr = ModbusSequentialDataBlock(0, [17]*100),
        ir = ModbusSequentialDataBlock(0, [17]*100))
    context = ModbusServerContext(slaves=store, single=True)

    #---------------------------------------------------------------------------# 
    # initialize server information
    #---------------------------------------------------------------------------# 
    identity = ModbusDeviceIdentification()
    identity.VendorName  = 'Rubicon'
    identity.VendorUrl   = 'http://rubiconwater.com'
    identity.ProductName = 'Rubicon Modbus Server'
    identity.ModelName   = 'Rotork Server'
    identity.MajorMinorRevision = '1.0'


#p.servThread = Thread(target=StartSerialServer, args=(p.context, framer=ModbusRtuFramer,identity=p.identity, port=p.port, timeout=p.timeout, baudrate=p.baudrate))
