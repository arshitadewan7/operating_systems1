# randmmu.py
from mmu import MMU
import random

class RandMMU(MMU):
    def __init__(self, frames, seed=0):
        # TODO: Constructor logic for RandMMU
        # ------------------------------------------------------------------
        # Keep simulator counters and configuration
        self.capacity = frames
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        self.debug = False

        # Residency structures
        # page -> {"dirty": bool}
        self.table = {}
        # list of resident pages to pick random victim from
        self.pages = []

        # Deterministic RNG for reproducible runs
        self.rng = random.Random(seed)
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
        # Hit: page already resident
        if page_number in self.table:
            if self.debug:
                print(f"hit R {page_number}")
            return

        # Miss: evict if full, then load clean page
        if len(self.table) >= self.capacity:
            self._evict_random_victim()
        self._insert_fault(page_number, dirty=False)
        # ------------------------------------------------------------------

    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        # ------------------------------------------------------------------
        # Hit: mark dirty
        if page_number in self.table:
            self.table[page_number]["dirty"] = True
            if self.debug:
                print(f"hit W {page_number}")
            return

        # Miss: evict if full, then load dirty page
        if len(self.table) >= self.capacity:
            self._evict_random_victim()
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

    # ===================== Internal helpers (not in template) =====================

    def _evict_random_victim(self):
        """Pick a random resident page and evict it. Count a disk write if dirty."""
        victim = self.rng.choice(self.pages)
        info = self.table.pop(victim)
        self.pages.remove(victim)

        if info["dirty"]:
            self.disk_writes += 1

        if self.debug:
            print(f"evict {victim} {'DIRTY' if info['dirty'] else 'CLEAN'} (rand)")

    def _insert_fault(self, page, dirty):
        """Load a page due to a fault (increments disk_reads and page_faults)."""
        self.table[page] = {"dirty": dirty}
        self.pages.append(page)
        self.disk_reads += 1
        self.page_faults += 1

        if self.debug:
            print(f"fault load {page} {'W' if dirty else 'R'}")
