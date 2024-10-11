import Page

class Block:
    '''
    Class of Block which include init, write_page, delete
    '''

    def __init__(self, pages_per_block, block_id):
        self.block_id = block_id
        self.pages_per_block = pages_per_block

        self.pages = [Page.Page(i) for i in range(block_id * pages_per_block, (block_id + 1) * pages_per_block)]
        self.write_pointer = -1
        self.valid_page_count = 0
        self.invalid_page_count = 0
        self.erase_count = 0
        self.is_free = True


    def allocate_page(self):
        self.write_pointer += 1
        self.valid_page_count += 1

        return self.write_pointer


    def write_page(self):
        blk_write_pointer = self.allocate_page()

        self.pages[blk_write_pointer].write()

        return blk_write_pointer, self.pages[blk_write_pointer].page_id


    def invalidate_page(self, page_id):
        self.invalid_page_count += 1

        self.pages[page_id % self.pages_per_block].delete()


    def delete_block(self):
        self.erase_count += 1
        self.write_pointer = -1

        for ppn in self.pages:
            if ppn.is_valid:
                yield ppn.page_id

            ppn.delete()
        
