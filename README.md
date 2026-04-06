# Life Expectancy of Ukrainian Creative Workers Under Soviet Occupation

**Author:** Mark Symkin (2026)
**V1 paper:** Elza Berdnyk, Mark Symkin, and Alona Motiashova (2025, Harvard Graduate Masterclass)

---

## Read the paper

**[→ Full paper with all 24 figures](https://symkinmark.github.io/ukraine-creative-workers-v2/)**

---

## What this study finds

Ukrainian creative workers who emigrated from the Soviet sphere lived **4.04 years longer** on average than those who remained (mean age at death: 75.25 vs 71.22 years; Cohen's d=0.292; Cliff's δ=0.18; p<0.001; n=8,643).

Workers deported by the Soviet state — sent to Gulags, exile, or execution — lived **22.87 years less** than non-migrants (mean 48.35 years; d=1.656; p<0.001). The 1937 peak: 65 deported creative workers died in a single year — 35.5% of the entire deported cohort.

Internal transfers (workers who voluntarily moved within the USSR) showed **no significant LE difference** from non-migrants (+0.52 years; p=0.094) — confirming the advantage came from leaving the Soviet sphere entirely, not from geographic mobility within it.

---

## Dataset

- **Source:** Encyclopedia of Modern Ukraine (esu.com.ua) — 16,215 entries scraped
- **Analysable:** 8,643 individuals with confirmed Ukrainian nationality, death date, and determinable migration status
- **Four groups:** Migrated (n=1,280) · Non-migrated (n=6,030) · Internal transfer (n=1,150) · Deported (n=183)
- **Primary dataset:** `ukraine_v2/esu_creative_workers_v2_3.csv`

---

## Repository structure

```
ukraine_v2/
├── PAPER_DRAFT.md              ← Full paper (Markdown source)
├── SCIENTIFIC_METHODOLOGY.md   ← Detailed methodology documentation
├── AI_METHODOLOGY_LOG.md       ← AI usage transparency log
├── generate_analysis.py        ← Statistical analysis + all 24 charts
├── build_paper_html.py         ← Builds docs/index.html from paper + charts
├── esu_creative_workers_v2_3.csv  ← Primary dataset (V2.3)
├── charts/                     ← All 24 generated figures (PNG)
└── chart_docs/                 ← Plain-language description of each figure
docs/
└── index.html                  ← Built paper (auto-generated, do not edit)
v1_paper.pdf                    ← V1 paper (Harvard Masterclass, 2025)
```

---

## Reproduce the analysis

```bash
# Generate all statistics and charts
python3 ukraine_v2/generate_analysis.py

# Rebuild the paper HTML
python3 ukraine_v2/build_paper_html.py
```

**Dependencies:** `pandas`, `numpy`, `scipy`, `matplotlib`, `seaborn`, `lifelines`

---

## Citation

Symkin, Mark. 2026. "Life Expectancy of Ukrainian Creative Industry Workers During the Soviet Occupation." V2.3. GitHub repository: https://github.com/symkinmark/ukraine-creative-workers-v2.

V1: Berdnyk, Elza, Mark Symkin, and Alona Motiashova. 2025. "Life Expectancy of Ukrainian Creative Industry Workers During the Soviet Occupation." Final Project, Harvard Graduate Masterclass on Entering Global Academia. https://github.com/symkinmark/ukraine-creative-workers-v2/blob/main/v1_paper.pdf
