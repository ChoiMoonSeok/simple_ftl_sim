import Trace_Generation as TG
import FTL
import SSD_Exceptions
import Statistics as st


def simulation(ftl_class, fname, page_size, pages_per_block, blocks_per_ssd, gc_threshold, gc_threshold_high, gc_policy, ops):

    trace_generator = TG.DefaultTraceGenerator(fname)
    SSD = ftl_class(page_size, pages_per_block, blocks_per_ssd, gc_threshold, gc_threshold_high, gc_policy, ops)

    for io in trace_generator.trace_iter():
        try:
            SSD.process(*io)
        except SSD_Exceptions.CapacityException as e:
            print(e)
            exit(1)
    
    print('Simulation Result')
    print(f'Write Requests : {st.WRITE_REQUEST_COUNT}')
    print(f'WAF : {(st.GC_WRITE + st.USER_WRITE) / st.USER_WRITE}')
            

if __name__ == '__main__':
    simulation(FTL.FTL, st.FNAME, st.PAGE_SIZE, st.PAGES_PER_BLOCK, st.BLOCKS_PER_SSD, st.GC_TRHESHOLD, st.GC_TRHESHOLD_HIGH, st.GC_POLICY, st.OVER_PROVISIONING_SPACE)