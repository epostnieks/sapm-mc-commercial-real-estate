# Data Sources — Commercial Real Estate Monte Carlo Simulation

Channel parameters in `mc_simulation.py` trace to the sources listed here.
The paper (Commercial Real Estate: Vacancy Doom Loop) is available on SSRN and contains the full
reference list and §4 calibration narrative.

---

## Channel Sources

### `C1_banking_fragility`

Extend-and-pretend capital destruction, unrealized CRE losses. $929B commercial mortgage exposure at FDIC-insured banks. 44% office vacancy in some CBDs. Sources: FDIC, Trepp CMBS data, Fed Financial Stability.

*Full citations: paper §4 (available SSRN).*

### `C2_municipal_fiscal_erosion`

Urban doom loop: CRE devaluation erodes property tax base, forcing service cuts or tax increases on remaining residents. NYC $1B+ annual revenue gap. Sources: Municipal bond analyses, city budget documents.

*Full citations: paper §4 (available SSRN).*

### `C3_pension_wealth_destruction`

Public pension CRE allocations marked at stale valuations. CalPERS, NYSTRS, etc. overallocated to CRE. Beneficiary wealth destruction from unrealized losses. Sources: pension annual reports, Preqin.

*Full citations: paper §4 (available SSRN).*

### `C4_service_worker_displacement`

Commuter spending collapse ($12.4B NYC alone). Net welfare loss after suburban offset (λ=0.3-0.4). Uncompensated job loss in CBD service sector. Sources: NYC Comptroller, Bloomberg CBD data.

*Full citations: paper §4 (available SSRN).*

### `C5_transit_fiscal_collapse`

Farebox revenue collapse from remote work. MTA, BART, WMATA all facing structural deficits. Federal COVID relief expiring. Sources: transit agency financials, FTA.

*Full citations: paper §4 (available SSRN).*

### `C6_regulatory_capture_lobbying`

1031 exchange ($10.2B/yr tax expenditure), REIT pass-through, lobbying ($140M+/yr from NAR, ABA, etc.) sustaining extend-and-pretend. Sources: JCT, OpenSecrets, Real Estate Roundtable.

*Full citations: paper §4 (available SSRN).*

---

## Industry Revenue (Π)

The private payoff Π = $13.0B/yr is global annual industry revenue.
Source: paper §2 and §4. See paper §DA-1 (Decision Audit Field 7) for full
revenue source documentation.

---

## SAPM Framework

- Postnieks, E. (2026). *The Private Pareto Theorem*. SAPM Foundation Paper. SSRN.
- Postnieks, E. (2026). *Commercial Real Estate (Vacancy Doom Loop)*. SAPM Working Paper. SSRN.

---

## Distribution Methodology

- Iman, R. L., & Conover, W. J. (1982). A distribution-free approach to
  inducing rank correlation among input variables. *Communications in
  Statistics — Simulation and Computation*, 11(3), 311–334.
- Cooke, R. M. (1991). *Experts in Uncertainty*. Oxford University Press.
