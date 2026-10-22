# Claude safety review - Windows POC coordinator process termination

**Project:** `hydra3333/analysing_perceived_randomness_in_reality`
**Reviewed:** `Predictive_Randomness_Windows_POC_P1_P2_Coordinator_Source_v0_1.zip`, `src/Powerball_Experiment_Coordinator.py` (556 lines), mainly `terminate_tree()` (lines 144-203) and the `KeyboardInterrupt` path (lines 472-478)
**Library behaviour checked against:** psutil 7.2.2 source (the version installed on the project PC)
**Version:** v2, 22 October 2026 (v2 corrects the process-name allow-list to include the batch wrapper's own legitimate child processes; see section 2A)
**Status:** independent review; no code changed.
**Also checked:** the `Run_Coordinator.bat` in the review package, and CPython 3.14's `Lib/venv/scripts/nt/activate.bat`.

---

## 0. Summary

- **ChatGPT's concern is correct.** The status-file PID can become a kill target without being shown to belong to the launched tree (lines 167-174). PID reuse is guarded by the creation-time check; a wrong or forged status file is not.
- **There are four further weaknesses** (section 1). The most important: the process tree is captured only at kill time. If the wrapper has already exited, nothing is captured, and the code then relies on the status file.
- **Everything can be fixed with `psutil` and the standard library.** No Job Objects or other new Windows API code are needed.
- **The key design change is "capture early, keep, verify".** Record the tree's members while the wrapper is alive, keep their `psutil.Process` objects, and later kill only those.
- **The status file becomes verification-only.** It is never a source of kill targets.
- **Useful framing for the owner:** a Job Object would solve the *missed-orphan* problem (a descendant escaping cleanup). It does not solve the *wrong-process kill* problem, which is the owner's concern. That one is solved by identity and ancestry discipline, which this design provides.

---

## 1. Assessment of the actual code

| # | Lines | Finding | Severity |
|---|---|---|---|
| D1 | 167-174 | **The status-file PID becomes a kill target without tree membership.** It is gated only on PID + creation time matching (`same_process`). That prevents killing a *reused* PID. It does not prevent killing a live *unrelated* process if the status file names one (a bug, a stale file, or a forged entry). ChatGPT's concern is accurate. | **High** (wrong-kill path) |
| D2 | 156-165 | **The tree is snapshotted only at kill time.** If the wrapper (`cmd.exe`) has already exited, nothing is enumerated. The descendants are then unreachable, because `children()` starts from the root. The fallback is D1's unsafe path. | High (makes D1 reachable) |
| D3 | 157 | **The root process is not checked against its launch identity.** No creation time is recorded at `Popen` time. In practice the root PID cannot be reused while `Popen` holds its process handle, but that is not a documented guarantee. Also, killing the root through psutil *by PID* is unnecessary, because `Popen.kill()` acts on the handle `Popen` owns. | Low |
| D4 | 159 (psutil) | **psutil's recursive `children()` compares every descendant's creation time only with the *root's*** (psutil 7.2.2, `__init__.py` lines 995-1029), not with its immediate parent's. A tiny window remains: an unrelated process created after the root started, whose own parent died and whose dead parent's PID was then reused by one of our tree members, would be listed as our descendant. The fix is cheap: also check each edge (section 3). | Very low, cheap to close |
| D5 | 198-203 | **A stop is reported as confirmed even when the experiment was never identified.** If the status file is missing and the tree was empty, the function returns `True, "Terminated..."`, yet an orphaned experiment may still be running. It should be `UNVERIFIED`, not success. | Medium (false assurance) |
| D6 | 472-478, 551-556 | **Ctrl+C is handled as an exception that can arrive anywhere.** (a) A second Ctrl+C during cleanup aborts `stop()` part-way, escapes the outer handler (which catches only `OSError`, `ValueError`, `RuntimeError`, `SubprocessError`), and no manifest is written. (b) A Ctrl+C arriving between `Popen` (line 444) and `active[n] = w` (line 454) leaves a launched child unregistered and never cleaned up. | Medium |
| D7 | 127 | **The creation-time tolerance of 0.5 s is loose.** Both values come from psutil, which reads the same Windows creation time, so they should match almost exactly. A tolerance of about 1 ms is ample. | Low |

**Confirmed correct:** in psutil 7.2.2 on Windows, `terminate()` and `kill()` call `_raise_if_pid_reused()`. That runs `is_running()`, which compares PID + creation time captured when the `Process` object was created (lines 458-468, 624-649, 1320-1339). **A stored `psutil.Process` object therefore refuses to kill a process whose PID has since been reused.** `wait_procs` and the survivor check are sound. Swallowing `AccessDenied` is acceptable, because the survivor check catches it afterwards.

---

## 2. Minimal safety invariants

1. **The ownership proof is ancestry captured while the root is alive.** A process may be killed only if it was observed as a descendant of the launched wrapper while that wrapper was alive and verified. Each parent-child link must also pass the creation-time order check (child created no earlier than its parent).
2. **Identity is PID + creation time, carried by a stored `psutil.Process` object.** Kill only through that stored object, so psutil's reuse check applies. Never construct a new object from a PID read from a file and kill it.
3. **The root is killed by handle.** Use `Popen.kill()` for the wrapper, never psutil by PID.
4. **The status file is evidence, not authority.** Its PID + creation time are used only to (a) check that the experiment is a captured member, and (b) confirm afterwards that it has exited.
5. **Executable names are a sanity filter.** The root must be `cmd.exe`. Descendants must be named `cmd.exe`, `chcp.com` or `python.exe` (section 2A explains why the wrapper legitimately produces all three). Any other descendant is an anomaly: report it and do not kill it. With experiments forbidden from starting child processes, it is a rule violation anyway.
6. **When ownership is uncertain, leave the process running and report it.** Never kill by name, never use `taskkill /IM`, and never kill a process that has not been captured.
7. **Success requires positive identification.** A stopped run is `STOPPED_CONFIRMED` only if the experiment process was identified (a captured member matching the status file's PID + creation time) and is now gone, and no captured member survives. Otherwise it is `UNVERIFIED` or `ORPHAN_SUSPECTED`.

### 2A. Legitimate processes started by the batch wrappers themselves (v2 correction)

v1 allowed only `python.exe` below the root. That is too narrow, because the `.bat` runners start short-lived processes of their own:

- **The wrapper's own `sys.prefix` pre-check.** The current `Run_Coordinator.bat` runs `"%PY%" -c "...sys.prefix check..."` before launching its program, and `Run_Experiment.bat` presumably does the same. Under a venv that is a short-lived redirector `python.exe` plus interpreter `python.exe`, which exit before the real experiment starts.
- **Venv activation, when it happens.** CPython 3.14's `activate.bat` saves and sets the console code page with `for /f ... in ('"%SystemRoot%\System32\chcp.com"')`, which runs a child `cmd.exe` that runs `chcp.com`, and then runs `chcp.com` directly twice. Under the coordinator this path is normally skipped, because the children inherit the coordinator's already-activated `VIRTUAL_ENV` and take the "already active" branch. It does occur if the coordinator is ever started without activation.
- **`CALL activate.bat` and the built-in commands** (`set`, `if`, `pushd`, `for` over file names) run inside the same `cmd.exe` and start no process.

Consequences for the design:

- **Allow-list:** root `cmd.exe`; descendants `cmd.exe`, `chcp.com`, `python.exe`. Anything else is an anomaly.
- **Ancestry, not names, proves ownership.** Names only catch the unexpected. A verified-ancestry descendant named `cmd.exe` or `chcp.com` is ours and may be killed.
- **Experiment identification must not confuse the pre-check interpreter with the experiment.** Matching the status file's PID + creation time to a captured member (section 3) already handles this. The pre-check `python.exe` is captured, exits, and simply becomes a gone member.
- **Transient members are normal.** Members that have already exited by stop time raise `NoSuchProcess` and count as gone.
- **Console code page (minor side effect).** If several children ever do run `activate.bat` concurrently, they share the coordinator's console and change its code page with `chcp`. Overlapping save/restore could leave the console in code page 65001. This is cosmetic, avoided when `VIRTUAL_ENV` is inherited, and worth one observation in the tests.

---

## 3. Proposed algorithm (pseudocode)

```text
LAUNCH(worker):
    t0 = time()
    proc = Popen([...wrapper...])            # unchanged Option F launch
    REGISTER worker immediately (no await/IO between Popen and registration)
    try: root = psutil.Process(proc.pid); root_ct = root.create_time()
    except: worker.unsupervisable = True      # can still kill root by handle
    require  t0 - 1s <= root_ct <= time() + 1s  and  root.name() == "cmd.exe"
             else worker.unsupervisable = True (report)
    worker.members = {}                       # pid -> stored psutil.Process

CAPTURE(worker):                              # every poll (~1 s) while proc.poll() is None
    if worker.unsupervisable: return
    try: snap = root.children(recursive=True) # psutil: root-ctime filter
    except (NoSuchProcess, AccessDenied): return
    known = {root.pid: root} | worker.members
    for c in snap (parents before children, i.e. repeat until no change):
        if c.pid in worker.members: continue
        parent = known.get(c.ppid())
        if parent is None: continue                       # parent not yet verified
        if c.create_time() < parent.create_time(): ANOMALY("stale ppid"); continue
        if c.name().lower() not in {"cmd.exe", "chcp.com", "python.exe"}:
            ANOMALY("unexpected descendant"); continue                 # see section 2A
        worker.members[c.pid] = c; known[c.pid] = c       # keep object for life of run
    status = read_status()
    if status and status.run_id == worker.run_id and not worker.experiment:
        match = member with pid == status.pid and |ct - status.ct| < 1 ms
        if match: worker.experiment = match
        elif STARTED older than grace (e.g. 10 s): ANOMALY("self-reported PID not in tree")
                                                    # report only; never kill it

STOP(worker, reason):                         # SIGINT ignored during this (see section 7)
    CAPTURE(worker)                           # final capture if root still alive
    for m in worker.members (deepest first):
        try: m.kill()                         # psutil refuses reused PIDs
        except NoSuchProcess: pass
        except AccessDenied: note(m)
    if proc.poll() is None: proc.kill()       # handle-based, cannot hit reused PID
    gone, alive = psutil.wait_procs(list(worker.members.values()), timeout=T)
    try: proc.wait(timeout=T) except TimeoutExpired: alive.append(root_marker)
    if alive:                         -> ORPHAN_SUSPECTED (pid, ct, name, exe, cmdline)
    elif worker.experiment is None:   -> UNVERIFIED (experiment never identified)
    else:                             -> STOPPED_CONFIRMED
    NEVER: kill anything not in worker.members; kill by status PID; kill by name.
```

Notes:

- The first-release rule (experiments start no child processes) means the tree stops growing within a second or two of launch: the wrapper; any transient activation and pre-check processes (section 2A); then the experiment's redirector and interpreter. Transient processes may or may not be captured, depending on timing, and either way is harmless. One capture per poll is ample.
- Members captured early stay killable after their parent exits, because the stored objects carry their identity (question 4).

---

## 4. Answers to the ten questions

1. **Accurate?** Yes, see D1. Also D2 (capture only at kill time), D5 (false "confirmed"), D6 (Ctrl+C), and the small D3/D4/D7 items.
2. **Feasible with psutil alone?** Yes. Everything above is psutil plus standard library: `signal`, `subprocess`, `time`. No Windows API code.
3. **Residual risks:**

   | Risk | Status after the fix |
   |---|---|
   | PID reuse | Defeated by PID + creation-time identity in stored objects (psutil-enforced) and handle-based root kill |
   | Stale parent PIDs | Closed by the per-edge creation-time check |
   | Forged or stale status | Harmless: never a kill source; run-ID checked; mismatch is an anomaly |
   | Ancestry races (a descendant created after the last capture and before the kill) | Can be missed; it is then left running and reported, which is the safe direction. With no experiment-created children, nothing appears after start-up. |
   | Re-parenting | Windows does not re-parent; children of a dead parent keep a stale parent PID, handled above |

   **Not guaranteed without OS isolation:** that *every* descendant is caught. Missed ones are left running and reported, never mis-killed.
4. **Only processes captured while the root is alive?** Yes, as the ownership proof. Children captured earlier remain legitimate targets after their parent exits, through their stored objects.
5. **Store `psutil.Process` objects with creation times?** Yes. This is the central improvement: psutil's kill path then rejects reused PIDs automatically.
6. **Executable checks?** Enforce **names** as a refusal filter: `cmd.exe` for the root; `cmd.exe`, `chcp.com` or `python.exe` for descendants (section 2A). Treat **full paths** as information only:
   - the redirector runs from `.venv\Scripts`, the real interpreter from the base installation, and future Python releases may change that arrangement;
   - enforcing paths would cause false refusals. Those are safe (the process is left running and reported) but would be noise.
7. **Ctrl+C:** see section 7. In short: a flag-setting `SIGINT` handler, no asynchronous exceptions, further Ctrl+C ignored during cleanup, a manifest always written, exit code 130.
8. **A non-destructive test with unrelated Python processes:** yes, section 5 (N1-N5).
9. **If something cannot be safely terminated:**
   - Stop launching new workers, but keep supervising the other running workers normally; their own verified clean-up remains safe.
   - At the end, report `FAIL` with a list of suspected orphans (PID, creation time, name, path, command line) and print a suggested manual command for the operator to run *after checking*.
   - Optionally (cheap and recommended), write an unresolved-orphan marker. The next coordinator start refuses to run until the operator acknowledges it (for example with `--acknowledge-orphans <group>`).
10. **Simpler or more robust design?** "Capture early, keep, verify" *is* the simplification. It removes the status-file fallback entirely and makes the ownership rule a single sentence. A cooperative stop-request file does not help with hangs. Using `taskkill /T` instead gives less control over identity checks, so psutil remains the right tool.

---

## 5. Test plan (Windows)

**Decoys present throughout every test.** Before each session, start from separate CMD windows (not from the coordinator) and record each decoy's PID + creation time:

- (a) global Python: `py -c "import time; time.sleep(3600)"`;
- (b) the project `.venv` Python with the same command;
- (c) a second project's or another venv's Python, if one exists;
- (d) a separate `cmd.exe` running a long `timeout /t 3600` batch file.

After **every** test, all decoys must still be alive with the same PID + creation time.

### Non-destructive (run first; the coordinator kills nothing)

| ID | Test | Pass |
|---|---|---|
| N1 | New `--plan-termination` diagnostic: launch six sleeping probes; capture runs; print each worker's members and the planned kill list, with name, PID, creation time and parent; kill nothing; then let the probes finish normally | No decoy appears in any plan; each plan contains only the root `cmd.exe` and descendants from {`cmd.exe`, `chcp.com`, `python.exe`}, with the wrapper's pre-check interpreter and any activation processes appearing as transient members; the experiment is matched to a member; record the observed tree shape as evidence |
| N2 | Forged status: a test-only probe case writes decoy (b)'s PID + creation time into its status file | Anomaly "self-reported PID not in tree" reported; decoy absent from the plan |
| N3 | Status file with the wrong `run_id` or missing | Ignored for matching; reported as `UNVERIFIED` if never matched |
| N4 | Edge check: unit test with a fake process table (stale parent PID, child older than parent) | Rejected as anomalies; nothing added to members |
| N5 | Name filter: unit test with an unexpected descendant name, and with `cmd.exe` / `chcp.com` descendants | Unexpected name: anomaly, not added. `cmd.exe` / `chcp.com` with verified ancestry: added as members, no anomaly |
| N6 | Coordinator started without an activated venv (children then run `activate.bat`), six workers | Plans include the transient `cmd.exe` / `chcp.com`; no false anomalies; console code page checked with `chcp` before and after |

### Destructive (only after N1-N5 pass; one at a time; decoys checked after each)

| ID | Test | Pass |
|---|---|---|
| D-1 | One sleep-timeout worker | `STOPPED_CONFIRMED`; members gone; no result file |
| D-2 | Six sleep-timeout workers | All six `STOPPED_CONFIRMED` |
| D-3 | W-09 / W-16 diagnostic: wrapper killed alone by handle, then supervised clean-up of the remaining members | Survivors observed, then removed through the stored objects; `STOPPED_CONFIRMED` |
| D-4 | Ctrl+C with six workers; press Ctrl+C a second time during clean-up | Clean-up completes; manifest written; exit 130; all `INTERRUPTED` and confirmed |
| D-5 | Memory guard triggered with deliberately high floors and small allocations | Guarded workers stopped and confirmed |
| D-6 | Hard exit (`os._exit(7)`) under the coordinator (the coordinator half of W-11) | Status `STARTED` only; run `FAILED`; no clean-up needed; members gone |

---

## 6. Is stronger isolation needed for production acceptance?

**No**, provided all of these hold:

- the D1-D7 fixes and the section 2 invariants are implemented;
- N1-N5 and D-1 to D-6 pass with the decoys untouched;
- experiments continue not to start child processes.

Precisely:

- **Wrong-process kills (the owner's concern)** are prevented by identity and ancestry discipline. The remaining theoretical route would need Windows itself to report a wrong parent for a newly created process.
- **Missed descendants** cannot be ruled out absolutely without OS-level isolation such as a Job Object. With no experiment-created children they are improbable, and they fail in the safe direction: left running, reported, flagged on the next start.

**Reconsider a Job Object only if** a future approved method must start its own child processes, which is when missed descendants become realistic.

---

## 7. Ctrl+C handling (replaces the asynchronous `KeyboardInterrupt` path)

```text
interrupt_requested = False
def on_sigint(signum, frame): interrupt_requested = True   # standard library signal
signal.signal(signal.SIGINT, on_sigint)                     # set at start-up

main loop: if interrupt_requested -> stop launching; STOP(all active, "INTERRUPTED")
during STOP of all: signal.signal(signal.SIGINT, signal.SIG_IGN)  # print "cleanup in progress"
always: write manifest; exit code 130 when interrupted
```

- Experiments share the console, so they receive Ctrl+C themselves and normally exit first. The coordinator's job is then confirmation and clean-up of anything left.
- Registering each worker immediately after `Popen` returns is safe once no exception can arrive asynchronously.

---

## Sources

- CPython 3.14 `activate.bat` (chcp.com use): https://github.com/python/cpython/blob/3.14/Lib/venv/scripts/nt/activate.bat
- psutil 7.2.2 source, `psutil/__init__.py` (`children`, `_raise_if_pid_reused`, `is_running`, `terminate`, `kill`), downloaded from PyPI.
- Python `subprocess` docs (`Popen.kill` / `terminate` act on the child process via its handle): https://docs.python.org/3.14/library/subprocess.html
- Python `signal` docs (SIGINT handling on Windows): https://docs.python.org/3.14/library/signal.html
- Microsoft, Terminating a Process: https://learn.microsoft.com/en-us/windows/win32/procthread/terminating-a-process
