"""WF-1B supplement probe (Claude, 31 Oct 2026): peak resident memory of one process running the WF-1 timing probe
(exchange/EX_077_Claude/probe_wf_timing.py: all 40 variants, invented master, simulated release). Linux only
(resource.getrusage). Reads no repository data file and no real draw.
Usage: python3 -I probe_wf_memory.py REPO GAME STEP"""
import resource, runpy, sys, time
repo = sys.argv[1]
t = time.time()
sys.argv = ['probe_wf_timing.py'] + sys.argv[1:]
try:
    runpy.run_path(repo + '/exchange/EX_077_Claude/probe_wf_timing.py', run_name='__main__')
finally:
    print('PEAK_RSS_MB', round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, 1), 'seconds', round(time.time() - t, 1))
