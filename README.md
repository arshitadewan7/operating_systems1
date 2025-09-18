## Clock Policy & Sweep Runner

To run the Clock (second-chance) policy:

```bash
python memsim.py trace1 4 clock debug
python memsim.py trace1 4 clock quiet
python memsim.py trace2 6 clock quiet
```

Compare against other policies:

```bash
python memsim.py trace1 4 lru quiet
python memsim.py trace1 4 rand quiet
python memsim.py trace1 4 clock quiet
```

Decompress the big traces once:

```bash
python - << 'PY'
import gzip, shutil
for n in ["bzip.trace.gz","gcc.trace.gz","sixpack.trace.gz","swim.trace.gz"]:
    with gzip.open(n,"rb") as f_in, open(n[:-3],"wb") as f_out:
        shutil.copyfileobj(f_in,f_out)
PY
```

Run the full experiment sweep (generates `results.csv`):

```bash
python sweep.py
```
