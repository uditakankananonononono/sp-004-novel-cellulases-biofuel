#!/usr/bin/env python3
"""Golden-output and corruption tests for the DOC-1-034 R1 package.

Byte-for-byte comparison under the canonicalization in cli/CLI_README.md.
Run from anywhere: python3 tests/run_tests.py   (exit 0 = all pass)
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CLI = os.path.join(ROOT, "cli", "sp004_audit.py")
GOLDEN = os.path.join(HERE, "golden")

CASES = [
    ("verify", ["verify"], 0),
    ("funnel", ["funnel"], 0),
    ("gates", ["gates"], 0),
    ("composition", ["composition"], 0),
    ("novelty", ["novelty"], 0),
    ("structure", ["structure"], 0),
    ("decoys", ["decoys"], 0),
    ("scrambles", ["scrambles"], 0),
    ("uniprot", ["uniprot"], 0),
    ("xcat", ["xcat"], 0),
    ("candidate_MGYP007817750544", ["candidate", "MGYP007817750544"], 0),
    ("candidates_top20", ["candidates", "--limit", "20"], 0),
    ("candidates_GH7", ["candidates", "--family", "GH7"], 0),
]


def run(root, argv):
    return subprocess.run([sys.executable, CLI, "--root", root] + argv,
                          capture_output=True)


def main():
    failures = []
    for name, argv, want_rc in CASES:
        golden_path = os.path.join(GOLDEN, name + ".txt")
        with open(golden_path, "rb") as fh:
            want = fh.read()
        proc = run(ROOT, argv)
        got = proc.stdout
        ok = got == want and proc.returncode == want_rc
        print("[%s] golden %-32s (%d bytes)" % ("PASS" if ok else "FAIL", name, len(want)))
        if not ok:
            failures.append(name)

    # determinism: same command twice, identical bytes
    a = run(ROOT, ["verify"]).stdout
    b = run(ROOT, ["verify"]).stdout
    ok = a == b
    print("[%s] determinism verify x2 identical" % ("PASS" if ok else "FAIL"))
    if not ok:
        failures.append("determinism")

    # corruption test: flip one byte in a temp COPY; verify must FAIL (rc 1)
    tmp = tempfile.mkdtemp(prefix="sp004-corrupt-")
    try:
        for item in ("results", "protocol", "MANIFEST.sha256"):
            src = os.path.join(ROOT, item)
            dst = os.path.join(tmp, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        victim = os.path.join(tmp, "results", "funnel_ref.json")
        data = open(victim, "rb").read()
        i = data.index(b"12451")
        open(victim, "wb").write(data[:i] + b"12452" + data[i + 5:])
        proc = run(tmp, ["verify"])
        ok = proc.returncode == 1 and b"AUDIT RESULT: FAIL" in proc.stdout
        print("[%s] corruption detected (verify exit %d on tampered copy)"
              % ("PASS" if ok else "FAIL", proc.returncode))
        if not ok:
            failures.append("corruption")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # extra-file negative test: unlisted bytes must FAIL verify
    tmp = tempfile.mkdtemp(prefix="sp004-extra-")
    try:
        for item in ("results", "protocol", "MANIFEST.sha256"):
            src = os.path.join(ROOT, item)
            dst = os.path.join(tmp, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        open(os.path.join(tmp, "EXTRA.bin"), "wb").write(b"unlisted bytes")
        proc = run(tmp, ["verify"])
        ok = (proc.returncode == 1 and b"AUDIT RESULT: FAIL" in proc.stdout
              and b"[FAIL] inventory-exhaustive" in proc.stdout)
        print("[%s] extra-file rejected (verify exit %d on unlisted EXTRA.bin)"
              % ("PASS" if ok else "FAIL", proc.returncode))
        if not ok:
            failures.append("extra-file")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # manifest self-check
    proc = subprocess.run(["sha256sum", "-c", "MANIFEST.sha256"],
                          cwd=ROOT, capture_output=True)
    bad = [ln for ln in proc.stdout.decode().splitlines() if not ln.endswith(": OK")]
    ok = proc.returncode == 0 and not bad
    print("[%s] manifest sha256sum -c clean" % ("PASS" if ok else "FAIL"))
    if not ok:
        failures.append("manifest")

    print("")
    if failures:
        print("TESTS FAILED: %s" % ", ".join(failures))
        return 1
    print("ALL TESTS PASS (%d golden + determinism + corruption + extra-file + manifest)" % len(CASES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
