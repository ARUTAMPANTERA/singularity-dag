# ===================================================================================
# PASSO 1: ENTRA NELLA CARTELLA DEL REPOSITORY
# ===================================================================================
cd ~/storage/shared/SingularityDAG

# ===================================================================================
# PASSO 2: CREA TUTTE LE CARTELLE MANCANTI
# ===================================================================================
mkdir -p languages/aru2
mkdir -p docs
mkdir -p kernel
mkdir -p versions
mkdir -p archive/appunti
mkdir -p archive/sperimentali

# ===================================================================================
# PASSO 3: BACKUP DEL VECCHIO README E SOSTITUZIONE CON QUELLO NUOVO
# ===================================================================================
cp README.md archive/README_vecchio_backup.md
cp "README_SINGULARITY_OS_v70_1_AETERNUM.md" README.md
mv "README_SINGULARITY_OS_v70_1_AETERNUM.md" docs/

# ===================================================================================
# PASSO 4: SPOSTA TUTTI I MANUALI .md IN docs/
# ===================================================================================
mv "MANUALE_UFFICIALE_v70.1_AETERNUM.md" docs/
mv "MANUALE_IA_ECOSYSTEM_v70.1.md" docs/
mv "linguaggi.md" docs/
mv "migliorie.md" docs/
mv "COMANDI TERMUX — SINGULARITY_OSmanuale battito.md" docs/MANUALE_TERMUX.md
mv "manuale dag.md" docs/MANUALE_DAG.md

# ===================================================================================
# PASSO 5: SPOSTA ARUTAM_SCRIPT SPEC E ALTRI FILE LINGUAGGIO
# ===================================================================================
mv aru2_spec.md languages/aru2/
mv "CLAUDE_TEMÙ_ESSENCE_v70_0.aru.md" languages/aru2/CLAUDE_TEMU_ESSENCE.md
mv "ARUTAM SCRIPTaistudio.md" archive/sperimentali/ARUTAM_SCRIPT_AI_STUDIO_old.md

# ===================================================================================
# PASSO 6: SPOSTA LANGDON PROTOCOL .md IN kernel/
# ===================================================================================
mv "LANGDON_REVERSE_PROTOCOL_v1.1.md" kernel/

# ===================================================================================
# PASSO 7: SPOSTA VERSIONI VECCHIE (v52) IN versions/
# ===================================================================================
mv v52.0_SPEC.md versions/
mv v52.0_TESTPLAN.md versions/

# ===================================================================================
# PASSO 8: SPOSTA VECCHIO MANUALE.md IN archive/
# ===================================================================================
mv MANUALE.md archive/vecchio_manuale.md

# ===================================================================================
# PASSO 9: SPOSTA APPUNTI E MESSAGGI VARI IN archive/appunti/
# ===================================================================================
mv "deenseek.md" archive/appunti/deepseek_note.md
mv "ultimo qwen attestazione.md" archive/appunti/
mv "X CLAUDE ULTIMOMessaggio.md" archive/appunti/
mv "last messaggio.md" archive/appunti/
mv "proposta 712.md" archive/appunti/
mv "proposta espansione.md.txt" archive/appunti/
mv "messaggio x Claude.md.txt" archive/appunti/
mv "lista comandi termux.md" archive/appunti/

# ===================================================================================
# PASSO 10: PULISCI LA CARTELLA artifacts/ (SOLO JSON DEVONO RESTARE)
# ===================================================================================
cd artifacts
mv "proposta 712.md" ../archive/appunti/ 2>/dev/null
mv "last messaggio.md" ../archive/appunti/ 2>/dev/null
mv "proposta espansione.md.txt" ../archive/appunti/ 2>/dev/null
mv "messaggio x Claude.md.txt" ../archive/appunti/ 2>/dev/null
mv "lista comandi termux.md" ../archive/appunti/ 2>/dev/null
cd ..

# ===================================================================================
# PASSO 11: VERIFICA CHE TUTTO SIA A POSTO
# ===================================================================================
echo "=== ROOT ==="
ls -1
echo ""
echo "=== artifacts/ ==="
ls -1 artifacts/
echo ""
echo "=== kernel/ ==="
ls -1 kernel/
echo ""
echo "=== languages/aru2/ ==="
ls -1 languages/aru2/
echo ""
echo "=== docs/ ==="
ls -1 docs/
echo ""
echo "=== versions/ ==="
ls -1 versions/
echo ""
echo "=== archive/ ==="
ls -1 archive/

# ===================================================================================
# PASSO 12: AGGIUNGI TUTTO, COMMITTA E PUSH
# ===================================================================================
git add -A
git commit -m "Ristrutturazione completa repository: pulizia root, organizzazione cartelle, aggiornato README"
git push origin main

# ===================================================================================
# PASSO 13: RIAVVIA IL BATTITO CARDIACO
# ===================================================================================
~/dag_sync.sh &
echo "Battito cardiaco riavviato."
ps aux | grep dag_sync

# ==============================================================================
# SINTESI FINALE
# ==============================================================================
riepilogo:
  root: README.md, MANIFEST.json
  artifacts: SOLO file JSON + cartella reports
  kernel: kernel AETERNUM + LANGDON
  languages/aru2: aru2_spec.md, CLAUDE_TEMU_ESSENCE.md (+ validator e examples se già generati)
  docs: tutti i manuali ufficiali e guide
  versions: v52 storico
  archive: appunti, vecchi manuali, proposte, versioni sperimentali