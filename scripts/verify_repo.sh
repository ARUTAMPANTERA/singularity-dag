#!/data/data/com.termux/files/usr/bin/bash

echo "═══════════════════════════════════════════════════════════════"
echo "🜁 EPISTEMIC_SYSTEM_UNIFIED v1.0 — VERIFICA COMPLETA"
echo "═══════════════════════════════════════════════════════════════"
echo ""

ERRORS=0
WARNINGS=0

# 1. VERIFICA CARTELLE
echo "📁 1. VERIFICA CARTELLE..."
for dir in kernel docs tools tests examples .github/workflows archive; do
    if [ -d "$dir" ]; then
        echo "   ✅ $dir/"
    else
        echo "   ❌ $dir/ MANCANTE"
        ERRORS=$((ERRORS + 1))
    fi
done
echo ""

# 2. VERIFICA KERNEL
echo "📄 2. VERIFICA KERNEL..."
if [ -f "kernel/EPISTEMIC_SYSTEM_UNIFIED_v1_0_FINAL.yaml" ]; then
    echo "   ✅ EPISTEMIC_SYSTEM_UNIFIED_v1_0_FINAL.yaml"
    SIZE=$(wc -c < "kernel/EPISTEMIC_SYSTEM_UNIFIED_v1_0_FINAL.yaml")
    echo "      Dimensione: $SIZE byte"
else
    echo "   ❌ EPISTEMIC_SYSTEM_UNIFIED_v1_0_FINAL.yaml MANCANTE"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 3. VERIFICA DOCUMENTAZIONE
echo "📚 3. VERIFICA DOCUMENTAZIONE..."
if [ -f "docs/guardianoauditreport_template.yaml" ]; then
    echo "   ✅ docs/guardianoauditreport_template.yaml"
else
    echo "   ❌ docs/guardianoauditreport_template.yaml MANCANTE"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 4. VERIFICA TOOLS PYTHONecho "🔧 4. VERIFICA TOOLS PYTHON..."
if [ -f "tools/nd_v9.py" ]; then
    echo "   ✅ tools/nd_v9.py"
    python -m py_compile "tools/nd_v9.py" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "      ✅ Sintassi Python valida"
    else
        echo "      ❌ Errore sintassi Python"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "   ❌ tools/nd_v9.py MANCANTE"
    ERRORS=$((ERRORS + 1))
fi

if [ -f "tools/uq_v6.py" ]; then
    echo "   ✅ tools/uq_v6.py"
    python -m py_compile "tools/uq_v6.py" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "      ✅ Sintassi Python valida"
    else
        echo "      ❌ Errore sintassi Python"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "   ❌ tools/uq_v6.py MANCANTE"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 5. VERIFICA TESTS
echo "🧪 5. VERIFICA TESTS..."
if [ -f "tests/test_cases.yaml" ]; then
    echo "   ✅ tests/test_cases.yaml"
else
    echo "   ❌ tests/test_cases.yaml MANCANTE"
    ERRORS=$((ERRORS + 1))
fi

if [ -f "tests/engines_test.py" ]; then
    echo "   ✅ tests/engines_test.py"
else
    echo "   ❌ tests/engines_test.py MANCANTE"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 6. CONTEGGIO FILE
echo "📊 6. CONTEGGIO FILE..."
TOTAL=$(find . -type f 2>/dev/null | grep -v ".git" | wc -l)YAML=$(find . -name "*.yaml" 2>/dev/null | grep -v ".git" | wc -l)
PY=$(find . -name "*.py" 2>/dev/null | grep -v ".git" | wc -l)
MD=$(find . -name "*.md" 2>/dev/null | grep -v ".git" | wc -l)
echo "   Totale: $TOTAL"
echo "   YAML: $YAML"
echo "   Python: $PY"
echo "   Markdown: $MD"
echo ""

# 7. RIEPILOGO
echo "═══════════════════════════════════════════════════════════════"
echo "🜁 RIEPILOGO"
echo "═══════════════════════════════════════════════════════════════"
echo "ERRORI: $ERRORS"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo "✅ VERIFICA PASSATA — Repository pronto"
    exit 0
else
    echo "❌ VERIFICA FALLITA — Correggi $ERRORS errori"
    exit 1
fi
