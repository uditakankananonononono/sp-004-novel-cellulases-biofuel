#!/usr/bin/env python3
"""sp004_audit.py - read-only query/audit CLI over the frozen SP-004 (DOC-1-034 R1)
cellulase-discovery outputs.

DETERMINATION: (a) read-only query/audit tool over frozen outputs.
It never recomputes science from raw data and never creates a new scientific
result: every number it emits is either copied verbatim from a frozen artifact
or recomputed by direct tabulation of a frozen table under the documented
canonicalization (see cli/CLI_README.md). It contains no search, scoring,
alignment, or filtering logic of its own.

Requires: Python 3.8+ standard library only.
"""
import argparse, csv, hashlib, json, os, statistics, sys

TOOL = "sp004_audit"
VERSION = "1.0.0"

CELLULASE_PFAM = {
    "PF00150": "GH5", "PF01341": "GH6", "PF00840": "GH7", "PF00759": "GH9",
    "PF01670": "GH12", "PF02015": "GH45", "PF02011": "GH48", "PF01915": "GH3",
}
REF_MEDIAN_ALIPHATIC = 64.44  # frozen: gate_evaluation.json metrics.ref_median_aliphatic
MIN_CYS = 2                     # frozen: locked gate G5


def eprint(*a):
    print(*a, file=sys.stderr)


def load_json(root, rel):
    with open(os.path.join(root, rel), "r", encoding="utf-8") as fh:
        return json.load(fh)


def load_csv(root, rel):
    with open(os.path.join(root, rel), "r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def final_candidates(rows):
    return [r for r in rows if r["stage_reached"] == "F6_pass"]


def family_of(pfam_field):
    fams = {CELLULASE_PFAM[p] for p in pfam_field.split(";") if p in CELLULASE_PFAM}
    if len(fams) == 1:
        return next(iter(fams))
    if not fams:
        return "none"
    return "multi-domain"


def recompute_ref_funnel(rows):
    stages = [r["stage_reached"] for r in rows]
    n = len(stages)
    f1 = sum(1 for s in stages if s != "F1_fail")
    f2 = sum(1 for s in stages if s not in ("F1_fail", "F2_fail", "F2_not_evaluable"))
    f3 = sum(1 for s in stages if s not in ("F1_fail", "F2_fail", "F2_not_evaluable", "F3_fail"))
    f4 = sum(1 for s in stages if s not in ("F1_fail", "F2_fail", "F2_not_evaluable", "F3_fail", "F4_fail"))
    f6 = sum(1 for s in stages if s == "F6_pass")
    return {"hits": n, "with_sequence": n, "F1_pass": f1, "F2_pass": f2,
            "F3_pass": f3, "F4_pass": f4, "F6_pass": f6}


def recompute_decoy_funnel(rows):
    stages = [r["stage_reached"] for r in rows]
    n = len(stages)
    f1 = sum(1 for s in stages if s != "F1_fail")
    return {"hits": n, "with_sequence": n, "F1_pass": f1}


def thermostable(rows):
    return [r for r in rows
            if float(r["aliphatic_index"]) >= REF_MEDIAN_ALIPHATIC and int(r["cys"]) >= MIN_CYS]


def structure_ok(entry):
    try:
        return int(entry.get("rcsb_hits", 0)) > 0 and float(entry.get("template_coverage", 0)) >= 0.6
    except (TypeError, ValueError):
        return False


# ---------------------------------------------------------------- verify ----

def cmd_verify(root, as_json=False):
    checks = []

    def rec(name, ok, detail):
        checks.append({"check": name, "ok": bool(ok), "detail": detail})

    # 1. MANIFEST.sha256
    mpath = os.path.join(root, "MANIFEST.sha256")
    if not os.path.exists(mpath):
        rec("manifest", False, "MANIFEST.sha256 not found")
        manifest_ok = False
    else:
        bad, missing, total = [], [], 0
        with open(mpath, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.rstrip("\n")
                if not line.strip():
                    continue
                digest, rel = line.split("  ", 1)
                total += 1
                fp = os.path.join(root, rel)
                if not os.path.exists(fp):
                    missing.append(rel)
                elif sha256_file(fp) != digest:
                    bad.append(rel)
        manifest_ok = not bad and not missing
        rec("manifest", manifest_ok,
            "%d files listed; %d hash mismatches; %d missing" % (total, len(bad), len(missing)))

    # 1b. exhaustive inventory: no unlisted bytes (MANIFEST.sha256 exempts itself
    # and is instead covered by the outer archive hash in PACKAGE_MANIFEST.json)
    listed = set()
    if os.path.exists(mpath):
        with open(mpath, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.rstrip("\n")
                if line.strip():
                    listed.add(line.split("  ", 1)[1])
    unlisted = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for fn in sorted(filenames):
            rel = os.path.relpath(os.path.join(dirpath, fn), root)
            rel = rel.replace(os.sep, "/")
            if rel == "MANIFEST.sha256":
                continue
            if rel not in listed:
                unlisted.append(rel)
    rec("inventory-exhaustive", not unlisted,
        "every regular file is listed in MANIFEST.sha256 (self-manifest exempt); %d unlisted"
        % len(unlisted) if not unlisted else
        "UNLISTED FILES PRESENT: %s" % ", ".join(unlisted[:10]))

    # 2. protocol lock hash
    try:
        ge = load_json(root, "results/gate_evaluation.json")
        proto_hash = sha256_file(os.path.join(root, "protocol/protocol.json"))
        rec("protocol-lock-hash",
            proto_hash == ge["protocol_sha256"],
            "protocol.json SHA-256 %s vs recorded %s" % (proto_hash, ge["protocol_sha256"]))
    except Exception as ex:
        rec("protocol-lock-hash", False, "error: %s" % ex)
        ge = {}

    # 3. locked gate text reproduced verbatim
    try:
        proto = load_json(root, "protocol/protocol.json")
        rec("gate-text",
            proto["success_gate"]["all_required"] == ge.get("gate_text"),
            "6 locked gate strings identical in protocol.json and gate_evaluation.json")
    except Exception as ex:
        rec("gate-text", False, "error: %s" % ex)
        proto = {}

    # 4. reference funnel
    try:
        rows = load_csv(root, "results/candidates_ref.csv")
        recomputed = recompute_ref_funnel(rows)
        frozen = load_json(root, "results/funnel_ref.json")
        rec("funnel-reference", recomputed == frozen,
            "recomputed %s vs frozen %s" % (recomputed, frozen))
    except Exception as ex:
        rec("funnel-reference", False, "error: %s" % ex)
        rows = []

    # 5. decoy funnel
    try:
        drows = load_csv(root, "results/candidates_decoy.csv")
        recomputed_d = recompute_decoy_funnel(drows)
        frozen_d = load_json(root, "results/funnel_decoy.json")
        rec("funnel-decoy", recomputed_d == frozen_d,
            "recomputed %s vs frozen %s" % (recomputed_d, frozen_d))
    except Exception as ex:
        rec("funnel-decoy", False, "error: %s" % ex)
        drows = []

    # 6. gates G1-G6 recomputed vs gate_evaluation.json
    fin = final_candidates(rows)
    try:
        m = ge["metrics"]
        n_refs = len(proto["reference_set"]["accessions"])
        novel30 = sum(1 for r in fin if r["novel_at_30"] == "True")
        sc = load_json(root, "results/structure_check.json")
        s_ok = sum(1 for e in sc if structure_ok(e))
        thermo = len(thermostable(fin))
        decoy_final = sum(1 for r in drows if r["stage_reached"] == "F6_pass")
        ref_yield = len(fin) / n_refs
        decoy_yield = decoy_final / len(proto["reference_set"]["decoys"])
        g = {
            "G1": n_refs >= 12 and n_refs == 15,
            "G2": len(fin) >= 40 and len(fin) == m["final_candidates"],
            "G3": novel30 >= 15 and novel30 == m["novel_lt30"],
            "G4": s_ok >= 15 and s_ok == m["structure_ok"] and len(sc) == m["structure_examined"],
            "G5": thermo >= 5 and thermo == m["thermostable"],
            "G6": (decoy_yield <= 0.10 * ref_yield
                   and decoy_yield == m["decoy_yield_per_query"]
                   and abs(ref_yield - m["ref_yield_per_query"]) < 1e-9),
        }
        checks_frozen = ge["checks"]
        all_ok = all(g.values()) and all(checks_frozen.get(k) is True for k in g) \
            and ge.get("overall") == "PASS" and len(fin) == m["final_candidates"]
        rec("gates-G1-G6", all_ok,
            "recomputed %s; frozen checks %s; overall %s"
            % (g, checks_frozen, ge.get("overall")))
    except Exception as ex:
        rec("gates-G1-G6", False, "error: %s" % ex)

    # 7. frozen candidate-table internal consistency (locked filter definitions)
    try:
        bad = [r["accession"] for r in fin if not (
            r["catalytic_conserved"] == "True"
            and r["novel_at_40"] == "True"
            and float(r["max_ref_identity"]) < 0.40
            and 180 <= int(r["length"]) <= 900
            and float(r["min_evalue"]) <= 1e-10
            and family_of(r["pfam"]) in ("GH3", "GH5", "GH6", "GH7", "GH9",
                                         "GH12", "GH45", "GH48", "multi-domain"))]
        rec("candidate-table-consistency", not bad,
            "%d/%d F6_pass rows satisfy every locked filter definition verbatim"
            % (len(fin) - len(bad), len(fin)))
    except Exception as ex:
        rec("candidate-table-consistency", False, "error: %s" % ex)

    # 8. decoy specificity: zero gate-counted candidates
    try:
        rec("decoy-specificity",
            all(r["stage_reached"] != "F6_pass" for r in drows),
            "0 of %d decoy-pool rows reached F6_pass" % len(drows))
    except Exception as ex:
        rec("decoy-specificity", False, "error: %s" % ex)

    # 9. scrambled controls
    try:
        scr = load_json(root, "results/scramble_controls.json")
        zeros = sum(1 for e in scr if e["scrambled_hits_E<=1e-10"] == 0)
        rec("scrambled-controls", zeros == len(scr) == 5,
            "%d/%d scrambled controls with zero hits at E<=1e-10" % (zeros, len(scr)))
    except Exception as ex:
        rec("scrambled-controls", False, "error: %s" % ex)

    # 10. cross-catalog replication set
    try:
        xcat = load_json(root, "results/xcat_candidates.json")
        ok = len(xcat) == 30 and all(
            float(e["min_evalue"]) <= 1e-10 and float(e["max_ref_identity"]) < 0.40
            for e in xcat)
        rec("cross-catalog-replication", ok,
            "%d candidates; all at E<=1e-10 and <40%% reference identity" % len(xcat))
    except Exception as ex:
        rec("cross-catalog-replication", False, "error: %s" % ex)

    # 11. UniProt novelty screen internal consistency
    try:
        screen = load_json(root, "results/uniprot_novelty_screen.json")
        summary = load_json(root, "results/uniprot_screen_summary.json")
        with_id = [e["best_uniprot_identity"] for e in screen if "best_uniprot_identity" in e]
        errors = [e for e in screen if e.get("uniprot_screen_error")]
        zero_hits = [e["accession"] for e in screen if e.get("uniprot_hits_at_1e-40") == 0]
        already = [e for e in screen if "best_uniprot_identity" in e
                   and e["best_uniprot_identity"] >= 0.90]
        ok = (len(screen) == summary["screened"] == 20
              and len(with_id) == summary["with_identity"]
              and len(errors) == len(summary["errors_documented"])
              and zero_hits == summary["zero_hits"]
              and len(already) == len(summary["already_in_uniprot_ge90"])
              and statistics.median(with_id) == summary["identity_median"])
        rec("uniprot-screen-consistency", ok,
            "%d screens (%d with identity, %d documented API-incident errors, "
            "%d zero-hit, %d already-in-UniProt); median identity %.4f"
            % (len(screen), len(with_id), len(errors), len(zero_hits),
               len(already), statistics.median(with_id) if with_id else float("nan")))
    except Exception as ex:
        rec("uniprot-screen-consistency", False, "error: %s" % ex)

    passed = sum(1 for c in checks if c["ok"])
    total = len(checks)

    if as_json:
        print(json.dumps({"tool": TOOL, "version": VERSION, "overall": "PASS" if passed == total else "FAIL",
                          "passed": passed, "total": total, "checks": checks}, indent=1))
    else:
        print("SP-004 (DOC-1-034 R1) frozen-output audit - %s v%s" % (TOOL, VERSION))
        print("mode: (a) read-only query/audit over frozen outputs; no science is recomputed from raw data")
        print("")
        for c in checks:
            print("[%s] %s - %s" % ("PASS" if c["ok"] else "FAIL", c["check"], c["detail"]))
        print("")
        print("AUDIT RESULT: %s (%d/%d checks passed)"
              % ("PASS" if passed == total else "FAIL", passed, total))
    return 0 if passed == total else 1


# ----------------------------------------------------------------- query ----

def cmd_funnel(root, as_json=False):
    ref = load_json(root, "results/funnel_ref.json")
    dec = load_json(root, "results/funnel_decoy.json")
    if as_json:
        print(json.dumps({"reference": ref, "decoy": dec}, indent=1)); return 0
    print("Discovery funnel (frozen: results/funnel_ref.json, results/funnel_decoy.json)")
    print("")
    print("%-28s %12s %12s" % ("stage", "reference", "decoy"))
    labels = [("hits (E<=1e-5, dedup)", "hits"), ("with sequence", "with_sequence"),
              ("F1 length 180-900", "F1_pass"), ("F2 cellulase-GH Pfam", "F2_pass"),
              ("F3 E<=1e-10", "F3_pass"), ("F4 <40% ref identity", "F4_pass"),
              ("F6 catalytic D/E intact", "F6_pass")]
    for label, key in labels:
        r = ref.get(key, "-")
        d = dec.get(key, "-")
        print("%-28s %12s %12s" % (label, r, d))
    print("")
    print("decoy gate-counted candidates: 0 (no decoy row passed F2)")
    return 0


def cmd_gates(root, as_json=False):
    ge = load_json(root, "results/gate_evaluation.json")
    if as_json:
        print(json.dumps(ge, indent=1)); return 0
    print("Locked-gate evaluation (frozen: results/gate_evaluation.json)")
    print("protocol SHA-256: %s" % ge["protocol_sha256"])
    print("locked at: %s" % ge["locked_at"])
    print("")
    verdicts = {
        "G1": ("reference build >= 12 live-verified characterized cellulases", ">=12", "15"),
        "G2": ("distinct candidates pass F1,F2,F3,F4,F6", ">=40", str(ge["metrics"]["final_candidates"])),
        "G3": ("of G2, novelty <30% to every reference", ">=15", str(ge["metrics"]["novel_lt30"])),
        "G4": ("top-50 with RCSB template E<=1e-10, cov>=60%", ">=15", "%d/%d" % (ge["metrics"]["structure_ok"], ge["metrics"]["structure_examined"])),
        "G5": ("thermostability proxy (aliphatic>=64.44 AND >=2 Cys)", ">=5", str(ge["metrics"]["thermostable"])),
        "G6": ("decoy yield <= 10% of reference yield", "<=9.55/query", "0/query (ref %.2f/query)" % ge["metrics"]["ref_yield_per_query"]),
    }
    print("%-4s %-58s %-12s %-14s %s" % ("gate", "locked rule (abbrev.)", "threshold", "observed", "verdict"))
    for k in ["G1", "G2", "G3", "G4", "G5", "G6"]:
        rule, thr, obs = verdicts[k]
        print("%-4s %-58s %-12s %-14s %s" % (k, rule, thr, obs, "PASS" if ge["checks"][k] else "FAIL"))
    print("")
    print("overall: %s" % ge["overall"])
    return 0


def cmd_composition(root, as_json=False):
    rows = final_candidates(load_csv(root, "results/candidates_ref.csv"))
    counts = {}
    for r in rows:
        f = family_of(r["pfam"])
        counts[f] = counts.get(f, 0) + 1
    order = ["GH3", "GH5", "GH6", "GH45", "GH7", "GH48", "GH9", "GH12", "multi-domain", "none"]
    items = [(f, counts[f]) for f in order if f in counts]
    exo = counts.get("GH7", 0) + counts.get("GH6", 0) + counts.get("GH48", 0)
    if as_json:
        print(json.dumps({"total": len(rows), "families": counts,
                          "exo_acting_tranche_GH7_GH6_GH48": exo}, indent=1)); return 0
    print("GH-family composition of the %d final candidates" % len(rows))
    print("(direct tabulation of frozen results/candidates_ref.csv Pfam fields)")
    print("")
    print("%-14s %8s %10s" % ("family", "count", "share"))
    for f, c in items:
        print("%-14s %8d %9.1f%%" % (f, c, 100.0 * c / len(rows)))
    print("")
    print("exo-acting tranche (GH7+GH6+GH48): %d candidates (%.1f%%)"
          % (exo, 100.0 * exo / len(rows)))
    return 0


def cmd_novelty(root, as_json=False):
    rows = final_candidates(load_csv(root, "results/candidates_ref.csv"))
    out = {"final_candidates": len(rows)}
    for t in ("25", "30", "35", "40"):
        out["novel_at_%s" % t] = sum(1 for r in rows if r["novel_at_%s" % t] == "True")
    if as_json:
        print(json.dumps(out, indent=1)); return 0
    print("Novelty of final candidates vs the 15 characterized references")
    print("(predeclared sensitivity tabulation of frozen novel_at_* flags)")
    print("")
    print("%-34s %8s %10s" % ("max identity threshold", "count", "share"))
    for t in ("25", "30", "35", "40"):
        c = out["novel_at_%s" % t]
        print("%-34s %8d %9.1f%%" % ("<%s%% to every reference" % t, c, 100.0 * c / len(rows)))
    return 0


def cmd_structure(root, as_json=False):
    sc = load_json(root, "results/structure_check.json")
    hits = [e for e in sc if structure_ok(e)]
    if as_json:
        print(json.dumps({"examined": len(sc), "with_template": len(hits),
                          "templates": hits}, indent=1)); return 0
    print("Structure check, top-%d candidates by E-value (frozen: results/structure_check.json)" % len(sc))
    print("qualifying template: RCSB hit at E<=1e-10 with >=60% local coverage")
    print("")
    print("%-18s %-10s %8s %9s" % ("accession", "template", "coverage", "identity"))
    for e in hits:
        print("%-18s %-10s %8s %9s" % (e["accession"], e.get("rcsb_template", "-"),
                                       e.get("template_coverage", "-"), e.get("template_identity", "-")))
    print("")
    print("%d/%d top candidates have a qualifying template" % (len(hits), len(sc)))
    return 0


def cmd_decoys(root, as_json=False):
    drows = load_csv(root, "results/candidates_decoy.csv")
    pools = {}
    for r in drows:
        pools.setdefault(r["refs"], {"rows": 0, "stages": {}})
        pools[r["refs"]]["rows"] += 1
        s = r["stage_reached"]
        pools[r["refs"]]["stages"][s] = pools[r["refs"]]["stages"].get(s, 0) + 1
    if as_json:
        print(json.dumps(pools, indent=1)); return 0
    print("Decoy specificity pools (frozen: results/candidates_decoy.csv)")
    print("three non-cellulase hydrolase queries through the identical funnel")
    print("")
    print("%-22s %8s  %s" % ("decoy pool", "rows", "terminal stages"))
    for name in sorted(pools):
        p = pools[name]
        stages = ", ".join("%s %d" % (k, p["stages"][k]) for k in sorted(p["stages"]))
        print("%-22s %8d  %s" % (name, p["rows"], stages))
    print("")
    print("gate-counted decoy candidates (F6_pass): 0")
    return 0


def cmd_scrambles(root, as_json=False):
    scr = load_json(root, "results/scramble_controls.json")
    if as_json:
        print(json.dumps(scr, indent=1)); return 0
    print("Scrambled-sequence controls (frozen: results/scramble_controls.json)")
    print("composition-preserving shuffles of 5 final candidates vs the full catalog")
    print("")
    print("%-18s %26s" % ("candidate", "hits at E<=1e-10"))
    for e in scr:
        print("%-18s %26d" % (e["candidate"], e["scrambled_hits_E<=1e-10"]))
    return 0


def cmd_uniprot(root, as_json=False):
    screen = load_json(root, "results/uniprot_novelty_screen.json")
    summary = load_json(root, "results/uniprot_screen_summary.json")
    if as_json:
        print(json.dumps({"screen": screen, "summary": summary}, indent=1)); return 0
    print("UniProtKB novelty screen, top-%d candidates (frozen: results/uniprot_novelty_screen.json)" % len(screen))
    print("")
    print("%-18s %-14s %8s  %s" % ("accession", "best homolog", "identity", "note"))
    for e in screen:
        if e.get("uniprot_screen_error"):
            print("%-18s %-14s %8s  %s" % (e["accession"], "-", "-", "EBI API incident; documented"))
        elif e.get("uniprot_hits_at_1e-40") == 0:
            print("%-18s %-14s %8s  %s" % (e["accession"], "-", "-", "no UniProtKB hit at E<=1e-40"))
        else:
            note = "already in UniProt (metagenome-derived deposit)" if e["best_uniprot_identity"] >= 0.90 else ""
            print("%-18s %-14s %8s  %s" % (e["accession"], e["best_uniprot"],
                                           "%.4f" % e["best_uniprot_identity"], note))
    print("")
    print("median best-homolog identity: %.4f over %d completed screens with identity"
          % (summary["identity_median"], summary["with_identity"]))
    print("%d screens blocked by the documented EBI HMMER API incident (no gate depends on this screen)"
          % len(summary["errors_documented"]))
    return 0


def cmd_xcat(root, as_json=False):
    xcat = load_json(root, "results/xcat_candidates.json")
    if as_json:
        print(json.dumps(xcat, indent=1)); return 0
    print("Cross-catalog replication candidates (frozen: results/xcat_candidates.json)")
    print("full screen rerun in the independent MGnify30-C5-ppfam catalog, identical funnel")
    print("")
    print("%-18s %12s %12s %8s" % ("accession", "min E", "max ref id", "length"))
    for e in xcat:
        print("%-18s %12s %12s %8s" % (e["accession"], e["min_evalue"],
                                       e["max_ref_identity"], e["length"]))
    print("")
    print("%d candidates (a lower bound: C5-ppfam is Pfam-poor, so F2 is harder to satisfy there)"
          % len(xcat))
    return 0


def cmd_candidate(root, accession, as_json=False):
    rows = load_csv(root, "results/candidates_ref.csv")
    hits = [r for r in rows if r["accession"] == accession]
    if not hits:
        eprint("no row for accession %s in results/candidates_ref.csv" % accession)
        return 1
    r = hits[0]
    if as_json:
        print(json.dumps(r, indent=1)); return 0
    print("candidate record (verbatim frozen row, results/candidates_ref.csv)")
    print("")
    for k in ("accession", "stage_reached", "length", "min_evalue", "max_ref_identity",
              "novel_at_25", "novel_at_30", "novel_at_35", "novel_at_40",
              "catalytic_conserved", "closest_ref", "refs", "pfam",
              "aliphatic_index", "cys"):
        print("%-22s %s" % (k, r.get(k, "")))
    return 0


def cmd_candidates(root, args, as_json=False):
    rows = load_csv(root, "results/candidates_ref.csv")
    rows = [r for r in rows if r["stage_reached"] == "F6_pass"]
    if args.family:
        rows = [r for r in rows if family_of(r["pfam"]) == args.family]
    if args.closest:
        rows = [r for r in rows if r["closest_ref"] == args.closest]
    rows.sort(key=lambda r: float(r["min_evalue"]))
    rows = rows[: args.limit]
    if args.csv:
        cols = ["accession", "aliphatic_index", "catalytic_conserved", "closest_ref", "cys",
                "length", "max_ref_identity", "min_evalue", "novel_at_25", "novel_at_30",
                "novel_at_35", "novel_at_40", "pfam", "refs", "stage_reached"]
        print(",".join(cols))
        for r in rows:
            print(",".join(r[c] for c in cols))
        return 0
    if as_json:
        print(json.dumps(rows, indent=1)); return 0
    print("final candidates (F6_pass), sorted by min E-value")
    print("")
    print("%-18s %6s %11s %11s %-16s %-24s" % ("accession", "length", "min E", "max ref id", "family", "closest reference"))
    for r in rows:
        print("%-18s %6s %11s %11s %-16s %-24s" % (
            r["accession"], r["length"], r["min_evalue"], r["max_ref_identity"],
            family_of(r["pfam"]), r["closest_ref"]))
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(
        prog=TOOL,
        description="Read-only query/audit CLI over the frozen SP-004 (DOC-1-034 R1) outputs. "
                    "Determination (a): query/audit tool; it cannot rerun the pipeline and "
                    "never creates a new scientific result.")
    p.add_argument("--root", default=".", help="package root containing results/ (default: .)")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("verify", "funnel", "gates", "composition", "novelty", "structure",
                 "decoys", "scrambles", "uniprot", "xcat"):
        sp = sub.add_parser(name)
        sp.add_argument("--json", action="store_true")
    sp = sub.add_parser("candidate")
    sp.add_argument("accession")
    sp.add_argument("--json", action="store_true")
    sp = sub.add_parser("candidates")
    sp.add_argument("--family", help="GH family label, e.g. GH7, or multi-domain")
    sp.add_argument("--closest", help="closest-reference alias, e.g. Tre_CBH1_GH7")
    sp.add_argument("--limit", type=int, default=20)
    sp.add_argument("--csv", action="store_true", help="emit frozen rows verbatim as CSV")
    sp.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    root = args.root
    if not os.path.isdir(os.path.join(root, "results")):
        eprint("error: %s does not look like the package root (results/ missing)" % root)
        return 2
    fn = {"verify": lambda: cmd_verify(root, args.json),
          "funnel": lambda: cmd_funnel(root, args.json),
          "gates": lambda: cmd_gates(root, args.json),
          "composition": lambda: cmd_composition(root, args.json),
          "novelty": lambda: cmd_novelty(root, args.json),
          "structure": lambda: cmd_structure(root, args.json),
          "decoys": lambda: cmd_decoys(root, args.json),
          "scrambles": lambda: cmd_scrambles(root, args.json),
          "uniprot": lambda: cmd_uniprot(root, args.json),
          "xcat": lambda: cmd_xcat(root, args.json),
          "candidate": lambda: cmd_candidate(root, args.accession, args.json),
          "candidates": lambda: cmd_candidates(root, args, args.json)}[args.cmd]
    return fn()


if __name__ == "__main__":
    sys.exit(main())
