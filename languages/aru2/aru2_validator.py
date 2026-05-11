#!/usr/bin/env python3
# ==============================================================================
# ARUTAM_SCRIPT v2.0 VALIDATOR (.aru2) — SINGULARITY_OS v70.2
# ==============================================================================
import re
import sys

def validate_aru2(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    errors = []
    warnings = []

    required_directives = ['@kernel', '@lock_group', '@validate_pre', '@validate_post']
    for d in required_directives:
        if d not in content:
            errors.append(f"DIRETTIVA MANCANTE: {d} — richiesta per v70.2")

    lock_group_pattern = r'@lock_group\((\w+),\s*(\d+),\s*inherit=(\w+)\)'
    for match in re.finditer(lock_group_pattern, content):
        name, count, tier = match.groups()
        if tier not in ['T1','T2','T3','T4','T5','T6']:
            errors.append(f"TIER INVALIDO per {name}: {tier} (accettati: T1-T6)")

    if '@validate_pre(GOV_L21, checklist=40)' not in content:
        errors.append("Manca @validate_pre(GOV_L21, checklist=40)")

    if '/evolve' in content:
        errors.append("Comando /evolve non consentito in v70.2")

    if '@embedding_bridge' in content and '@if(@host.embedding_available' not in content:
        errors.append("@embedding_bridge non è in conditional loading (@if)")

    print(f"=== VALIDAZIONE {filepath} ===")
    if errors:
        for e in errors:
            print(f"  ❌ {e}")
    if warnings:
        for w in warnings:
            print(f"  ⚠️ {w}")
    if not errors and not warnings:
        print("✅ File .aru2 valido per v70.2.")

    return len(errors) == 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 aru2_validator.py <file.aru2>")
        sys.exit(1)
    success = validate_aru2(sys.argv[1])
    sys.exit(0 if success else 1)
