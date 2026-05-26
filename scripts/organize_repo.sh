#!/data/data/com.termux/files/usr/bin/bash

echo "🜁 Organizing EPISTEMIC_SYSTEM_UNIFIED v1.0 Repository..."

# ─── FASE 1: CREA CARTELLE MANCANTI ───
mkdir -p tests examples/sandbox_examples examples/factoid_examples .github/workflows
echo "✅ Cartelle create"

# ─── FASE 2: ELIMINA FILE VUOTI ───
rm -f kernel/dhdj.md kernel/hh.md
echo "✅ File vuoti eliminati"

# ─── FASE 3: ARCHIVIA VERSIONI VECCHIE ───
mv kernel/SINGULARITY_OS.aru archive/ 2>/dev/null
mv kernel/SINGULARITY_OS_COPILOT_FUSION.aru3.txt archive/ 2>/dev/null
mv kernel/v70.3_HYBRID_MAX_EXPANSION.md archive/ 2>/dev/null
mv kernel/LANGDON_REVERSE_PROTOCOL_v1.1.md archive/ 2>/dev/null
echo "✅ Versioni vecchie archiviate"

# ─── FASE 4: RISOLVI DUPLICATI ───
mv kernel/mappinglocks.yaml archive/ 2>/dev/null
mv kernel/guardianoauditreport_template.yaml docs/ 2>/dev/null
echo "✅ Duplicati risolti"

# ─── FASE 5: CORREGGI ESTENSIONI FILE ───
mv "kernel/EPISTEMIC_SYSTEM_UNIFIED_v1_0_FINAL.yaml.md" kernel/EPISTEMIC_SYSTEM_UNIFIED_v1_0_FINAL.yaml 2>/dev/null
echo "✅ Estensioni corrette"

# ─── FASE 6: CREA FILE MANCANTI ───
cat > tests/test_cases.yaml << 'EOF'
test_cases:
  - id: TC01_lookup_rete_eter
    priority: HIGH
  - id: TC02_factoid_ingestion
    priority: HIGH
  - id: TC03_node_controverso_reich
    priority: HIGH
  - id: TC04_code_sandbox
    priority: MEDIUM
  - id: TC05_majorana_theta
    priority: HIGH
EOF

cat > tests/engines_test.py << 'EOF'
import sys
sys.path.append('../tools')
from nd_v9 import nd_v9
from uq_v6 import uq_v6
print("✅ Engine tests ready")
EOF

echo "✅ File mancanti creati"

# ─── FASE 7: VERIFICA STRUTTURA ───
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "🜁 STRUTTURA FINALE"
echo "═══════════════════════════════════════════════════════════════"
find . -maxdepth 3 -type f \( -name "*.yaml" -o -name "*.py" -o -name "*.md" \) | grep -v ".git" | grep -v "archive" | sort

# ─── FASE 8: GIT ADD + COMMIT ───
echo ""
echo "🜁 Git add..."
git add .

echo ""
echo "🜁 Git status..."
git status

echo ""
echo "✅ Repository organizzato! Pronto per commit."
