#Edited 2022 by Cameron Worthington t include readdso function to read the osclloscope and pass data aong to analyse.py


import click
import zmq
import csv
from oscilloscopeRead import scopeRead
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

class zmq_env:
    def __init__(self):

        self.context = zmq.Context()

        self.trdbox = self.context.socket(zmq.REQ)
        self.trdbox.connect('tcp://localhost:7766')

        self.sfp0 = self.context.socket(zmq.REQ)
        self.sfp0.connect('tcp://localhost:7750')

        self.sfp1 = self.context.socket(zmq.REQ)
        self.sfp1.connect('tcp://localhost:7751')

        self.analyse = self.context.socket(zmq.REQ)
        self.analyse.connect('tcp://localhost:7770')

        self.scope = scopeRead.Reader('ttyACM1')



@click.group()
@click.pass_context
def minidaq(ctx):
    ctx.obj = zmq_env()




from datetime import datetime
import os
from re import T
import signal
import time
import click
import zmq
import oscilloscopeRead.scopeRead as scopeRead
import multiprocessing
from time import sleep, time
import struct

class zmq_env:
    def __init__(self):

        self.context = zmq.Context()

        self.trdbox = self.context.socket(zmq.REQ)
        self.trdbox.connect('tcp://localhost:7766')

        self.sfp0 = self.context.socket(zmq.REQ)
        self.sfp0.connect('tcp://localhost:7750')

        self.sfp1 = self.context.socket(zmq.REQ)
        self.sfp1.connect('tcp://localhost:7751')


@click.group()
@click.pass_context
def minidaq(ctx):
    ctx.obj = zmq_env()


@minidaq.command()
@click.option('--n_repeats','-n', default=1, help='Number of repeats of the experiment')
@click.option('--n_duration','-t', default=60, help='time in seconds for experiment')
@click.option('--filename','-f', default="scopeData", help='File name of oscilloscope data file without type')
@click.pass_context

def trigger_read(ctx, n_duration, n_repeats, filename):
    #print(f'n_events: {n_events}')
    repeatfilename = filename +".csv"
    f =open(repeatfilename, 'w')
    write = csv.writer(f)
    write.writerow([f"Number of coincidences for an interval of {n_duration} s repeated {n_repeats} times"])
    ExperimentStart = datetime.timestamp(datetime.now())
    write.writerow([ExperimentStart])
    #write.writerow(['peak of Ch 1', 'Peak of Ch 2', 'seconds since start of experiment'])

        
    print(f'duration: {n_duration} s')
    #scopeReader = scopeRead.Reader("ttyACM1")
    for z in range(n_repeats):
        # try:
        #     repeatfilename = "scopeData/"+filename +f"_{z}.csv"
        # except:
        #     print("Make sure there is a directory called '/scopeData'")
        # print(f'duration: {n_duration} s')
        #scopeReader = scopeRead.Reader("ttyACM1")
        startTime=  datetime.timestamp(datetime.now())
        runEndTime = startTime+n_duration
        # with open(repeatfilename, 'w') as f:
        #     write = csv.writer(f)
        #     write.writerow([n_duration])
        #     write.writerow([startTime])
        # f.close()

        #run_period = time.time() + 60*0.5 #How long you want to search for triggers for
        # trig_count_1 = int(os.popen('trdbox reg-read 0x102').read().split('\n')[0])

        ctx.obj.trdbox.send_string("read 0x102")
        trig_count_1 = int(ctx.obj.trdbox.recv_string(), 16)
        print(f'Trigger count before waiting: {trig_count_1}')

        trig_count_2 = 0
        i = 0
        #maxval =[]
        ctx.obj.trdbox.send_string("write 0x103 1")
        print(f'{ctx.obj.trdbox.recv_string()}: Unblocked, waiting for trigger...')

        while datetime.timestamp(datetime.now()) < runEndTime:
            ctx.obj.trdbox.send_string("read 0x102")
            trig_count_2 = int(ctx.obj.trdbox.recv_string(), 16)

            if trig_count_2 != trig_count_1:
                #print(f'i: {i}')
                
                i += 1

                # try:
                #     maxval.append(read_scope(scopeReader, datetime.timestamp(datetime.now())-ExperimentStart))
                # #     #ctx.invoke(readevent)
                # #     # print('Reading event')
                # #     timeRead = datetime.timestamp(datetime.now())-startTime

                # #     read_scope(scopeReader, repeatfilename,  timeRead)
                # #     #ctx.invoke(readdso)
                
                # except: 
                #     maxval.append([0,0,datetime.timestamp(datetime.now())-ExperimentStart])
                #     pass

                ctx.obj.trdbox.send_string("read 0x102")
                trig_count_1 = int(ctx.obj.trdbox.recv_string(), 16)
                #print(f'New trigger count after event: {trig_count_1}')
                ctx.obj.trdbox.send_string("write 0x103 1")
                rec =ctx.obj.trdbox.recv_string()
               # print(f'{rec}: Unblocked, waiting for trigger...')
            else:
                pass
        write.writerow([i])        
        #write.writerows(maxval)
        print(f"repeat {z}/{n_repeats} completed") 
    f.close()       
    print('Done looking for triggers, quitting...')



# @minidaq.command()
# @click.pass_context
# def readevent(ctx):
#     scopeReader = scopeRead.Reader("ttyACM1")
#     # ctx.obj.trdbox.send_string(f"write 0x103 1") # unblocks
#     # ctx.obj.trdbox.send_string(f"write 0x08 1") # send trigger
#     ctx.obj.trdbox.send_string("write 0x103 1")
#     #print(f'{ctx.obj.trdbox.recv_string()}: Unblocked, waiting for trigger...')
#     test = ctx.obj.trdbox.recv_string()
#     ctx.obj.sfp0.send_string("read")
#     chamber_1 = ctx.obj.sfp0.recv()

#     ctx.obj.sfp1.send_string("read")
#     chamber_2 = ctx.obj.sfp1.recv()

#     print(len(chamber_1) + len(chamber_2))



#     f = open("data", "wb")
#     f.write(chamber_1)
#     f.write(chamber_2)
#     f.close()
#     temp =read_scope(scopeReader)
#     print('Done')


def read_scope(reader, timeStamp=0):

    waveforms = reader.getData([1,2], save_png=True)
    f = open('scopeData.csv', 'w')
    # with open(filename, 'a') as f:
    #     write = csv.writer(f)
    #     write.writerow([timeStamp])
    #     write.writerow(waveforms[0])
    #     write.writerow(waveforms[1])
    f.write("ch1,ch2\n")
    for i in range(len(waveforms[0])):

        f.write(f"{waveforms[0][i]},{waveforms[1][i]}\n")
    f.close()
    return ([np.min(waveforms[0]),np.min(waveforms[1]),timeStamp])

@minidaq.command()
@click.pass_context
def old_readevent(ctx):

    #ctx.obj.analyse.send_string("Wake") # -------------added as a test message on 20 July 2022-------
    #print(ctx.obj.analyse.recv_string())


    ctx.obj.trdbox.send_string(f"write 0X103 1") # ublock trigger
    print(ctx.obj.trdbox.recv_string())

    ctx.obj.sfp1.send_string("read")
    data = ctx.obj.sfp1.recv()
    print(len(data))
    f = open('data', 'wb')
    f.write(data)

@minidaq.command()
@click.pass_context
def readdso(ctx):
    #ctx.obj.trdbox.send_string(f"write 0X103 1") # ublock trigger

    #print(ctx.obj.trdbox.recv_string())
    waveform = ctx.obj.scope.getData([1,2], save_png=True)
    print(waveform)

@minidaq.command()
@click.option('--scinid','-i', default=0, help='scintillator to optimise (1 or 0)')
@click.option('--filename','-f', default='', help='filename to save the muon rate as a func of threshold (if none then no image saved)')
@click.option('--n_repeats','-n', default=3, help='File name of oscilloscope data file without type')
@click.pass_context
def findoptthr(ctx, scinid, filename, n_repeats):
    ctx.obj.trdbox.send_string(f"write 0X101 0x10121012") # set up dgg
    rec = ctx.obj.trdbox.recv_string()
    if scinid==0:
        ctx.obj.trdbox.send_string(f"write 0X100 0x00000204") # set up discriminator
        
    elif scinid == 1:
        ctx.obj.trdbox.send_string(f"write 0X100 0x00000404") # set up discriminator
    else:
        print("Enter valid scintillator ID (0 or 1)")
        exit
    print(ctx.obj.trdbox.recv_string())
    arrCounts = []
    arrThresh = []
    progress = 0
    for i in range(2000, 2070):
        progress+=1
        su736_dis_base = 0x280 #from trdbox.py
        value = ( (scinid&1) << 14 ) | ( i & 0xFFF )
        ctx.obj.trdbox.send_string(f"write {su736_dis_base+0x08} {value}")
        rec = ctx.obj.trdbox.recv_string()
        print(f"{progress}/140")
        arrLocalCounts = []
        for x in range(n_repeats):
            ctx.obj.trdbox.send_string("read 0x102")
            trig_count_1 = int(ctx.obj.trdbox.recv_string(), 16)
            sleep(10)
            
            ctx.obj.trdbox.send_string("read 0x102")
            trig_count_2 = int(ctx.obj.trdbox.recv_string(), 16)
            arrLocalCounts.append(trig_count_2- trig_count_1)
        ave = np.average(arrLocalCounts)
        #print(f'num counts for threshold {i} in 10s: {ave}')
        arrCounts.append(ave)
        arrThresh.append(i)

    optThresh =arrThresh[ arrCounts.index(max(arrCounts))]
    print(arrThresh)
    print(arrCounts)
    plt.plot(arrThresh, arrCounts)
    plt.xlabel("threshold value")
    plt.ylabel("number of muon events recorded in 10s")
    plt.title(f"Optimal Threshold = {optThresh}")
    plt.draw()
    print(f"Optimal Threshold = {optThresh}")
    try:
        plt.savefig(filename)
    except:
        pass
# @minidaq.command()
# def dis_thr(ch, thresh): #stolen from trdbox.py

# -------------------------------------STEPHAN Minidaq-----------------------------------

def get_pretrigger_count(trdbox):
    trdbox.send_string("read 0x102")
    cnt = int(trdbox.recv_string(), 16)
    # print(cnt)
    return cnt

def wait_for_pretrigger(trdbox, interval=0.1):
    cnt = get_pretrigger_count(trdbox)
    while get_pretrigger_count(trdbox) <= cnt:
        sleep(interval)

def gen_event_header(payloadsize):
    """Generate MiniDaq header"""
    ti = time()
    tis = int(ti)
    tin = ti-tis
    return struct.pack("<LBBBBBBHLL", 
        0xDA7AFEED, # magic
        1, 0, # equipment 1:0 is event
        0, 1, 0, # reserved / header version / reserved
        20, payloadsize, # header, payload sizes
        hex(tis), hex(int(tin))# time stamp
    )

@minidaq.command()
@click.pass_context
def readevent(ctx):

    outfile = open("data.bin", "wb")

    # -------------------------------------------------------------
    # trigger
    scopeReader = scopeRead.Reader("ttyACM1")
    # ctx.obj.trdbox.send_string(f"write 0x08 1") # send trigger
    ctx.obj.trdbox.send_string(f"trg unblock") # send trigger
    print(ctx.obj.trdbox.recv_string())

    wait_for_pretrigger(ctx.obj.trdbox, 0.5)

    # -------------------------------------------------------------
    # readout

    # define the equipments that should be read out
    eqlist = [ctx.obj.sfp1, ctx.obj.sfp0]

    # send query for data to all equipments
    for eq in eqlist:
        eq.send_string("read")

    # receive the data
    data = list(eq.recv() for eq in eqlist)

    # -------------------------------------------------------------
    # build event and write to file

    evdata = bytes()#gen_event_header(payloadsize = sum(len(i) for i in data))
    for segment in data:
        evdata += segment
        # print(len(segment),outfile.tell())

    outfile.write(evdata)
    
    # print("total:", len(evdata))

    temp =read_scope(scopeReader)
    outfile.close()