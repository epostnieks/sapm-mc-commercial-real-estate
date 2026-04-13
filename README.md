# SAPM Monte Carlo — Commercial Real Estate / Vacancy Doom Loop

**Public replication repository for quantitative results in:**

> Postnieks, E. (2026). *Commercial Real Estate (Vacancy Doom Loop).* SAPM Working Paper. SSRN.

This repository provides everything needed to independently reproduce, audit,
and extend the Monte Carlo simulation underlying the paper's core results.
The paper is available on SSRN.

---

## Results (N = 100,000 draws, seed = 42)

| Statistic | Value |
|-----------|-------|
| **β_W median** | **7.78** |
| β_W mean | 7.83 |
| β_W std | 0.85 |
| **90% CI** | **[6.5, 9.3]** |
| 99% CI | [6.1, 10.0] |
| P(β_W < 1) | 0.0000% |
| **ΔW median** | **$101.2B/yr** |
| Π (revenue) | $13.0B/yr |

**β_W = 7.78** means the commercial real estate industry destroys **$7.78 in system
welfare for every $1.00 in revenue** — across 6 channels and 100,000 Monte Carlo draws.

**Classification**: Class 2 — Intractability

---

## What Is β_W?

```
β_W = ΔW / Π
```

- **ΔW** = total annualized welfare destruction ($B/yr) across all channels
- **Π** = annual industry **revenue** ($B/yr) — not profit

β_W > 1: industry destroys more welfare than it captures in revenue.
β_W > 3: Strong Intractability threshold — reform requires structural replacement.

---

## Quick Start

```bash
git clone https://github.com/epostnieks/sapm-mc-commercial-real-estate.git
cd sapm-mc-commercial-real-estate
pip install numpy scipy
python mc_simulation.py
```

Expected output: `β_W median : 7.78` and `ΔW median : $101.2B/yr`

---

## Welfare Channels

| Channel | Median ($B/yr) | 90% CI | Distribution |
|---------|---------------|--------|--------------|
| C1_banking_fragility | $24.0B | [$18.0B, $32.0B] | Lognormal |
| C2_municipal_fiscal_erosion | $7.5B | [$5.6B, $10.0B] | Lognormal |
| C3_pension_wealth_destruction | $32.0B | [$25.0B, $41.0B] | Lognormal |
| C4_service_worker_displacement | $18.5B | [$13.7B, $25.0B] | Lognormal |
| C5_transit_fiscal_collapse | $6.0B | [$4.5B, $8.0B] | Lognormal |
| C6_regulatory_capture_lobbying | $12.5B | [$10.4B, $15.0B] | Lognormal |
| **Total ΔW** | **$101.2B** | **[$84.7B, $121.0B]** | Correlated (ρ=0.3) |

---

## Impossibility Floor

The floor β_W ≥ 4.7 cannot be breached by any policy while the
industry continues to operate. In 100,000 draws, only **0.0000%**
fall below this floor — confirming the structural constraint.

## Repository Contents

| File | Description |
|------|-------------|
| `mc_simulation.py` | Self-contained simulation — no private pipeline imports |
| `mc_results.json` | Pre-run results (100K draws, seed=42) — matches paper |
| `mc_histogram.json` | Binned β_W distribution (80 bins) for companion chart |
| `assumptions.md` | Every parameter: value, derivation, source |
| `data_sources.md` | Full citation list for all empirical inputs |

---

## Replication Notes

Results are seeded and deterministic. Tested with:
```
numpy==1.26.4  scipy==1.12.0  Python 3.11.9
```

The `median` and `ci_90` (to 1 decimal) match exactly across compatible versions.

---

## License

CC BY 4.0. Cite as:

> Postnieks, E. (2026). *SAPM Monte Carlo — Commercial Real Estate (Vacancy Doom Loop)*.
> GitHub: epostnieks/sapm-mc-commercial-real-estate.
> https://github.com/epostnieks/sapm-mc-commercial-real-estate
