import subprocess, csv, itertools, os

traces = ["bzip.trace", "gcc.trace", "sixpack.trace", "swim.trace"]
policies = ["lru", "clock", "rand"]
frames_list = [8, 16, 32, 64, 128, 256, 512, 1024]

def run_one(trace, frames, policy):
    out = subprocess.check_output(
        ["python", "memsim.py", trace, str(frames), policy, "quiet"],
        text=True
    )
    reads = writes = rate = None
    for line in out.splitlines():
        ls = line.strip().lower()
        if ls.startswith("total disk reads:"):
            reads = int(ls.split(":")[1])
        elif ls.startswith("total disk writes:"):
            writes = int(ls.split(":")[1])
        elif ls.startswith("page fault rate:"):
            rate = float(ls.split()[-1])
    if None in (reads, writes, rate):
        raise RuntimeError(f"Could not parse output:\n{out}")
    return reads, writes, rate

def main():
    frames = frames_list
    pols = policies
    if os.environ.get("FRAMES"):
        frames = [int(x) for x in os.environ["FRAMES"].split(",")]
    if os.environ.get("POLICIES"):
        pols = os.environ["POLICIES"].split(",")

    with open("results.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["trace","frames","policy","disk_reads","disk_writes","fault_rate"])
        for trace, frames_val, policy in itertools.product(traces, frames, pols):
            dr, dw, fr = run_one(trace, frames_val, policy)
            w.writerow([trace, frames_val, policy, dr, dw, fr])
            print(f"{trace} {frames_val:>4} {policy:>5}  fault_rate={fr:.4f}")

if __name__ == "__main__":
    main()
