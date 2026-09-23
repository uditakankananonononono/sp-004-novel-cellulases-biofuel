# Sculpted Project Summary - Novel Cellulases for Biofuel Production

## Status
R1 locked-gate positive, 6/6 gates passed. This is a validated computational discovery funnel and candidate resource, not biochemical proof.

## Useful discovery
A CAZyme-aware, catalytic-residue-constrained search of 128.7 million MGnify proteins reduced 12,451 hits to 1,433 candidates. Ninety-six point nine percent are below 30% identity to all 15 characterized references. Three non-cellulase hydrolase decoy pools produced zero gate-counted candidates; five composition-preserving scrambled sequences produced zero hits; an independent catalog yielded 30 candidates.

The surprising useful angle is compositional scarcity: 84% of candidates are GH3/GH5, while only 171 are in exo-acting GH6/GH7/GH48 classes. That shifts priority from "screen everything" to a compact, high-value exo-acting tranche for cocktail research, alongside a large GH3 library for glucose-tolerance hypotheses.

## What is new
The project combines family-aware metagenome search, locked catalytic-site conservation, non-cellulase decoys, independent-catalog replication, scrambled controls, structural modelability checks and live UniProt novelty screening. It does not treat sequence similarity alone as enzyme discovery.

## Why it matters
Cellulosic-biofuel enzyme cocktails depend on complementary endo-, exo- and beta-glucosidase activity. A provenance-resolved shortlist reduces a 128.7-million-protein catalog to auditable candidate tranches for later expression and activity testing.

## Working tool/application
The reusable application is a candidate-triage workflow that accepts characterized references plus catalytic annotations and returns:
- gate-by-gate candidate tables;
- decoy and scrambled-control diagnostics;
- novelty flags against characterized and UniProt pools;
- family composition and scarce-function tranches;
- structural-modelability and sequence-proxy annotations;
- complete provenance and abstentions.

It supports research prioritization only. Thermostability, cellulose hydrolysis, substrate specificity, expression yield and cocktail synergy remain unmeasured.

## Top-lab reviewer questions
1. Do the 171 exo-acting candidates retain activity on crystalline cellulose after expression?
2. Does the family scarcity persist after structure-based adjudication and domain-architecture controls?
3. Can a predeclared structure/register round reduce pairwise catalytic-position misregistration?
4. Which candidates improve a commercial baseline cocktail under matched protein loading?

## Next computational round
Before any wet-lab claim, run an orthogonal structure/domain/register round on the exo-acting tranche with family-stratified controls, independent structure resources, topology/tunnel checks, and frozen pass/failure gates. Preserve the three near-identical UniProt deposits as novelty negatives.

## Project package status
The archive includes a technical report, research paper, literature ledger, locked protocol, results tables, validation artifacts and figures. It is substantive but not yet a full graduated multi-round project. A polished approximately 20-page designed report, tested standalone triage tool, external replication and final synthesis remain required.

## Drive
Primary deliverable: https://drive.google.com/file/d/1AzQ7-r-DqBrH8nQa9ixj35LPdtP8GpFX/view?usp=drivesdk&authuser=uditakankana%40gmail.com
