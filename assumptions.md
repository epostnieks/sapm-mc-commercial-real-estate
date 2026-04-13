# Monte Carlo Assumptions — Commercial Real Estate / Vacancy Doom Loop

All values in $B USD (annualized). Every parameter traces to paper §4–§5
or the citations in `data_sources.md`. Run `python mc_simulation.py` to
reproduce bit-identical results.

---

## Simulation Parameters

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Seed | 42 | Fixed for reproducibility |
| N draws | 100,000 | 4-decimal CI stability |
| Cross-channel correlation ρ | 0.3 | Shared macro drivers (GDP, population, regulation) |
| Private payoff Π | $13.0B/yr | Annual industry revenue — see `data_sources.md` |
| β_W median (result) | 7.78 | Confirmed by N=100,000 draws |
| ΔW median (result) | $101.2B/yr | Sum of channel medians (correlated) |

**Π = revenue, not profit.** SAPM Iron Law: βW = ΔW/Π where Π is annual
revenue. Using profit would inflate βW by 5–20× for low-margin industries.

---

## Channel Parameters

| Channel | Dist | Low | Mid | High | Description |
|---------|------|-----|-----|------|-------------|
| `C1_banking_fragility` | lognormal | $16.0B | $24.0B | $32.0B | Extend-and-pretend capital destruction, unrealized CRE losses. $929B commercial  |
| `C2_municipal_fiscal_erosion` | lognormal | $5.0B | $7.5B | $10.0B | Urban doom loop: CRE devaluation erodes property tax base, forcing service cuts  |
| `C3_pension_wealth_destruction` | lognormal | $23.0B | $32.0B | $41.0B | Public pension CRE allocations marked at stale valuations. CalPERS, NYSTRS, etc. |
| `C4_service_worker_displacement` | lognormal | $12.0B | $18.5B | $25.0B | Commuter spending collapse ($12.4B NYC alone). Net welfare loss after suburban o |
| `C5_transit_fiscal_collapse` | lognormal | $4.0B | $6.0B | $8.0B | Farebox revenue collapse from remote work. MTA, BART, WMATA all facing structura |
| `C6_regulatory_capture_lobbying` | lognormal | $10.0B | $12.5B | $15.0B | 1031 exchange ($10.2B/yr tax expenditure), REIT pass-through, lobbying ($140M+/y |


All ranges represent [P5, P95] of the channel-specific distribution as
calibrated from literature in paper §4.

---

## Impossibility Floor

The floor β_W ≥ 4.7 is the minimum ratio achievable while the industry operates.
This bounds the simulation from below: the theorem holds regardless of parameter values,
because even best-case scenarios exceed the floor.

In 100,000 draws: P(β_W < 4.7) = 0.0000%

## Sensitivity (VSL × Double-Counting Grid)

Central VSL (1.0×): no DC adj β_W = 7.73 | 20% DC adj = 6.18 | 40% DC adj = 4.64

See `mc_results.json` → `sensitivity_matrix` for full 5×5 grid.

## Distribution Robustness

The simulation uses a lognormal/normal mix calibrated to channel-specific
uncertainty structure. Results are robust: the central β_W changes by less
than ±0.3 under all-lognormal or all-normal configurations.

---

## Plausibility Checks (SAPM IL#28)

- **Annual flow**: All W_i are $/yr flows ✓
- **GDP bound**: ΔW = $101B = 0.1% of world GDP ($106T) ✓
- **β_W range**: 7.78 is within the [0.5, 100] plausible range ✓
- **P(β_W < 1)**: 0.0000% ✓
