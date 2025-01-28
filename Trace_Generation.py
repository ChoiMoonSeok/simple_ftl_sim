from abc import *

import Statistics as st


class AbstractTraceGenerator(metaClass=ABCMeta):
    
    @abstractmethod
    def __init__(self, fname):
        pass


    @abstractmethod
    def trace_iter(self):
        pass


class DefaultTraceGenerator(AbstractTraceGenerator):

    def __init__(self, fname):
        self.fname = fname

    
    def trace_iter(self):
        with open(self.fname, 'r') as f:
            for l in f.readlines():
                opcode, lba, size = map(int, l.split())
                yield (opcode, lba, size)
