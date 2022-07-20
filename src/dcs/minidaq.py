#Edited 2022 by Cameron Worthington t include readdso function to read the osclloscope and pass data aong to analyse.py


import click
import zmq
from oscilloscopeRead import scopeRead


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


@minidaq.command()
@click.pass_context
def readevent(ctx):

    ctx.obj.analyse.send_string("Wake")
    print(ctx.obj.analyse.recv_string())

    ctx.obj.trdbox.send_string(f"write 0x08 1") # send trigger
    print(ctx.obj.trdbox.recv_string())

    ctx.obj.sfp1.send_string("read")
    data = ctx.obj.sfp1.recv()
    print(len(data))

@minidaq.command()
@click.pass_context
def readdso(ctx):
    waveform = ctx.obj.scope.getData([1,2], save_png=True)
    print(waveform)
