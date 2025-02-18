GC_POLICY_ENUM = {'FIFO':0, 'greedy':1, 'cost-benefit':2}


# trace file name
FNAME = 'Default_trace.csv'

# SSD parameters
PAGE_SIZE = 512 * 8
PAGES_PER_BLOCK = 512
BLOCKS_PER_SSD = 512 * 1 * 8 * 20
GC_TRHESHOLD = 0.75
GC_TRHESHOLD_HIGH = 0.95
OVER_PROVISIONING_SPACE = 0.25
GC_POLICY = GC_POLICY_ENUM['greedy']


# About Workloads
WRITE_REQUEST_COUNT = 0


# About WA
USER_WRITE = 0
GC_WRITE = 0
GARBAGE_COLLECTION_COUNT = 0