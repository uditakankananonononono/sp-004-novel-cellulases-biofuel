# SP-004 feasibility log (recorded BEFORE protocol lock)

Live checks executed 2026-09-21.

- CAZy (cazy.org) reachable; family pages GH1/3/5/6/7/9/12/44/45/48 downloaded and
  mechanism (retaining/inverting) extracted per family (raw HTML hashed in
  data/raw/grounding/cazy_GH*.html). Ensembl not used (unreachable per program constraint).
- UniProtKB live queries built the characterized-cellulase panel: 15 enzymes across
  GH3, GH5, GH6, GH7, GH9, GH12, GH45, GH48 with ACT_SITE features and Pfam xrefs
  (Trichoderma reesei CBH1/CBH2/EG1/EG2, Aspergillus aculeatus BGL1, Humicola
  insolens EG1/EG6B/EG5, Thermobifida fusca Cel6A/Cel9A/Cel5A, Acetivibrio
  (Clostridium) thermocellum CelS, Acidothermus cellulolyticus E1, Bacillus
  subtilis EG, Pyrococcus furiosus EG). Raw JSON + FASTA hashed.
- Grounding negatives: the T. reesei name-based queries returned 0 under the exact
  names first tried ("Cellobiohydrolase 1"); the panel was rebuilt from live
  organism-level queries instead of recalled accessions. Pyrococcus furiosus
  endoglucanase (Q9V2T0) carries no ACT_SITE annotation - recorded; catalytic
  filter routes around it via next-best annotated reference.
- Decoy hydrolases verified live: T. reesei xylanase 1 (P36218), hen lysozyme C
  (P00698), B. licheniformis alpha-amylase (P06278).
- EBI HMMER API v1 with MGnify30-C2 proven end-to-end during SP-003 (same
  sandbox, same day); afa (aligned FASTA) download verified available per job.
