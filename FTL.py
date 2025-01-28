from collections import deque
from math import ceil

import SSD_Exceptions
import Block
import Statistics as st

class FTL:

    def __init__(self, page_size, pages_per_block, blocks_per_ssd, gc_threshold, gc_threshold_high, gc_policy, ops):
        
        self.page_size = page_size
        self.pages_per_block = pages_per_block
        self.blocks_per_ssd = blocks_per_ssd
        self.capacity = page_size * pages_per_block * blocks_per_ssd

        self.gc_threshold = gc_threshold
        self.gc_threshold_high = gc_threshold_high
        self.gc_policy = gc_policy

        self.ops = ops
        self.free_block_count = blocks_per_ssd

        self.blocks = [Block.Block(pages_per_block, i) for i in range(blocks_per_ssd)]

        self.free_block_que = deque([i for i in range(blocks_per_ssd)])
        if gc_policy == 0:
            self.sealed_block_que = deque([])
        else:
            self.sealed_block_que = []

        self.write_pointer = self.allocate_block()

        
        # Values for Mapping LBA to ppn
        self.lpn_que = deque([i for i in range(blocks_per_ssd * pages_per_block)])

        self.lba_to_lpn = dict()
        self.lpn_to_ppn = dict()

        self.ppn_to_lpn = dict()
        self.lpn_to_lba = dict()

        print('Start SSD simulation with ' + st.FNAME + ' trace.')
        print('Prameters')
        print(f'Page Size : {self.page_size}')
        print(f'Pages Per Block : {self.pages_per_block}')
        print(f'Blocks Per SSD : {self.blocks_per_ssd}')
        print(f'SSD Capacity : {self.capacity / 1024 / 1024 / 1024} Giga Bytes')
        print(f'GC Threshold : {self.gc_threshold}')
        print(f'GC Threshold High : {self.gc_threshold_high}')
        print(f'Over Provisioning Space : {self.ops}')
        print('-' * 50)

        
    def process(self, opcode, lba, size):
        if opcode == 'W' or opcode == 'w':
            st.WRITE_REQUEST_COUNT += 1
            self.write(lba, size)
        elif opcode == 'R' or opcode == 'r':
            self.read(lba, size)


    def allocate_block(self):
        self.free_block_count -= 1

        return self.free_block_que.popleft()


    def read(self, lba, size):
        pass


    def write(self, lba, size):
        '''
        lba : logical block address
        size : write request size(bytes)
        '''
        
        cnt = 0
        if (self.free_block_count) < (self.blocks_per_ssd * (1 - 1 * (1 - self.ops) * self.gc_threshold_high)):

            cnt += 1
            while (self.free_block_count) < (self.blocks_per_ssd * (1 - 1 * (1 - self.ops) * self.gc_threshold)):
                self.garbage_collection()
                if cnt > (self.blocks_per_ssd * (1 - self.gc_threshold * (1 - self.ops))):
                    raise SSD_Exceptions.CapacityException

        # 해당 LBA가 사용된 적이 있는 경우, 할당된 lpn과 ppn을 삭제
        # If LBA has been used, remove allocated lpn and ppn
        if lba in self.lba_to_lpn:
            for lpn in self.lba_to_lpn[lba]:
                self.lpn_que.append(lpn)

                ppn = self.lpn_to_ppn[lpn]

                self.blocks[ppn // self.pages_per_block].invalidate_page(ppn)

                self.ppn_to_lpn.pop(ppn)
                self.lpn_to_ppn.pop(lpn)
                self.lpn_to_lba.pop(lpn)

            self.lba_to_lpn.pop(lba)

        page_count = ceil(size / self.page_size)

        self.lba_to_lpn[lba] = [self.lpn_que.popleft() for _ in range(page_count)]

        for lpn in self.lba_to_lpn[lba]:

            self.lpn_to_lba[lpn] = lba

            self.write_page(lpn)
            st.USER_WRITE += 1


    def write_page(self, lpn):
        blk_write_pointer, page_id = self.blocks[self.write_pointer].write_page()

        self.lpn_to_ppn[lpn] = page_id
        self.ppn_to_lpn[page_id] = lpn


        if blk_write_pointer == self.pages_per_block - 1:
            self.sealed_block_que.append(self.write_pointer)
            self.write_pointer = self.allocate_block()



    def select_victim_FIFO(self):
        return self.sealed_block_que.popleft()
    

    def select_victim_greedy(self):
        most_invalid = 0
        most_invalid_blk = None
        for i in range(len(self.sealed_block_que)):
            if self.blocks[i].invalid_page_count > most_invalid:
                most_invalid = self.blocks[i].invalid_page_count
                most_invalid_blk = i
                if most_invalid == st.PAGES_PER_BLOCK:
                    break

        return self.sealed_block_que.pop(most_invalid_blk)
            


    def gc_write(self, lpn):
        st.GC_WRITE += 1
        self.write_page(lpn)


    def garbage_collection(self):
        if self.gc_policy == 0:
            self.FIFO()
        elif self.gc_policy == 1:
            self.greedy()
        elif self.gc_policy == 2:
            self.cost_benefit()
        

    
    def FIFO(self):
        victim = self.select_victim_FIFO()
        self.free_block_que.append(victim)
        self.free_block_count += 1

        for ppn in self.blocks[victim].delete_block():
            self.gc_write(self.ppn_to_lpn[ppn])
    

    def greedy(self):
        victim = self.select_victim_greedy()
        self.free_block_que.append(victim)
        self.free_block_count += 1

        for ppn in self.blocks[victim].delete_block():
            self.gc_write(self.ppn_to_lpn[ppn])
        


    def cost_benefit(self):
        pass