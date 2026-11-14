"""County pathway twin: a local-level state-space estimator per (signal, county), run causally.
State x_t = latent level on a transformed scale (logit for shares, log for ratios); random walk with variance q per month.
Observation variance r_t comes from the counts (binomial / Poisson delta method), so small counties get wide intervals by construction."""
import numpy as np
Q_GRID = np.array([0.0005, 0.002, 0.008, 0.03, 0.1, 0.3])   # per month, transformed scale
PHI_GRID = np.array([1.0, 3.0, 10.0, 30.0])                 # overdispersion of observation noise relative to pure counting noise
# Structure note (rule 10): with counting noise alone, q ran to its upper bound on queue signals. Queue snapshots are not
# independent draws, so the structure was changed (overdispersion phi added) rather than widening the q bounds.
PARAMS = [(q, phi) for q in Q_GRID for phi in PHI_GRID]

def transform(kind, num, den, den_count=None):
    if kind == "share":
        p = (num + 0.5) / (den + 1.0)
        return np.log(p / (1 - p)), 1.0 / (num + 0.5) + 1.0 / (den - num + 0.5)
    if kind == "ratio":
        dc = den if den_count is None or np.isnan(den_count) else den_count
        return np.log(max(num, 0.5) / den), 1.0 / max(num, 0.5) + 1.0 / max(dc, 0.5)
    if kind == "pct":   # annual published percentage without denominators: assume sd of 1 percentage point (qc assumption)
        p = min(max(num / 100.0, 0.005), 0.995)
        return np.log(p / (1 - p)), (0.01 / (p * (1 - p))) ** 2
    raise ValueError(kind)

def inverse(kind, x):
    x = np.asarray(x, float)
    if kind in ("share", "pct"): return 1 / (1 + np.exp(-x))
    return np.exp(x)

def kfilter(tm, y, r, q):
    """tm: time in months (float, increasing). Returns dict of arrays: prior mean/var, post mean/var, loglik per obs."""
    n = len(y); m0 = np.empty(n); P0 = np.empty(n); m = np.empty(n); P = np.empty(n); ll = np.empty(n)
    mm, PP = y[0], 4.0  # diffuse-ish start centred on first obs
    for i in range(n):
        if i > 0: PP = PP + q * max(tm[i] - tm[i - 1], 0.0)
        m0[i], P0[i] = mm, PP
        S = PP + r[i]; K = PP / S; e = y[i] - mm
        ll[i] = -0.5 * (np.log(2 * np.pi * S) + e * e / S)
        mm = mm + K * e; PP = (1 - K) * PP
        m[i], P[i] = mm, PP
    ll[0] = 0.0
    return dict(m0=m0, P0=P0, m=m, P=P, ll=ll)

def smooth(tm, f, q):
    n = len(f["m"]); ms = f["m"].copy(); Ps = f["P"].copy()
    for i in range(n - 2, -1, -1):
        Pp = f["P"][i] + q * max(tm[i + 1] - tm[i], 0.0)
        C = f["P"][i] / Pp
        ms[i] = f["m"][i] + C * (ms[i + 1] - f["m"][i])
        Ps[i] = f["P"][i] + C * C * (Ps[i + 1] - Pp)
    return ms, Ps
