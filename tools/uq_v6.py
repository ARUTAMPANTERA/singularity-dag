# tools/uq_v6.py
# UQ_v6 minimal reference implementation for testing and examples.
# Output: UQ ∈ [0.0, 1.0]

def tier_weight(tier):
    return {"TIER_0": 1.0, "TIER_1": 0.8, "TIER_2": 0.5, "TIER_3": 0.2}.get(tier, 0.2)

def compute_conflict_penalty(conflict_set):
    if not conflict_set:
        return 0.0
    size = conflict_set.get("size", 1)
    contradiction = conflict_set.get("contradiction_score", 0.0)
    penalty = min(1.0, contradiction * (1 + (size - 1) * 0.25))
    return penalty

def compute_bias_penalty(bias_signals):
    if not bias_signals:
        return 0.0
    vals = [v for v in bias_signals.values()]
    return min(1.0, sum(vals) / max(1, len(vals)))

def uq_v6(sources, conflict_set=None, bias_signals=None):
    if not sources:
        return 0.0
    weights = []
    for s in sources:
        tier = s.get("tier", "TIER_3")
        strength = float(s.get("evidence_strength", 1.0))
        weights.append(tier_weight(tier) * strength)
    max_support = float(len(sources)) or 1.0
    s_support = sum(weights) / max_support
    conflict_penalty = compute_conflict_penalty(conflict_set)
    bias_penalty = compute_bias_penalty(bias_signals)
    uq_raw = s_support * (1 - conflict_penalty) * (1 - bias_penalty)
    uq = max(0.0, min(1.0, uq_raw))
    return round(uq, 3)

if __name__ == "__main__":
    sources1 = [
        {"tier": "TIER_0", "evidence_strength": 1.0},
        {"tier": "TIER_1", "evidence_strength": 0.8}
    ]
    print("Example 1 UQ:", uq_v6(sources1, conflict_set=None, bias_signals=None))
    sources2 = [
        {"tier": "TIER_2", "evidence_strength": 0.4},
        {"tier": "TIER_3", "evidence_strength": 0.3}
    ]
    conflict = {"size": 2, "contradiction_score": 0.6}
    bias = {"source_homogeneity": 0.2}
    print("Example 2 UQ:", uq_v6(sources2, conflict_set=conflict, bias_signals=bias))