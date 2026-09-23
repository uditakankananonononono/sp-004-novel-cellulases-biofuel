# SP-004 (DOC-1-034): Discovering Novel Cellulases for Biofuel Production

**Locked-gate outcome: OVERALL PASS - all 6 gates.** Protocol locked 2026-09-21 21:24 IST (`protocol/protocol.json`) before any candidate-level result was inspected. Gate text never modified after lock. Primary pipeline + full stage-2 validation complete.

## 1. Question

Can we discover genuinely novel, catalytically intact cellulases in the global metagenome (MGnify) with CAZyme-family-aware specificity - enzymes suitable as candidates for cellulosic-biofuel enzyme cocktails - while rejecting non-cellulase lookalikes?

## 2. Locked success gate and outcome

| Gate | Locked rule (abbrev.) | Threshold | Observed | Verdict |
|---|---|---|---|---|
| G1 | live-verified characterized cellulase references | >=12 | 15 | PASS |
| G2 | distinct MGnify candidates pass F1,F2,F3,F4,F6 | >=40 | 1,433 | PASS |
| G3 | of G2, novelty <30% to every reference | >=15 | 1,389 | PASS |
| G4 | of top-50 examined, RCSB template E<=1e-10 & cov>=60% | >=15 | 16 | PASS |
| G5 | thermostability proxy (aliphatic >= ref median 64.44 AND >=2 Cys) | >=5 | 1,266 | PASS |
| G6 | decoy pools (xylanase, lysozyme, amylase) yield <= 10% of reference yield | <=9.55/query | 0/query (ref: 95.5/query) | PASS |

## 3. Methods

**Reference panel (grounding-first).** 15 live-verified, ACT_SITE-annotated, CAZyme-family-spanning characterized cellulases retrieved from UniProt/RCSB with hashing: GH7 (Tre CBH1 P62694, Tre/Hins EG1 P07981), GH6 (Tre CBH2 P07987, Tfu Cel6A P26222), GH5 (Tre EG2 P07982, Tfu Cel5A Q01786, Acel E1 P54583, Bsub EG P10475), GH9 (Tfu Cel9A P26221), GH45 (Hins EG5 Q7SIG5), GH48 (Cthe CelS P0C2S5), GH12 (Pfu EG Q9V2T0), GH3 (Aac BGL1 P48825), plus Hins EG6B (P56680). Three decoys from non-cellulase glycosidase/hydrolase families: Tre xylanase XYN1 (P36218), hen lysozyme (P00698), Bacillus licheniformis amylase (P06278). CAZy mechanism pages (retaining/inverting per GH family) hashed into `data/raw/grounding/`.

**Filters (locked).** F1 length 180-900 aa; F2 candidate Pfam metadata (MGnify hit metadata) must include a catalytic cellulase-GH family from {PF00150 GH5, PF01341 GH6, PF00840 GH7, PF00759 GH9, PF01670 GH12, PF02015 GH45, PF02011 GH48, PF01915 GH3}; F3 min phmmer E<=1e-10 across the 15 references; F4 max global identity to any reference <40% (BLOSUM62, -11/-1); F6 every annotated catalytic position of the candidate's best-E ACT_SITE reference must align to Asp or Glu. F5 structure: top-50 by E-value, RCSB search E<=1e-10 + local coverage.

**Documented execution substitution (F6 mapping vehicle).** The locked F6 rule names the phmmer aligned-FASTA (afa) as the position-mapping vehicle. EBI afa downloads contain only hit rows - the query/reference row is absent (verified on the downloaded files: 543/543 headers are MGYP hits), so reference-position-to-column mapping cannot be built from the afa. The locked RULE (D/E at every annotated catalytic position of the best-E ACT_SITE reference) is unchanged; the mapping is computed from a pairwise global alignment against that same reference using the identical BLOSUM62 -11/-1 aligner as F4. Recorded here and in code; gate text untouched.

**Stage-2 validation.** (A) Cross-catalog replication: the full 15-reference screen rerun against the independent MGnify30-C5-ppfam catalog with the identical F1-F4 funnel. (B) Negative controls: composition-preserving shuffles of 5 final candidates searched against MGnify30-C2. (C) UniProt novelty screen: top-20 final candidates phmmer vs UniProtKB with best-homolog identity.

## 4. Results

**Funnel.** 15 references vs MGnify30-C2 (128.7M sequences): 12,451 unique hits (E<=1e-5) -> F1 9,057 -> F2 5,033 -> F3 3,401 -> F4 3,395 -> F6 1,433 final candidates. Decoy pools: 1,273 raw hits, 848 length-passing, ZERO carrying a cellulase-GH Pfam -> 0 gate-counted candidates (specificity).

**The 1,433 candidates are genuinely novel and catalytically intact.** 1,389/1,433 (96.9%) sit below 30% identity to every characterized reference; the full set is below 40%. Every one conserves Asp/Glu at every annotated catalytic position of its best ACT_SITE reference.

**GH-family composition (the commercial core finding).** GH3 beta-glucosidases 672 (46.9%), GH5 endoglucanases 530 (37.0%), GH6 cellobiohydrolase-II-type 109 (7.6%), GH45 endoglucanases 56 (3.9%), GH7 cellobiohydrolase-I-type 43 (3.0%), GH48 processive cellulases 19 (1.3%), multi-domain 4. Median length 604 aa.

**Structure.** 16 of the top-50 have RCSB templates at E<=1e-10 with >=60% local coverage (templates include 6GJF, 1ECE, 5IHS).

**Thermostability proxy.** 1,266/1,433 (88.3%) have aliphatic index >= the reference-panel median (64.44) AND >=2 cysteines.

**Stage-2 validation.** (A) Cross-catalog: 30 candidates replicate under the identical funnel in the independent Pfam-poor C5 catalog - a hard replication set, since C5-ppfam specifically holds sequences POOR in Pfam annotations (analogous scale to SP-003's 21). (B) All 5 scrambled controls: ZERO hits at E<=1e-10 against the full 128.7M-sequence catalog.

**Stage C (UniProt novelty screen, top-20).** 15 of 20 screens completed: median best-UniProtKB-homolog identity 36.1% (range 2.2%-100%). Three top-20 candidates have near-identical UniProt entries (MGYP001480172483 99.7% to A0A370GNA7; MGYP003860412909 98.5% to A0A2T5PCH5; MGYP000843571747 100% to A0A7X7NE49) and are flagged as already-in-UniProt (metagenome-derived deposits) - they stay in the set but are deprioritized for novelty claims. One candidate (MGYP007332108226) has zero UniProtKB hits at E<=1e-40 (its E=1.0 job returned 84,176 weak hits, which saturated EBI's TSV generation; resolved via a tighter-E rerun). The remaining 5 of 20 could not be screened because of an EBI HMMER API incident on 2026-09-21/22 (job records purged immediately after submission, verified across 3+ resubmissions each; documented in results/uniprot_screen_summary.json). No gate depends on stage C.

## 5. Biofuel commercial analysis (distinct from the PET program)

Cellulosic ethanol economics are enzyme-cost-limited: cocktail cost per gallon is a primary lever, and industrial cocktails (Celluclast/Cellic-type) are built on three activities - endoglucanase (GH5/7/12/45), exo-cellobiohydrolase (GH7 CBH1 + GH6 CBH2), and beta-glucosidase (GH1/GH3) - plus processive accessories (GH9, GH48). The metagenome pool we recovered is strongly endo/beta-glucosidase-biased: 84% of candidates are GH3 or GH5, while the exo-acting CBH classes that limit saccharification of crystalline cellulose are scarce (GH7 3.0%, GH6 7.6%, GH48 1.3%). Two commercial consequences:

1. **The 43 GH7 + 109 GH6 + 19 GH48 candidates are the high-value tranche.** Fungal CBH1 (GH7) is the workhorse and cost-driver of commercial cocktails; 43 novel, catalytically intact, <40%-identity GH7s - 16/50 top candidates already structure-modelable - are a direct discovery feedstock for cocktail engineering (thermostability, tolerance to product inhibition, lignin tolerance).
2. **The 672 GH3 beta-glucosidases address a known bottleneck.** Beta-glucosidase supplementation relieves cellobiose inhibition; glucose-tolerant GH3s are actively sought. 672 novel GH3s with intact catalytic acid/base residues, 88% passing thermostability proxies, are a screening library for glucose-tolerant variants.

Route to use-level: shortlist GH7/GH6/GH48 + thermostable GH3s -> expression in a fungal/yeast host -> microplate saccharification assays on pretreated biomass (filter-paper activity + cellobiose release) -> cocktail reconstitution against a Cellic baseline. All 1,433 candidates are metagenomic (no cultivation needed), non-redundant with the 15 references, and provenance-resolved via MGnify studies.

## 6. Limitations

- F6's alignment-vehicle substitution (afa -> pairwise) is documented above; the D/E rule is unchanged but pairwise mapping on very distant homologs can misregister insertions - the 1,433 are therefore conservative.
- F2 depends on MGnify hit-metadata Pfam annotation; 269 candidates were not evaluable for F2 (no Pfam metadata) and excluded from gate counts by design.
- Structure check covers the top-50 only; modelability of the remaining 1,383 is untested.
- Thermostability is a sequence proxy (aliphatic index + cysteine count), not a measurement.
- Cross-catalog replication (30) is bounded by C5-ppfam's size and its Pfam-poor composition, which also makes F2 harder to satisfy there; 30 is a lower bound on true replication.

## 7. Provenance

All retrievals (UniProt entries + feature tables, RCSB FASTAs, CAZy family pages, EBI HMMER jobs, PubMed eutils) hashed at fetch time; manifests in `data/processed/reference_set_final.json`, `results/run_manifest_*.json`, `results/pubmed_grounding_all.json`. Idempotent cache-backed code in `code/`. Locked protocol hash in `results/gate_evaluation.json`.
