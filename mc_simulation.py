#!/usr/bin/env python3
"""
SAPM Monte Carlo Simulation — Commercial Real Estate / Vacancy Doom Loop
==========================================

Reproduces all quantitative results in:

  Postnieks, E. (2026). SAPM Working Paper: Commercial Real Estate (Vacancy Doom Loop).
  Available: SSRN.

This script is self-contained. Dependencies: numpy, scipy only.
Seeded at seed=42 — produces bit-identical results on any machine
with numpy>=1.24, scipy>=1.10.

Usage
-----
  pip install numpy scipy
  python mc_simulation.py

Theory
------
β_W = ΔW / Π  where:
  Π  = annual industry revenue ($B/yr) — never profit
  ΔW = total annualized welfare destruction ($B/yr)
     = Σ_i W_i across all channels, sampled with correlation ρ=0.3

Classification: Class 2 — Intractability
"""

import json
import numpy as np
from pathlib import Path
from scipy import stats

CONFIG = {
    "paper_id": "cre",
    "domain_name": "Commercial Real Estate",
    "theorem": "Vacancy Doom Loop",
    "classification": "Class 2 \u2014 Intractability",
    "seed": 42,
    "n_draws": 100000,
    "correlation_rho": 0.3,
    "private_payoff_B": 13.0,
    "channels": {
        "C1_banking_fragility": {
            "dist": "lognormal",
            "low": 16.0,
            "mid": 24.0,
            "high": 32.0,
            "weight": 0.24,
            "description": "Extend-and-pretend capital destruction, unrealized CRE losses. $929B commercial mortgage exposure at FDIC-insured banks. 44% office vacancy in some CBDs. Sources: FDIC, Trepp CMBS data, Fed Financial Stability."
        },
        "C2_municipal_fiscal_erosion": {
            "dist": "lognormal",
            "low": 5.0,
            "mid": 7.5,
            "high": 10.0,
            "weight": 0.075,
            "description": "Urban doom loop: CRE devaluation erodes property tax base, forcing service cuts or tax increases on remaining residents. NYC $1B+ annual revenue gap. Sources: Municipal bond analyses, city budget documents."
        },
        "C3_pension_wealth_destruction": {
            "dist": "lognormal",
            "low": 23.0,
            "mid": 32.0,
            "high": 41.0,
            "weight": 0.32,
            "description": "Public pension CRE allocations marked at stale valuations. CalPERS, NYSTRS, etc. overallocated to CRE. Beneficiary wealth destruction from unrealized losses. Sources: pension annual reports, Preqin."
        },
        "C4_service_worker_displacement": {
            "dist": "lognormal",
            "low": 12.0,
            "mid": 18.5,
            "high": 25.0,
            "weight": 0.185,
            "description": "Commuter spending collapse ($12.4B NYC alone). Net welfare loss after suburban offset (\u03bb=0.3-0.4). Uncompensated job loss in CBD service sector. Sources: NYC Comptroller, Bloomberg CBD data."
        },
        "C5_transit_fiscal_collapse": {
            "dist": "lognormal",
            "low": 4.0,
            "mid": 6.0,
            "high": 8.0,
            "weight": 0.06,
            "description": "Farebox revenue collapse from remote work. MTA, BART, WMATA all facing structural deficits. Federal COVID relief expiring. Sources: transit agency financials, FTA."
        },
        "C6_regulatory_capture_lobbying": {
            "dist": "lognormal",
            "low": 10.0,
            "mid": 12.5,
            "high": 15.0,
            "weight": 0.12,
            "description": "1031 exchange ($10.2B/yr tax expenditure), REIT pass-through, lobbying ($140M+/yr from NAR, ABA, etc.) sustaining extend-and-pretend. Sources: JCT, OpenSecrets, Real Estate Roundtable."
        }
    },
    "impossibility_floor": 4.7
}

# ─────────────────────────────────────────────────────────────────────────────
# SIMULATION ENGINE (identical across all SAPM domains)
# ─────────────────────────────────────────────────────────────────────────────

def generate_correlated_draws(config, rng):
    channels = config["channels"]
    n_draws  = config["n_draws"]
    rho      = config["correlation_rho"]
    n_ch     = len(channels)
    corr     = np.full((n_ch, n_ch), rho)
    np.fill_diagonal(corr, 1.0)
    L        = np.linalg.cholesky(corr)
    Z        = rng.standard_normal((n_draws, n_ch))
    Z_corr   = Z @ L.T
    draws    = np.zeros((n_draws, n_ch))
    names    = list(channels.keys())
    for i, (name, p) in enumerate(channels.items()):
        U    = stats.norm.cdf(Z_corr[:, i])
        dist, low, mid, high = p["dist"], p["low"], p["mid"], p["high"]
        if dist == "lognormal":
            sigma = np.log(high / mid) / 1.645
            draws[:, i] = stats.lognorm.ppf(U, s=sigma, scale=mid)
        elif dist == "normal":
            sigma = (high - low) / (2 * 1.645)
            draws[:, i] = stats.norm.ppf(U, loc=mid, scale=sigma)
        elif dist == "triangular":
            c = (mid - low) / (high - low)
            draws[:, i] = stats.triang.ppf(U, c, loc=low, scale=high - low)
        else:
            raise ValueError(f"Unknown distribution: {dist}")
    return draws, names


def build_sensitivity_matrix(config):
    channels = config["channels"]
    names    = list(channels.keys())
    mids     = [channels[n]["mid"] for n in names]
    vsl_idx  = mids.index(max(mids))
    pi       = config["private_payoff_B"]
    matrix   = []
    for vm in [0.5, 0.75, 1.0, 1.25, 1.5]:
        row = {"vsl_multiplier": vm, "values": {}}
        for dc in [0.0, 0.10, 0.20, 0.30, 0.40]:
            total = sum(mids[i] * (vm if i == vsl_idx else 1.0) for i in range(len(names)))
            row["values"][f"dc_{int(dc*100)}pct"] = round(total * (1 - dc) / pi, 2)
        matrix.append(row)
    return matrix


def build_histogram(beta_draws, n_bins=80):
    counts, edges = np.histogram(beta_draws, bins=n_bins)
    return [
        {"bin_low": round(float(edges[i]),3), "bin_high": round(float(edges[i+1]),3),
          "bin_mid": round(float((edges[i]+edges[i+1])/2),3),
          "count": int(counts[i]), "density": round(float(counts[i]/len(beta_draws)),6)}
        for i in range(len(counts))
    ]


def run():
    cfg = CONFIG
    rng = np.random.default_rng(seed=cfg["seed"])
    print(f"SAPM Monte Carlo — {cfg['domain_name']} ({cfg['theorem']})")
    print(f"  N={cfg['n_draws']:,}  seed={cfg['seed']}  ρ={cfg['correlation_rho']}  Π=${cfg['private_payoff_B']:,}B")
    draws, names = generate_correlated_draws(cfg, rng)
    total       = np.sum(draws, axis=1)
    beta        = total / cfg["private_payoff_B"]
    p5, p95     = np.percentile(beta, [5, 95])
    p1, p99     = np.percentile(beta, [1, 99])
    pi_sa       = total - cfg["private_payoff_B"]
    floor       = cfg.get("impossibility_floor")
    p_floor     = float(np.mean(beta < floor)) if floor else None
    ch_stats    = {
        n: {"median": round(float(np.median(draws[:,i])),1),
             "mean":   round(float(np.mean(draws[:,i])),1),
             "p5":     round(float(np.percentile(draws[:,i],5)),1),
             "p95":    round(float(np.percentile(draws[:,i],95)),1),
             "std":    round(float(np.std(draws[:,i])),1)}
        for i, n in enumerate(names)
    }
    results = {
        "paper_id": cfg["paper_id"],
        "domain_name": cfg["domain_name"],
        "theorem": cfg["theorem"],
        "classification": cfg["classification"],
        "seed": cfg["seed"], "n_draws": cfg["n_draws"],
        "n_channels": len(cfg["channels"]),
        "correlation_rho": cfg["correlation_rho"],
        "private_payoff_B": cfg["private_payoff_B"],
        "beta_w": {
            "median": round(float(np.median(beta)),2),
            "mean":   round(float(np.mean(beta)),2),
            "std":    round(float(np.std(beta)),2),
            "p1":  round(float(p1),2), "p5":  round(float(p5),2),
            "p95": round(float(p95),2), "p99": round(float(p99),2),
            "ci_90": [round(float(p5),1), round(float(p95),1)],
            "ci_99": [round(float(p1),1), round(float(p99),1)],
            "p_below_1": round(float(np.mean(beta < 1.0)),6),
            "p_below_1_pct": f"{np.mean(beta < 1.0)*100:.4f}%",
        },
        "impossibility_floor": {
            "floor_value": floor,
            "p_below_floor": round(p_floor,6) if p_floor is not None else None,
            "p_below_floor_pct": f"{p_floor*100:.4f}%" if p_floor is not None else None,
        } if floor else None,
        "welfare_cost": {
            "total_median_B": round(float(np.median(total)),1),
            "total_mean_B":   round(float(np.mean(total)),1),
            "total_p5_B":     round(float(np.percentile(total,5)),1),
            "total_p95_B":    round(float(np.percentile(total,95)),1),
        },
        "pi_sa": {
            "median_B": round(float(np.median(pi_sa)),1),
            "mean_B":   round(float(np.mean(pi_sa)),1),
            "p5_B":     round(float(np.percentile(pi_sa,5)),1),
            "p95_B":    round(float(np.percentile(pi_sa,95)),1),
        },
        "channel_statistics": ch_stats,
        "sensitivity_matrix": build_sensitivity_matrix(cfg),
    }
    bw = results["beta_w"]
    wc = results["welfare_cost"]
    print(f"  β_W median : {bw['median']}")
    print(f"  90% CI     : {bw['ci_90']}")
    print(f"  P(β_W < 1) : {bw['p_below_1_pct']}")
    print(f"  ΔW median  : ${wc['total_median_B']:,.1f}B/yr")
    return results


if __name__ == "__main__":
    results = run()
    out = Path(__file__).parent / "mc_results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"  Wrote: {out}")
    rng2 = np.random.default_rng(seed=CONFIG["seed"])
    d2, _ = generate_correlated_draws(CONFIG, rng2)
    t2    = np.sum(d2, axis=1)
    b2    = t2 / CONFIG["private_payoff_B"]
    hist  = build_histogram(b2)
    hout  = Path(__file__).parent / "mc_histogram.json"
    hout.write_text(json.dumps(hist, indent=2), encoding="utf-8")
    print(f"  Wrote: {hout}")
    bw = results["beta_w"]
    print(f"\nVerify: beta_w.median = {bw['median']}  ci_90 = {bw['ci_90']}")
