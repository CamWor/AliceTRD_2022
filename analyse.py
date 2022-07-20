from ast import Try
from socket import socket
import zmq

context = zmq.Context()
daq = context.socket(zmq.REP)
daq.bind('tcp://*:7770')
print('Waiting for wake-up command ...\n')
data  =daq.recv_string()
print(data)

daq.send_string('Ready to analyse')








