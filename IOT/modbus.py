from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusTcpClient

import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

ip_address= 'localhost'   #Enter ip address of ethernet converter here

def read_float(address,quant,slave_id,limit):
    curr_reg=address
    while(curr_reg<=limit):
        result=client.read_holding_registers(address=curr_reg,count=quant,unit=slave_id)
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big, wordorder=Endian.Little)
        decoded=decoder.decode_32bit_float()
        print("Value in reg "+str(curr_reg)+" is "+str(decoded))
        curr_reg=curr_reg+quant

def read_long(address,quant,slave_id,limit):
    curr_reg=address
    while(curr_reg<=limit):
        result=client.read_holding_registers(address=curr_reg,count=quant,unit=slave_id)
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big, wordorder=Endian.Little)
        decoded=decoder.decode_32bit_uint()
        print("Value in reg "+str(curr_reg)+" is "+str(decoded))
        curr_reg=curr_reg+quant

def read_long_four(address,quant,slave_id,limit):
    curr_reg=address
    while(curr_reg<=limit):
        result=client.read_holding_registers(address=curr_reg,count=2,unit=slave_id)
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big, wordorder=Endian.Little)
        decoded=decoder.decode_32bit_uint()
        print("Value in reg "+str(curr_reg)+" is "+str(decoded))
        curr_reg=curr_reg+quant



def run_sync_client(unit):
    client = ModbusClient(ip_address, port=502) #Enter TCP/IP Port value for port parameter
    client.connect()
    read_float(address=43901,quant=2,slave_id=unit,limit=43966)
    read_long_four(address=43995,quant=4,slave_id=unit,limit=44000)
    read_float(address=43001,quant=2,slave_id=unit,limit=43016)
    read_long(address=43019,quant=2,slave_id=unit,limit=43020)
    read_float(address=43031,quant=2,slave_id=unit,limit=43046)
    read_long(address=43049,quant=2,slave_id=unit,limit=43050)
    read_float(address=43061,quant=2,slave_id=unit,limit=43076)
    read_long(address=43079,quant=2,slave_id=unit,limit=43080)
    read_float(address=43091,quant=2,slave_id=unit,limit=43106)
    read_long(address=43109,quant=2,slave_id=unit,limit=43110)
    read_float(address=43121,quant=2,slave_id=unit,limit=43126)
    read_float(address=43131,quant=2,slave_id=unit,limit=43132)
    read_long(address=43139,quant=2,slave_id=unit,limit=43140)
    client.close()

if __name__ == "__main__":
    slave_id=1 #Enter Slave id
    while(slave_id <= 500):
        run_sync_client(slave_id)
        slave_id=slave_id + 1 
