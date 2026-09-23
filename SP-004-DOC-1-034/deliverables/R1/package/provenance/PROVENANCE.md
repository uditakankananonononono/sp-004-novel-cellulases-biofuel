# Provenance chain - DOC-1-034 R1

1. Protocol locked 2026-09-21 21:24 IST, before any candidate-level result
   was inspected (protocol/protocol.json; SHA-256
   a90624ce91b33a59519677523df712047c86e977cc863ae9a164bb117079c17d).
2. Primary funnel run against EBI HMMER API / MGnify30-C2 2026_07
   (results/run_manifest_ref.json, 15 job UUIDs; decoys:
   results/run_manifest_decoy.json, 3 job UUIDs).
3. Stage-2 validation 2026-09-21/22 (results/run_manifest_validation.json,
   40 job UUIDs + resubmission counts for the API-incident screens).
4. Frozen gate record results/gate_evaluation.json (embeds the protocol
   SHA-256; the packaged protocol.json reproduces it exactly).
5. Program repository commit 6cfa8a7 ("Add SP-004 cellulase discovery funnel
   and candidate triage project") - the only commit touching the project;
   the 22 packaged frozen files are byte-identical to that tree.
6. Drive archive SP-004-deliverables.tar.gz (SHA-256 20db2992fc6289563810a9
   47d188bad377af2286b4f470c2da3b4b8cb0bde348, 449,890 bytes) independently
   recovered and verified byte-identical to the repository tree.
7. This package: frozen artifacts + paper (PDF/source) + audit CLI + tests
   + provenance + MANIFEST.sha256. Packaging added no scientific content;
   every number in the paper is verbatim from a frozen artifact or a direct
   tabulation of a frozen table, marked as such.

## Raw-byte archive registry (program Drive folder; hashed at packaging 2026-09-23)

| Archive | Bytes | SHA-256 |
|---|---|---|
| SP-004-raw-hmmer.tar.gz | 15,846,711 | a898e3e8c7aad22a5524d2068f9a5ec96b96885864cf82e13b773069dcaedab1 |
| SP-004-raw-grounding.tar.gz | 175,732 | 1e12d5b9f4d1aa7b5b8ff123ab3244c8f76ff80bf3ec1d94c9e4dd3c0fa0839a |
| SP-004-raw-validation-fasta-1.tar.gz | 220,438 | 2e1379fb6bd20ad26a850113d962eff6715c00812256207d8eb0ac077436c753 |
| SP-004-raw-validation-fasta-2.tar.gz | 47,700 | 635c5cf6e2f10d0ae43d433687515fa2292d2669f18c5082020778d5a2074dfb |
| SP-004-raw-validation-fasta-3b.tar.gz | 5,360,256 | 0d907fbc2bc8f82c4723eae6baa03863c6001287a94d094162851c36b6568939 |
| SP-004-raw-validation-fasta-4.tar.gz | 6,516,614 | 20cbea15bd72e843ffbfbb039136131ddecf078e56181116c90e60c35732d21f |
| SP-004-raw-validation-fasta-5.tar.gz | 79,034 | 543a7eef12ea1062c8a8e941304c608395de55fb85bd2d842968547703e54f74 |
| SP-004-raw-validation-tsv-meta.tar.gz | 13,068,055 | 5bea8762537b46243d63bb631b23371b1564e09d2b27aa194996ddfb3976d523 |
| SP-004-rawvf3-uniprot_071737.tar.gz | 6,590,333 | 5bcb2a22150209609b9da4b796ddb06b5de7a811ee56f6e919ff557eba546f4e |
| SP-004-rawvf3-uniprot_412909.tar.gz | 5,134,480 | c9ff7dfa900dba1116a19ac3f180cffbbb24ac610789c69f2fb2dc3d541ff953 |
| SP-004-rawvf3-uniprot_695315.tar.gz | 6,343,456 | 9a4acb1b0df412b539999fb015c0cdf086a19e2e4884d4ef2b4495cea77297bd |
| SP-004-rawvf3-uniprot_933065.tar.gz | 9,326,149 | 9950bacd44bb1af4999ad3f6d47b2831efbed589670c376581ae0ded039d861d |
| SP-004-deliverables.tar.gz | 449,890 | 20db2992fc6289563810a947d188bad377af2286b4f470c2da3b4b8cb0bde348 |

Drive folder: https://drive.google.com/drive/folders/1WYQZH9bFnEOI1Tq8NZ6XfVg6w5cF-PZk

NAME-COLLISION NOTE (for auditors): the same Drive folder contains
SP-004-R2..R6-prefixed archives and SP-004-small-protein-evidence-gap-*.tar.gz.
Those belong to other experiments sharing the SP-004 sequence number (a PRIDE
proteomics arc and the DOC-2-077 small-protein arc), not to DOC-1-034
cellulase R1, and are excluded from this package.
