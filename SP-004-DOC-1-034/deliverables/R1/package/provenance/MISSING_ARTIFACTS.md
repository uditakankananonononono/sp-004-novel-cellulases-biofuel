# Missing artifacts registry - DOC-1-034 R1

Per the packaging constraint, unrecoverable artifacts are marked missing and
the package is narrowed accordingly. Nothing was recreated from memory.

1. **code/ (R1 analysis code)** - run_analysis.py, stage2_validation.py,
   evaluate_gates.py, pubmed_grounding.py, pubmed_broaden.py. Referenced by
   the project README; never committed to the repository (commit 6cfa8a7
   contains exactly the 22 packaged files); absent from all recovered Drive
   archives. Consequence: the pipeline cannot be re-executed; the packaged
   CLI is determination (a), read-only query/audit over frozen outputs.
2. **data/processed/reference_set_final.json** - the 15-reference manifest
   with retrieval hashes. Consequence: the final alias-to-accession mapping
   is auditable only through the report pairings and the locked protocol's
   accession list (see the note under paper Appendix B).
3. **protocol/PROTOCOL_LOCK.txt** - referenced by the README. Mitigated:
   the locked protocol hash is embedded in results/gate_evaluation.json and
   the packaged protocol/protocol.json reproduces it exactly.
4. **results/pubmed_grounding_all.json** - raw eutils grounding. Mitigated:
   report/literature_ledger.md preserves the full query-and-hit record from
   which the paper's reference list is drawn.
5. **SP-004-raw-validation-fasta-3.tar.gz** - only the "-3b" archive exists
   in the Drive folder; whether 3b supersedes 3 is unverifiable.
6. **Original execution environment** - no requirements file, container
   image, or Python dependency versions recoverable. Contributes to the
   determination-(a) CLI decision.
7. **API-incident error trail** - results/uniprot_screen_summary.json
   references "exact error trail in /tmp logs"; ephemeral, unrecovered. The
   incident remains documented by the summary JSON and by resubmission
   counts in results/run_manifest_validation.json.
