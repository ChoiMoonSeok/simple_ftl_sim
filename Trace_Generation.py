class AbstractTraceGenerator:
    
    def __init__(self, fname):
        self.fname = fname


    def trace_iter(self):
        pass


class DefaultTraceGenerator(AbstractTraceGenerator):

    def __init__(self, fname):
        self.fname = fname

    
    def trace_iter(self):
        with open(self.fname, 'r') as f:
            for l in f.readlines():
                opcode, lba, size = l.split(sep=',')
                yield (opcode, int(lba), int(size))
