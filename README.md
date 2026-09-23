# SP-004 / DOC-1-034 - Novel Cellulases for Biofuel Production

## Summary (from `SP-004-DOC-1-034/README.md`)


**Locked-gate outcome: OVERALL PASS (6/6).** 12,451 hits -> 1,433 novel catalytically intact cellulase candidates (96.9% <30% identity to all 15 references); decoy yield 0; 30 cross-catalog replication candidates; 5/5 scrambled controls clean; 16/50 structure templates; 1,266 thermostability-proxy candidates.

- `protocol/protocol.json` (+ PROTOCOL_LOCK.txt, feasibility_log.md) - locked CAZyme-aware gates G1-G6
- `code/` - run_analysis.py (search/filter/structure), stage2_validation.py (cross-catalog, scrambles, UniProt screen), evaluate_gates.py, pubmed_grounding.py + pubmed_broaden.py
- `results/` - gate_evaluation.json, funnel_ref/decoy.json, candidates_ref/decoy.csv, structure_check.json, xcat_candidates.json, scramble_controls.json, uniprot_novelty_screen.json, run manifests, pubmed_grounding_all.json
- `data/` - reference_set_final.json (15 refs + 3 decoys, ACT_SITE + Pfam xrefs), raw HMMER caches, grounding (CAZy pages, UniProt pool, pubmed), validation caches
- `report/report.md` (full report + biofuel commercial analysis), `report/literature_ledger.md`, `paper/paper.md`, `figures/`

## Contents

- `SP-004-DOC-1-034/` - migrated unchanged from `science-program/projects/SP-004-DOC-1-034` (73 files)

## Provenance

Split out of the `science-program` repository (source commit `028a7141ed5f951a7b6e6517d4e72768d414a560`) on 2026-09-23. Every file is byte-identical to the source; `MIGRATION_MANIFEST.tsv` lists sha256, original path and new path for each of the 73 files.

Part of Udita Phookan's computational science program: every experiment locks its question, validation design, success gate and failure policy before outcome analysis, and negative results are preserved. Program-wide ledgers and standards live in the `science-program-ledger` repository.
