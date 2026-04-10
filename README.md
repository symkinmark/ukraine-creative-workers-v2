# Life Expectancy of Ukrainian Creative Workers Under Soviet Occupation

**Author:** Mark Symkin (2026)
**V1 paper:** Elza Berdnyk, Mark Symkin, and Alona Motiashova (2025, Harvard Graduate Masterclass)

---

## Read the paper

**[→ Full paper with all figures](https://symkinmark.github.io/ukraine-creative-workers-v2/)**

---

## What this study finds

Ukrainian creative workers who emigrated from the Soviet sphere lived **3.98 years longer** on average than those who remained (mean age at death: 75.42 vs 71.44 years; Cohen's d=0.292; Cliff's δ=0.18; p<0.001; n=8,590).

Workers deported by the Soviet state — sent to Gulags, exile, or execution — lived **22.05 years less** than non-migrants (mean 49.39 years; d=1.613; p<0.001). The 1937 peak: 67 deported creative workers died in a single year — 34.4% of the entire deported cohort.

Internal transfers (workers who voluntarily moved within the USSR) showed **no significant LE difference** from non-migrants (+0.35 years; p=0.271) — confirming the advantage came from leaving the Soviet sphere entirely, not from geographic mobility within it.

---

## Dataset

- **Source:** Encyclopedia of Modern Ukraine (esu.com.ua) — 16,215 entries scraped
- **Analysable:** 8,590 individuals with confirmed Ukrainian nationality, death date, and determinable migration status
- **Four groups:** Migrated (n=1,324) · Non-migrated (n=5,960) · Internal transfer (n=1,111) · Deported (n=195)
- **Primary dataset:** `ukraine_v2/esu_creative_workers_v2_6.csv`
- **AI classification error rate:** 3.2% (200-entry stratified validation, complete)

---

## Repository structure

```
ukraine_v2/
├── PAPER_DRAFT.md              ← Full paper (Markdown source, V3.0 restructured)
├── SCIENTIFIC_METHODOLOGY.md   ← Detailed methodology & replication guide
├── AI_METHODOLOGY_LOG.md       ← AI usage transparency log (15 phases)
├── generate_analysis.py        ← Statistical analysis + all charts
├── build_paper_html.py         ← Builds docs/index.html from paper + charts
├── check_paper_numbers.py      ← Verifies all 177 numeric claims against dataset
├── esu_creative_workers_v2_6.csv  ← Primary dataset (V2.6)
├── charts/                     ← Generated figures (33 static PNGs + 31 interactive Plotly)
├── chart_docs/                 ← Plain-language description of each figure
└── validation/                 ← 200-entry validation review interfaces
docs/
└── index.html                  ← Built paper (auto-generated, do not edit)
v1_paper.pdf                    ← V1 paper (Harvard Masterclass, 2025)
```

### Paper structure (V3.0)

The paper uses a progressive-revelation structure: each section answers a question raised by the previous one.

| Section | Content |
|---|---|
| §1 Introduction | Historical context, Executed Renaissance, research question, political sensitivity |
| §2 Prior Study | V1→V3.0 expansion, gap narrowing explained |
| §3 Data and Methods | ESU source, classification protocol, validation |
| §4 The Mortality Gap | Three core findings: 3.98-year gap, 22-year deportee deficit, internal transfer null |
| §5 Who, When, Where | Patterns by profession, cohort, gender, geography, period |
| §6 Statistical Robustness | OLS, PSM, Cox PH, time-varying, sensitivity, missing-worker bias |
| §7 Discussion | Four mechanisms, causation caveats, historical interpretation |
| §8 Limitations | 8 documented limitations |
| §9 Conclusion | Conservative lower bound, future priorities |
| Appendix A | 18 supplementary figures |
| Appendix B | Full robustness tables and model specifications |

---

## Reproduce the analysis

```bash
# Generate all statistics and charts
python3 ukraine_v2/generate_analysis.py

# Rebuild the paper HTML
python3 ukraine_v2/build_paper_html.py

# Verify all 177 numeric claims in the paper
python3 ukraine_v2/check_paper_numbers.py
```

**Dependencies:** `pandas`, `numpy`, `scipy`, `matplotlib`, `seaborn`, `lifelines`, `plotly`

---

## Citation

Symkin, Mark. 2026. "Observed Age at Death Among Ukrainian Creative Workers Under Soviet Occupation: A Quantitative Study Using the Encyclopedia of Modern Ukraine." V3.0. GitHub repository: https://github.com/symkinmark/ukraine-creative-workers-v2.

V1: Berdnyk, Elza, Mark Symkin, and Alona Motiashova. 2025. "Life Expectancy of Ukrainian Creative Industry Workers During the Soviet Occupation." Final Project, Harvard Graduate Masterclass on Entering Global Academia. https://github.com/symkinmark/ukraine-creative-workers-v2/blob/main/v1_paper.pdf
