import FTL
import SSD_Exceptions
import Statistics as st


def simulation(fname, page_size, pages_per_block, blocks_per_ssd, gc_threshold, ops):
    SSD = FTL.FTL(page_size, pages_per_block, blocks_per_ssd, gc_threshold, ops)

    with open(fname, 'r') as f:
        for line in f.readlines():
            lba, size = map(int, line.split())
            
            try:
                SSD.write(lba, size * 512)
            except SSD_Exceptions.CapacityException as e:
                print(e)
                exit(1)
    
    print('Simulation Result')
    print(f'Write Requests : {st.WRITE_REQUEST_COUNT}')
    print(f'WAF : {(st.GC_WRITE + st.USER_WRITE) / st.USER_WRITE}')
            



if __name__ == '__main__':
    simulation(st.FNAME, st.PAGE_SIZE, st.PAGES_PER_BLOCK, st.BLOCKS_PER_SSD, st.GC_TRHESHOLD, st.OVER_PROVISIONING_SPACE)