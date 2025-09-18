from mmu import MMU


class ClockMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for EscMMU

        # capacity / number of frames
        self.capacity = int(frames)
        # ring buffer: each slot holds a page number (int) or None
        self.frames = [None] * self.capacity
        # per-page metadata: page -> {"idx": int, "dirty": bool, "ref": int}
        self.meta = {}
        # clock hand (index into self.frames)
        self.hand = 0
        # use free frames before evicting
        self.free_indices = list(range(self.capacity))

        # counters
        self._disk_reads = 0
        self._disk_writes = 0
        self._page_faults = 0

        self._debug = False

        # pass

    def set_debug(self):
        # TODO: Implement the method to set debug mode
        self._debug = True
        # pass

    def reset_debug(self):
        # TODO: Implement the method to reset debug mode
        self._debug = False

        # pass

    def _dbg(self, msg: str):
        if self._debug:
            print(msg)


    def read_memory(self, page_number):
        # TODO: Implement the method to read memory
        self._access(page_number, is_write=False)
        # pass

    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        self._access(page_number, is_write=False)
        # pass

    def get_total_disk_reads(self):
        # TODO: Implement the method to get total disk reads
        return self._disk_reads
    
    def get_total_disk_writes(self):
        # TODO: Implement the method to get total disk writes
        return self._disk_writes

    def get_total_page_faults(self):
        # TODO: Implement the method to get total page faults
        return self._page_faults
    
    # core logic
    def _access(self, page: int, is_write: bool):
        info = self.meta.get(page)
        if info is not None:
            # hit: give second chance
            info["ref"] = 1
            if is_write:
                info["dirty"] = True
                self._dbg(f"hit W {page} frame {info['idx']}")
            else:
                self._dbg(f"hit R {page} frame {info['idx']}")
            return

        # miss → fault + read
        self._page_faults += 1
        self._disk_reads += 1

        idx = self._place(page, dirty=is_write)
        self._dbg(f"fault load {page} {'W' if is_write else 'R'} into frame {idx}")

    def _place(self, page: int, dirty: bool) -> int:
        if self.free_indices:
            idx = self.free_indices.pop(0)
        else:
            idx = self._evict()

        self.frames[idx] = page
        self.meta[page] = {"idx": idx, "dirty": bool(dirty), "ref": 1}
        return idx

    def _evict(self) -> int:
        # second-chance loop: clear ref==1; evict first with ref==0
        while True:
            current_page = self.frames[self.hand]
            if current_page is None:
                # should not happen once the ring is full, but be safe
                freed = self.hand
                self.hand = (self.hand + 1) % self.capacity
                return freed

            info = self.meta[current_page]
            if info["ref"] == 1:
                info["ref"] = 0
                self.hand = (self.hand + 1) % self.capacity
                continue

            # evict victim at self.hand
            if info["dirty"]:
                self._disk_writes += 1
                self._dbg(f"evict {current_page} DIRTY (clock)")
            else:
                self._dbg(f"evict {current_page} CLEAN (clock)")

            del self.meta[current_page]
            self.frames[self.hand] = None
            freed = self.hand
            # advance so we don’t immediately re-check the same slot
            self.hand = (self.hand + 1) % self.capacity
            return freed