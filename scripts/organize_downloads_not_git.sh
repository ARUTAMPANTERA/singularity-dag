#!/data/data/com.termux/files/usr/bin/bash

echo "═══════════════════════════════════════════════════════════════"
echo "🜁 ORGANIZZAZIONE FILE — LAVORO (NO GIT REPO)"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Configurazione
DOWNLOADS="$HOME/storage/downloads"
REPO="$HOME/.../shared/SingularityDAG"
WORK_DIR="$HOME/Markor/Singularity"
AISTUDIO_DIR="$DOWNLOADS/AIStudio"

# Crea cartelle lavoro (NON nel repo)
mkdir -p "$WORK_DIR/working"
mkdir -p "$WORK_DIR/archive"
mkdir -p "$AISTUDIO_DIR"
mkdir -p "$AISTUDIO_DIR/organized"
mkdir -p "$AISTUDIO_DIR/to_review"

echo "✅ Cartelle lavoro create:"
echo "   $WORK_DIR/working/"
echo "   $WORK_DIR/archive/"
echo "   $AISTUDIO_DIR/"
echo ""

# Contatori
MOVED=0
KEPT_IN_REPO=0
ERRORS=0

# Scansiona Downloads per file AI Studio
echo "🔍 Scansione Downloads per file AI Studio..."
echo ""

for file in "$DOWNLOADS"/aistudio* "$DOWNLOADS"/*.yaml "$DOWNLOADS"/*.md "$DOWNLOADS"/*.txt "$DOWNLOADS"/*.aru "$DOWNLOADS"/*.aru3 2>/dev/null; do
    if [ -f "$file" ]; then
        BASENAME=$(basename "$file")
        
        # Salta se già nel repo
        if echo "$file" | grep -q "SingularityDAG"; then
            continue
        fi
        
        echo "   📄 Analizzo: $BASENAME"
        
        # Estrai nome dal contenuto
        CONTENT=$(head -30 "$file" 2>/dev/null)
        
        # Determina se è production o lavoro
        if echo "$CONTENT" | grep -qi "EPISTEMIC_SYSTEM_UNIFIED.*FINAL\|PRODUCTION_READY\|GUARDIANO.*SIGNOFF"; then
            # FILE PRODUCTION → va nel repo
            DEST="$REPO/kernel"
            echo "      ✅ PRODUCTION → Repo Git ($DEST)"
            mv "$file" "$DEST/" 2>/dev/null
            ((KEPT_IN_REPO++))
        else
            # FILE LAVORO → va in Downloads/AIStudio
            DEST="$AISTUDIO_DIR/to_review"
            echo "      📝 LAVORO → $DEST"
            mv "$file" "$DEST/" 2>/dev/null
            ((MOVED++))
        fi
    fi
done

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "🜁 RIEPILOGO"
echo "═══════════════════════════════════════════════════════════════"
echo "File produzione (repo Git): $KEPT_IN_REPO"
echo "File lavoro (no Git): $MOVED"
echo "Errori: $ERRORS"
echo ""
echo "📂 STRUTTURA:"
echo "   REPO: $REPO/kernel/"
echo "   LAVORO: $AISTUDIO_DIR/to_review/"
echo "   ARCHIVIO: $WORK_DIR/archive/"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo "✅ ORGANIZZAZIONE COMPLETATA"
    exit 0
else
    echo "⚠️  Alcuni file richiedono attenzione"
    exit 1
fi
