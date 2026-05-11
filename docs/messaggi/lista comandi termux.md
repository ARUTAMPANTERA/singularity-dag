Ecco la lista completa dei comandi Termux per gestire l'intero sistema SINGULARITY_OS, il battito cardiaco e le sessioni.

---

📋 COMANDI TERMUX — SINGULARITY_OS (v71.0+)

🫀 Battito cardiaco (DAG Sync)

Comando Descrizione
~/dag_sync.sh & Avvia il battito cardiaco in background.
ps aux \| grep dag_sync Verifica se il battito è in esecuzione.
pkill -f dag_sync.sh Ferma il battito cardiaco normalmente.
pkill -9 -f dag_sync.sh Ferma il battito forzatamente.
tail -20 ~/dag_sync.log Mostra gli ultimi 20 log del battito.
cat ~/dag_sync.log Mostra l'intero file di log.
nano ~/dag_sync.sh Modifica lo script del battito.
chmod +x ~/dag_sync.sh Rende eseguibile lo script dopo una modifica.

📂 Navigazione e stato repository

Comando Descrizione
cd ~/storage/shared/SingularityDAG Vai alla cartella del DAG.
ls Elenca file e cartelle.
ls -a Elenca anche i file nascosti (es. .github).
git status Mostra lo stato del repository (modifiche, nuovi file).
git log --oneline -10 Mostra gli ultimi 10 commit.
git diff Mostra le differenze non ancora committate.
git branch Mostra il branch corrente.
df -h Mostra lo spazio libero sul dispositivo.

📤 Sincronizzazione con GitHub

Comando Descrizione
git add -A Aggiunge tutte le modifiche (nuovi file, cancellazioni).
git add nome_file Aggiunge un file specifico.
git commit -m "messaggio" Crea un commit con un messaggio descrittivo.
git push origin main Spinge i commit sul repository remoto.
git pull origin main --no-rebase Scarica e unisce le modifiche remote senza rebase.
git checkout --theirs nome_file In caso di conflitto, accetta la versione remota del file.
rm -f .git/index.lock Rimuove il file di lock se Git si blocca.
git reset --hard origin/main Attenzione! Resetta il repository allo stato remoto, cancellando modifiche locali.

🛡️ Validazione artefatti

Comando Descrizione
python3 scripts/validate_artifact.py artifacts/NOME.json --output artifacts/reports/NOME_REPORT.json Valida un singolo artefatto e genera il report in artifacts/reports/.
for f in artifacts/*.json; do python3 scripts/validate_artifact.py "$f" --output "artifacts/reports/$(basename $f .json)_REPORT.json"; done Valida tutti gli artefatti e genera i report.
for f in artifacts/*.json; do python3 scripts/validate_artifact.py "$f" 2>/dev/null; if [ $? -eq 5 ]; then mv "$f" archive/; fi; done Sposta automaticamente in archive/ gli artefatti che falliscono la validazione.

📥 Creazione file rapidi (senza editor)

Comando Descrizione
cat > artifacts/NUOVO.json << 'EOF' ... EOF Crea un file JSON incollando il contenuto tra EOF.
echo '{"test": true}' > test.json Crea un file con contenuto semplice.
mv vecchio_nome.json nuovo_nome.json Rinomina o sposta un file.
rm nome_file.json Elimina un file.
mkdir -p nuova/cartella Crea una cartella e tutte le cartelle intermedie.

💾 Snapshot e sessioni LLM

Comando / Azione Descrizione
Crea snapshot Copia il contenuto del file docs/MANUALE_TERMUX.md, sezione 4, e incollalo come primo messaggio in una nuova chat con un LLM.
Riprendi sessione Invia /context_sync e /dag_list nella chat per allineare il nodo al DAG.

🔧 Manutenzione e installazione

Comando Descrizione
pkg update && pkg upgrade -y Aggiorna tutti i pacchetti di Termux.
pkg install python -y Installa Python.
pkg install git -y Installa Git.
pkg install jq inotify-tools -y Installa strumenti per JSON e monitoraggio file.
pkg install nano -y Installa l'editor di testo Nano.
pkg install termux-api -y Installa l'API di Termux (necessaria per termux-boot).

⚡ Avvio automatico

Comando / File Descrizione
mkdir -p ~/.termux/boot/ Crea la cartella per gli script di avvio.
nano ~/.termux/boot/start_dag Crea il file di avvio.
chmod +x ~/.termux/boot/start_dag Rende eseguibile il file di avvio.

Contenuto del file ~/.termux/boot/start_dag:

```bash
#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock
~/dag_sync.sh &
```

---

Questa è la cassetta degli attrezzi completa. Ogni comando è testato e pronto all'uso. Per qualsiasi dubbio, consulta il manuale esteso in docs/MANUALE_TERMUX.md.