from ast import Try
from socket import socket
import zmq
import numpy as np
# context = zmq.Context()
# daq = context.socket(zmq.REP)
# daq.bind('tcp://*:7770')
# print('Waiting for wake-up command ...\n')
# data  =daq.recv_string()
# print(data)

# daq.send_string('Ready to analyse')

     
def parseFile(fName, headerLen=2):   #Parse file of: osc data where the first row is the timesstamp of the measurement, the second row is channel 1 and the 3rd row is channel 2. this then repeats
    count = 0
    f = open(fName)
    for line in f:
        count += 1 
    count -= headerLen
    f.close()
    numEvents = int(count/3)
    timeStamp, channel1, channel2 =np.zeros(numEvents),np.zeros(numEvents),np.zeros(numEvents)
    events = []

    f = open(fName)
    for x in range(headerLen):
        header = f.readline()
    x=0
    for x in range(numEvents):  
        timestamp = f.readline(3*x)
        channel1 = f.readline(3*x+1)
        channel2 = f.readline(3*x+2)
        events.append({"timeStamp":timeStamp,"channel1":channel1,"channel2":channel2 })

    return events


print(parseFile("scopeData.csv"))




