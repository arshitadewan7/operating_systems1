from mmu import MMU
from collections import OrderedDict

class LruMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for LruMMU
        # ------------------------------------------------------------------
        self.capacity = frames
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        self.debug = False

        # OrderedDict keeps pages in access order:
        # left = least recently used, right = most recently used
        self.order = OrderedDict()
        # ------------------------------------------------------------------

    def set_debug(self):
        # TODO: Implement the method to set debug mode
        # ------------------------------------------------------------------
        self.debug = True
        # ------------------------------------------------------------------

    def reset_debug(self):
        # TODO: Implement the method to reset debug mode
        # ------------------------------------------------------------------
        self.debug = False
        # ------------------------------------------------------------------

    def read_memory(self, page_number):
        # TODO: Implement the method to read memory
        # ------------------------------------------------------------------
        if page_number in self.order:
            # hit: move to most recently used
            self.order.move_to_end(page_number, last=True)
            if self.debug:
                print(f"hit R {page_number}")
            return

        # miss: evict if full
        if len(self.order) >= self.capacity:
            self._evict()
        self._insert_fault(page_number, dirty=False)
        # ------------------------------------------------------------------

    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        # ------------------------------------------------------------------
        if page_number in self.order:
            # hit: mark dirty and move to most recently used
            self.order[page_number]["dirty"] = True
            self.order.move_to_end(page_number, last=True)
            if self.debug:
                print(f"hit W {page_number}")
            return

        # miss: evict if full
        if len(self.order) >= self.capacity:
            self._evict()
        self._insert_fault(page_number, dirty=True)
        # ------------------------------------------------------------------

    def get_total_disk_reads(self):
        # TODO: Implement the method to get total disk reads
        # ------------------------------------------------------------------
        return self.disk_reads
        # ------------------------------------------------------------------

    def get_total_disk_writes(self):
        # TODO: Implement the method to get total disk writes
        # ------------------------------------------------------------------
        return self.disk_writes
        # ------------------------------------------------------------------

    def get_total_page_faults(self):
        # TODO: Implement the method to get total page faults
        # ------------------------------------------------------------------
        return self.page_faults
        # ------------------------------------------------------------------

    # ===================== Internal helpers =====================

    def _evict(self):
        """Evict the least recently used page (leftmost in OrderedDict)."""
        victim, info = self.order.popitem(last=False)  # remove LRU
        if info["dirty"]:
            self.disk_writes += 1
        if self.debug:
            print(f"evict {victim} {'DIRTY' if info['dirty'] else 'CLEAN'} (lru)")

    def _insert_fault(self, page, dirty):
        """Insert a new page on fault and mark it MRU."""
        self.order[page] = {"dirty": dirty}
        self.disk_reads += 1
        self.page_faults += 1
        if self.debug:
            print(f"fault load {page} {'W' if dirty else 'R'}")
