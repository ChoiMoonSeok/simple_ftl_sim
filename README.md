# simple_ftl_sim
- This Simulator only simulate over provisioning space and page mapping.
- You can change trace file and parameters at Statistics.py.

## About source code
- FTL.py
- Simulation.py : Read and run thr trace from file.
- FTL.py : Define FTL
- Block.py : Define Block
- Page.py : Define Page
- Trace_Generation.py : create io trace generator
- 


## How to run
- Create trace file which is include LBA and request size(in bytes)
- Set the trace file name and SSD parameters at Statistics.py

## trace file example
Opcode(W or R), lba(int), size(bytes)


W, 1234, 1024


W, 1245, 2048
